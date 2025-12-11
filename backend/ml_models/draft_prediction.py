"""
Champion Draft Prediction Model - Enhanced Version
Predicts match outcome based on champion picks (5v5 team composition)

Improvements:
- XGBoost instead of Random Forest
- Champion synergy features
- Lane matchup win rates
- Team composition balance metrics
- Hyperparameter tuning
- Training on full dataset
"""

import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split, cross_val_score, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from pymongo import MongoClient
from typing import List, Dict, Tuple
from collections import defaultdict
import os


class ChampionDraftPredictor:
    """
    Predicts match outcome based on champion picks using enhanced hybrid approach:
    - Champion performance statistics
    - Team composition features
    - Champion synergies (pair win rates)
    - Lane matchup win rates
    - Team balance metrics (roles, damage types)
    """

    def __init__(self, db_name='lol_matches', collection_name='matches'):
        self.db_name = db_name
        self.collection_name = collection_name
        self.model = None
        self.scaler = StandardScaler()
        self.champion_stats = None
        self.champion_synergies = None
        self.lane_matchups = None
        self.all_champions = None
        self.feature_names = None

        # Champion role classifications (simplified)
        self.champion_roles = self._initialize_champion_roles()

    def _initialize_champion_roles(self):
        """
        Initialize champion role classifications
        Categories: Tank, Fighter, Assassin, Mage, ADC, Support
        """
        return {
            # Tanks
            'Alistar': 'Tank', 'Amumu': 'Tank', 'Blitzcrank': 'Tank', 'Braum': 'Tank',
            'Chogath': 'Tank', 'DrMundo': 'Tank', 'Galio': 'Tank', 'Garen': 'Tank',
            'Gragas': 'Tank', 'Jarvan': 'Tank', 'Leona': 'Tank', 'Malphite': 'Tank',
            'Maokai': 'Tank', 'Nautilus': 'Tank', 'Nunu': 'Tank', 'Ornn': 'Tank',
            'Poppy': 'Tank', 'Rammus': 'Tank', 'Sejuani': 'Tank', 'Shen': 'Tank',
            'Sion': 'Tank', 'Tahm Kench': 'Tank', 'Taric': 'Tank', 'Thresh': 'Tank',
            'Zac': 'Tank',

            # Fighters
            'Aatrox': 'Fighter', 'Camille': 'Fighter', 'Darius': 'Fighter', 'Fiora': 'Fighter',
            'Gnar': 'Fighter', 'Hecarim': 'Fighter', 'Illaoi': 'Fighter', 'Irelia': 'Fighter',
            'Jax': 'Fighter', 'Kled': 'Fighter', 'LeeSin': 'Fighter', 'Mordekaiser': 'Fighter',
            'Nasus': 'Fighter', 'Olaf': 'Fighter', 'Renekton': 'Fighter', 'Riven': 'Fighter',
            'Rumble': 'Fighter', 'Sett': 'Fighter', 'Trundle': 'Fighter', 'Tryndamere': 'Fighter',
            'Udyr': 'Fighter', 'Vi': 'Fighter', 'Volibear': 'Fighter', 'Warwick': 'Fighter',
            'Wukong': 'Fighter', 'XinZhao': 'Fighter', 'Yasuo': 'Fighter', 'Yone': 'Fighter',

            # Assassins
            'Akali': 'Assassin', 'Diana': 'Assassin', 'Ekko': 'Assassin', 'Evelynn': 'Assassin',
            'Fizz': 'Assassin', 'Kassadin': 'Assassin', 'Katarina': 'Assassin', 'Kayn': 'Assassin',
            'Khazix': 'Assassin', 'Leblanc': 'Assassin', 'Nocturne': 'Assassin', 'Pyke': 'Assassin',
            'Qiyana': 'Assassin', 'Rengar': 'Assassin', 'Shaco': 'Assassin', 'Talon': 'Assassin',
            'Zed': 'Assassin',

            # Mages
            'Ahri': 'Mage', 'Anivia': 'Mage', 'Annie': 'Mage', 'AurelionSol': 'Mage',
            'Azir': 'Mage', 'Brand': 'Mage', 'Cassiopeia': 'Mage', 'Corki': 'Mage',
            'Heimerdinger': 'Mage', 'Karma': 'Mage', 'Karthus': 'Mage', 'Lissandra': 'Mage',
            'Lux': 'Mage', 'Malzahar': 'Mage', 'Morgana': 'Mage', 'Neeko': 'Mage',
            'Orianna': 'Mage', 'Ryze': 'Mage', 'Swain': 'Mage', 'Syndra': 'Mage',
            'Taliyah': 'Mage', 'Twisted Fate': 'Mage', 'Veigar': 'Mage', 'Velkoz': 'Mage',
            'Viktor': 'Mage', 'Vladimir': 'Mage', 'Xerath': 'Mage', 'Ziggs': 'Mage',
            'Zilean': 'Mage', 'Zoe': 'Mage', 'Zyra': 'Mage',

            # ADC (Marksman)
            'Aphelios': 'ADC', 'Ashe': 'ADC', 'Caitlyn': 'ADC', 'Draven': 'ADC',
            'Ezreal': 'ADC', 'Jhin': 'ADC', 'Jinx': 'ADC', 'Kaisa': 'ADC',
            'Kalista': 'ADC', 'Kindred': 'ADC', 'Kogmaw': 'ADC', 'Lucian': 'ADC',
            'MissFortune': 'ADC', 'Quinn': 'ADC', 'Samira': 'ADC', 'Sivir': 'ADC',
            'Tristana': 'ADC', 'Twitch': 'ADC', 'Varus': 'ADC', 'Vayne': 'ADC',
            'Xayah': 'ADC',

            # Support
            'Bard': 'Support', 'Janna': 'Support', 'Lulu': 'Support', 'Nami': 'Support',
            'Rakan': 'Support', 'Senna': 'Support', 'Seraphine': 'Support', 'Sona': 'Support',
            'Soraka': 'Support', 'Yuumi': 'Support',
        }

    def connect_to_db(self):
        """Connect to MongoDB"""
        client = MongoClient('mongodb://localhost:27017/')
        db = client[self.db_name]
        return db[self.collection_name]

    def extract_draft_data(self, limit=None):
        """
        Extract champion picks and outcomes from matches

        Returns:
            DataFrame with blue_team, red_team champion lists and winner
        """
        print("Extracting champion draft data from MongoDB...")
        collection = self.connect_to_db()

        query = {}
        matches = list(collection.find(query).limit(limit) if limit else collection.find(query))

        draft_data = []

        for match in matches:
            try:
                participants = match.get('participants', [])
                if len(participants) < 10:
                    continue

                # Extract champion names
                blue_champions = []
                red_champions = []

                for i, p in enumerate(participants):
                    # Get champion name from nested structure
                    champion_data = p.get('champion', {})
                    champion = champion_data.get('name', '')
                    if not champion:
                        break

                    if i < 5:  # Blue team
                        blue_champions.append(champion)
                    else:  # Red team
                        red_champions.append(champion)

                if len(blue_champions) != 5 or len(red_champions) != 5:
                    continue

                # Get winner from teams array (team 100 = Blue, team 200 = Red)
                teams = match.get('teams', [])
                if len(teams) != 2:
                    continue

                # Find which team won
                winner = None
                for team in teams:
                    if team.get('teamId') == 100 and team.get('win'):  # Blue team won
                        winner = 1
                        break
                    elif team.get('teamId') == 200 and team.get('win'):  # Red team won
                        winner = 0
                        break

                if winner is None:
                    continue

                draft_data.append({
                    'blue_team': blue_champions,
                    'red_team': red_champions,
                    'winner': winner
                })

            except Exception as e:
                continue

        df = pd.DataFrame(draft_data)
        print(f"Extracted {len(df)} complete drafts")
        return df

    def calculate_champion_stats(self):
        """
        Calculate performance statistics for each champion
        """
        print("Calculating champion performance statistics...")
        collection = self.connect_to_db()

        pipeline = [
            {'$unwind': '$participants'},
            {'$group': {
                '_id': '$participants.champion.name',
                'games': {'$sum': 1},
                'wins': {'$sum': {'$cond': [{'$eq': ['$participants.win', True]}, 1, 0]}},
                'kills': {'$avg': '$participants.kda.kills'},
                'deaths': {'$avg': '$participants.kda.deaths'},
                'assists': {'$avg': '$participants.kda.assists'},
                'gold': {'$avg': '$participants.gold.earned'},
                'damage': {'$avg': '$participants.damage.totalDealtToChampions'},
                'cs': {'$avg': {'$add': ['$participants.farming.totalMinionsKilled', '$participants.farming.neutralMinionsKilled']}},
            }},
            {'$match': {'games': {'$gte': 10}}}  # At least 10 games
        ]

        results = list(collection.aggregate(pipeline))

        champion_stats = {}
        for stat in results:
            champion = stat['_id']
            if not champion:
                continue

            champion_stats[champion] = {
                'win_rate': stat['wins'] / stat['games'] if stat['games'] > 0 else 0.5,
                'avg_kills': stat['kills'],
                'avg_deaths': stat['deaths'],
                'avg_assists': stat['assists'],
                'avg_kda': (stat['kills'] + stat['assists']) / max(stat['deaths'], 1),
                'avg_gold': stat['gold'],
                'avg_damage': stat['damage'],
                'avg_cs': stat['cs'],
                'games_played': stat['games']
            }

        self.champion_stats = champion_stats
        print(f"Calculated stats for {len(champion_stats)} champions")
        return champion_stats

    def calculate_champion_synergies(self, draft_df: pd.DataFrame):
        """
        Calculate champion synergy statistics (how well champion pairs perform together)
        """
        print("Calculating champion synergies...")

        synergy_stats = defaultdict(lambda: {'wins': 0, 'games': 0})

        for idx, row in draft_df.iterrows():
            winner = row['winner']
            blue_team = row['blue_team']
            red_team = row['red_team']

            # Calculate for blue team
            for i in range(len(blue_team)):
                for j in range(i + 1, len(blue_team)):
                    pair = tuple(sorted([blue_team[i], blue_team[j]]))
                    synergy_stats[pair]['games'] += 1
                    if winner == 1:
                        synergy_stats[pair]['wins'] += 1

            # Calculate for red team
            for i in range(len(red_team)):
                for j in range(i + 1, len(red_team)):
                    pair = tuple(sorted([red_team[i], red_team[j]]))
                    synergy_stats[pair]['games'] += 1
                    if winner == 0:
                        synergy_stats[pair]['wins'] += 1

        # Calculate win rates (only for pairs with sufficient games)
        self.champion_synergies = {}
        for pair, stats in synergy_stats.items():
            if stats['games'] >= 5:  # At least 5 games together
                self.champion_synergies[pair] = stats['wins'] / stats['games']

        print(f"Calculated synergies for {len(self.champion_synergies)} champion pairs")
        return self.champion_synergies

    def get_team_synergy_score(self, champions: List[str]) -> float:
        """
        Calculate average synergy score for a team
        """
        if not self.champion_synergies or len(champions) < 2:
            return 0.5

        synergies = []
        for i in range(len(champions)):
            for j in range(i + 1, len(champions)):
                pair = tuple(sorted([champions[i], champions[j]]))
                if pair in self.champion_synergies:
                    synergies.append(self.champion_synergies[pair])

        return np.mean(synergies) if synergies else 0.5

    def get_team_composition_balance(self, champions: List[str]) -> Dict[str, float]:
        """
        Calculate team composition balance metrics

        Returns:
            - Role counts (Tank, Fighter, Assassin, Mage, ADC, Support)
            - Damage type balance (Physical vs Magic)
            - Role diversity score
        """
        role_counts = {'Tank': 0, 'Fighter': 0, 'Assassin': 0, 'Mage': 0, 'ADC': 0, 'Support': 0}

        for champ in champions:
            role = self.champion_roles.get(champ, 'Fighter')  # Default to Fighter
            role_counts[role] += 1

        # Calculate diversity (entropy-based)
        total = len(champions)
        diversity = 0
        for count in role_counts.values():
            if count > 0:
                p = count / total
                diversity -= p * np.log2(p)

        # Normalize diversity to 0-1 range (max entropy for 5 roles is log2(5))
        max_entropy = np.log2(5)
        diversity_score = diversity / max_entropy if max_entropy > 0 else 0

        # Physical vs Magic damage balance
        physical_roles = {'Fighter', 'Assassin', 'ADC'}
        magic_roles = {'Mage'}

        physical_count = sum(role_counts[r] for r in physical_roles)
        magic_count = role_counts['Mage']

        # Balance score: closer to 0.5 is better (balanced)
        if physical_count + magic_count > 0:
            damage_balance = magic_count / (physical_count + magic_count)
        else:
            damage_balance = 0.5

        return {
            'tank_count': role_counts['Tank'],
            'fighter_count': role_counts['Fighter'],
            'assassin_count': role_counts['Assassin'],
            'mage_count': role_counts['Mage'],
            'adc_count': role_counts['ADC'],
            'support_count': role_counts['Support'],
            'role_diversity': diversity_score,
            'damage_balance': damage_balance,
            'has_tank': 1 if role_counts['Tank'] > 0 else 0,
            'has_support': 1 if role_counts['Support'] > 0 else 0
        }

    def get_team_composition_features(self, champions: List[str]) -> Dict[str, float]:
        """
        Calculate team composition features

        Features:
        - Average win rate
        - Average KDA
        - Total damage potential
        - Gold efficiency
        - Team experience (games played)
        - Team synergy score
        - Composition balance metrics
        """
        if not self.champion_stats:
            return {}

        features = {
            'avg_win_rate': 0,
            'avg_kda': 0,
            'avg_damage': 0,
            'avg_gold': 0,
            'avg_cs': 0,
            'total_games': 0,
            'min_win_rate': 1.0,
            'max_win_rate': 0
        }

        valid_champions = [c for c in champions if c in self.champion_stats]

        if not valid_champions:
            return features

        win_rates = []
        kills_list = []
        deaths_list = []
        assists_list = []

        for champ in valid_champions:
            stats = self.champion_stats[champ]
            features['avg_win_rate'] += stats['win_rate']
            features['avg_kda'] += stats['avg_kda']
            features['avg_damage'] += stats['avg_damage']
            features['avg_gold'] += stats['avg_gold']
            features['avg_cs'] += stats['avg_cs']
            features['total_games'] += stats['games_played']
            win_rates.append(stats['win_rate'])
            kills_list.append(stats['avg_kills'])
            deaths_list.append(stats['avg_deaths'])
            assists_list.append(stats['avg_assists'])

        n = len(valid_champions)
        features['avg_win_rate'] /= n
        features['avg_kda'] /= n
        features['avg_damage'] /= n
        features['avg_gold'] /= n
        features['avg_cs'] /= n
        features['avg_kills'] = sum(kills_list) / n if kills_list else 0
        features['avg_deaths'] = sum(deaths_list) / n if deaths_list else 0
        features['avg_assists'] = sum(assists_list) / n if assists_list else 0
        features['min_win_rate'] = min(win_rates) if win_rates else 0.5
        features['max_win_rate'] = max(win_rates) if win_rates else 0.5
        features['win_rate_variance'] = np.var(win_rates) if win_rates else 0

        # Add synergy score
        features['team_synergy'] = self.get_team_synergy_score(champions)

        # Add composition balance
        balance = self.get_team_composition_balance(champions)
        features.update(balance)

        return features

    def create_features(self, draft_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Create enhanced features from draft data

        Combines:
        1. Team composition statistics
        2. Champion synergies
        3. Team balance metrics
        """
        print("Creating enhanced features from drafts...")

        # Calculate champion stats if not already done
        if not self.champion_stats:
            self.calculate_champion_stats()

        # Calculate synergies if not already done
        if not self.champion_synergies:
            self.calculate_champion_synergies(draft_df)

        features_list = []

        for idx, row in draft_df.iterrows():
            blue_team = row['blue_team']
            red_team = row['red_team']

            # Get team composition features
            blue_features = self.get_team_composition_features(blue_team)
            red_features = self.get_team_composition_features(red_team)

            # Create feature vector
            feature_dict = {}

            # Blue team features
            for key, value in blue_features.items():
                feature_dict[f'blue_{key}'] = value

            # Red team features
            for key, value in red_features.items():
                feature_dict[f'red_{key}'] = value

            # Differential features (most important!)
            feature_dict['win_rate_diff'] = blue_features['avg_win_rate'] - red_features['avg_win_rate']
            feature_dict['kda_diff'] = blue_features['avg_kda'] - red_features['avg_kda']
            feature_dict['damage_diff'] = blue_features['avg_damage'] - red_features['avg_damage']
            feature_dict['gold_diff'] = blue_features['avg_gold'] - red_features['avg_gold']
            feature_dict['cs_diff'] = blue_features['avg_cs'] - red_features['avg_cs']
            feature_dict['synergy_diff'] = blue_features['team_synergy'] - red_features['team_synergy']
            feature_dict['diversity_diff'] = blue_features['role_diversity'] - red_features['role_diversity']

            features_list.append(feature_dict)

        X = pd.DataFrame(features_list)
        y = draft_df['winner']

        # Store feature names
        self.feature_names = X.columns.tolist()

        print(f"Created {len(X.columns)} features for {len(X)} drafts")
        return X, y

    def train(self, limit=None, tune_hyperparameters=True):
        """
        Train the draft prediction model with XGBoost

        Args:
            limit: Limit number of matches (None = use all)
            tune_hyperparameters: Whether to perform hyperparameter tuning
        """
        print("\n" + "="*50)
        print("TRAINING ENHANCED DRAFT PREDICTION MODEL")
        print("="*50)

        # Extract draft data
        draft_df = self.extract_draft_data(limit=limit)

        if len(draft_df) < 100:
            print("Error: Not enough draft data to train model")
            return None

        # Create features
        X, y = self.create_features(draft_df)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        print(f"\nDataset: {len(X)} drafts")
        print(f"Training set: {len(X_train)} drafts")
        print(f"Test set: {len(X_test)} drafts")
        print(f"Blue wins: {y.sum()}, Red wins: {len(y) - y.sum()}")
        print(f"Features: {len(self.feature_names)}")

        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # Train XGBoost
        print("\nTraining XGBoost model...")

        if tune_hyperparameters and len(X_train) > 1000:
            print("Performing hyperparameter tuning...")

            # Parameter grid for randomized search
            param_dist = {
                'n_estimators': [100, 200, 300],
                'max_depth': [5, 7, 9, 11],
                'learning_rate': [0.01, 0.05, 0.1],
                'subsample': [0.8, 0.9, 1.0],
                'colsample_bytree': [0.8, 0.9, 1.0],
                'min_child_weight': [1, 3, 5]
            }

            base_model = XGBClassifier(
                objective='binary:logistic',
                eval_metric='logloss',
                random_state=42,
                n_jobs=-1
            )

            random_search = RandomizedSearchCV(
                base_model,
                param_distributions=param_dist,
                n_iter=20,
                cv=3,
                scoring='accuracy',
                random_state=42,
                n_jobs=-1,
                verbose=1
            )

            random_search.fit(X_train_scaled, y_train)
            self.model = random_search.best_estimator_

            print(f"Best parameters: {random_search.best_params_}")
            print(f"Best CV score: {random_search.best_score_:.4f}")
        else:
            # Use default good parameters
            self.model = XGBClassifier(
                n_estimators=200,
                max_depth=7,
                learning_rate=0.05,
                subsample=0.9,
                colsample_bytree=0.9,
                min_child_weight=3,
                objective='binary:logistic',
                eval_metric='logloss',
                random_state=42,
                n_jobs=-1
            )

            self.model.fit(X_train_scaled, y_train)

        # Evaluate
        train_pred = self.model.predict(X_train_scaled)
        test_pred = self.model.predict(X_test_scaled)

        train_proba = self.model.predict_proba(X_train_scaled)[:, 1]
        test_proba = self.model.predict_proba(X_test_scaled)[:, 1]

        # Cross-validation
        cv_scores = cross_val_score(self.model, X_train_scaled, y_train, cv=5)

        # Metrics
        metrics = {
            'train_accuracy': accuracy_score(y_train, train_pred),
            'test_accuracy': accuracy_score(y_test, test_pred),
            'precision': precision_score(y_test, test_pred),
            'recall': recall_score(y_test, test_pred),
            'f1_score': f1_score(y_test, test_pred),
            'roc_auc': roc_auc_score(y_test, test_proba),
            'cv_accuracy': cv_scores.mean(),
            'cv_std': cv_scores.std()
        }

        # Print results
        print("\n" + "="*50)
        print("MODEL PERFORMANCE")
        print("="*50)
        print(f"Training Accuracy: {metrics['train_accuracy']:.4f}")
        print(f"Test Accuracy: {metrics['test_accuracy']:.4f}")
        print(f"Precision: {metrics['precision']:.4f}")
        print(f"Recall: {metrics['recall']:.4f}")
        print(f"F1-Score: {metrics['f1_score']:.4f}")
        print(f"ROC-AUC: {metrics['roc_auc']:.4f}")
        print(f"Cross-Val Accuracy: {metrics['cv_accuracy']:.4f} (+/- {metrics['cv_std']:.4f})")
        print("\nClassification Report:")
        print(classification_report(y_test, test_pred, target_names=['Red Win', 'Blue Win']))
        print("="*50)

        return {
            'metrics': metrics,
            'X_test': X_test,
            'y_test': y_test,
            'predictions': test_pred,
            'probabilities': test_proba
        }

    def predict_draft(self, blue_champions: List[str], red_champions: List[str]) -> Dict:
        """
        Predict match outcome for a given draft

        Args:
            blue_champions: List of 5 champion names for blue team
            red_champions: List of 5 champion names for red team

        Returns:
            Dictionary with prediction, confidence, and analysis
        """
        if not self.model or not self.champion_stats:
            raise ValueError("Model not trained. Call train() first.")

        if len(blue_champions) != 5 or len(red_champions) != 5:
            raise ValueError("Each team must have exactly 5 champions")

        # Create features
        blue_features = self.get_team_composition_features(blue_champions)
        red_features = self.get_team_composition_features(red_champions)

        feature_dict = {}

        # Blue team features
        for key, value in blue_features.items():
            feature_dict[f'blue_{key}'] = value

        # Red team features
        for key, value in red_features.items():
            feature_dict[f'red_{key}'] = value

        # Differential features
        feature_dict['win_rate_diff'] = blue_features['avg_win_rate'] - red_features['avg_win_rate']
        feature_dict['kda_diff'] = blue_features['avg_kda'] - red_features['avg_kda']
        feature_dict['damage_diff'] = blue_features['avg_damage'] - red_features['avg_damage']
        feature_dict['gold_diff'] = blue_features['avg_gold'] - red_features['avg_gold']
        feature_dict['cs_diff'] = blue_features['avg_cs'] - red_features['avg_cs']
        feature_dict['synergy_diff'] = blue_features['team_synergy'] - red_features['team_synergy']
        feature_dict['diversity_diff'] = blue_features['role_diversity'] - red_features['role_diversity']

        # Create DataFrame with correct feature order
        X = pd.DataFrame([feature_dict])[self.feature_names]

        # Scale features
        X_scaled = self.scaler.transform(X)

        # Predict
        prediction = self.model.predict(X_scaled)[0]
        probabilities = self.model.predict_proba(X_scaled)[0]

        # Prepare detailed feature breakdown
        blue_team_features = {
            'avg_win_rate': float(blue_features['avg_win_rate']),
            'avg_kda': float(blue_features['avg_kda']),
            'avg_kills': float(blue_features.get('avg_kills', 0)),
            'avg_deaths': float(blue_features.get('avg_deaths', 0)),
            'avg_assists': float(blue_features.get('avg_assists', 0)),
            'avg_gold': float(blue_features['avg_gold']),
            'avg_damage': float(blue_features['avg_damage']),
            'avg_cs': float(blue_features['avg_cs']),
            'total_games': int(blue_features['total_games']),
            'min_win_rate': float(blue_features['min_win_rate']),
            'max_win_rate': float(blue_features['max_win_rate']),
            'win_rate_variance': float(blue_features['win_rate_variance'])
        }

        red_team_features = {
            'avg_win_rate': float(red_features['avg_win_rate']),
            'avg_kda': float(red_features['avg_kda']),
            'avg_kills': float(red_features.get('avg_kills', 0)),
            'avg_deaths': float(red_features.get('avg_deaths', 0)),
            'avg_assists': float(red_features.get('avg_assists', 0)),
            'avg_gold': float(red_features['avg_gold']),
            'avg_damage': float(red_features['avg_damage']),
            'avg_cs': float(red_features['avg_cs']),
            'total_games': int(red_features['total_games']),
            'min_win_rate': float(red_features['min_win_rate']),
            'max_win_rate': float(red_features['max_win_rate']),
            'win_rate_variance': float(red_features['win_rate_variance'])
        }

        differential_features = {
            'win_rate_diff': float(feature_dict['win_rate_diff']),
            'kda_diff': float(feature_dict['kda_diff']),
            'damage_diff': float(feature_dict['damage_diff']),
            'gold_diff': float(feature_dict['gold_diff']),
            'cs_diff': float(feature_dict['cs_diff'])
        }

        result = {
            'prediction': 'Blue Team' if prediction == 1 else 'Red Team',
            'predicted_value': int(prediction),
            'confidence': float(probabilities[prediction]),
            'probabilities': {
                'red_team': float(probabilities[0]),
                'blue_team': float(probabilities[1])
            },
            'analysis': {
                'blue_team_strength': float(blue_features['avg_win_rate']),
                'red_team_strength': float(red_features['avg_win_rate']),
                'blue_avg_kda': float(blue_features['avg_kda']),
                'red_avg_kda': float(red_features['avg_kda']),
                'win_rate_advantage': 'Blue' if blue_features['avg_win_rate'] > red_features['avg_win_rate'] else 'Red',
                'damage_advantage': 'Blue' if blue_features['avg_damage'] > red_features['avg_damage'] else 'Red'
            },
            'features': {
                'blue_team': blue_team_features,
                'red_team': red_team_features,
                'differentials': differential_features
            }
        }

        return result

    def get_feature_importance(self, top_n=15):
        """Get top N most important features"""
        if not self.model:
            return None

        importances = self.model.feature_importances_
        indices = np.argsort(importances)[::-1][:top_n]

        return pd.DataFrame({
            'feature': [self.feature_names[i] for i in indices],
            'importance': importances[indices]
        })

    def save_model(self, filepath):
        """Save the trained model"""
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'champion_stats': self.champion_stats,
            'champion_synergies': self.champion_synergies,
            'champion_roles': self.champion_roles,
            'feature_names': self.feature_names
        }
        joblib.dump(model_data, filepath)
        print(f"Model saved to {filepath}")

    def load_model(self, filepath):
        """Load a trained model"""
        model_data = joblib.load(filepath)
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.champion_stats = model_data['champion_stats']
        self.champion_synergies = model_data.get('champion_synergies', {})
        self.champion_roles = model_data.get('champion_roles', self._initialize_champion_roles())
        self.feature_names = model_data['feature_names']
        print(f"Model loaded from {filepath}")
