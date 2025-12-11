"""
Champion Clustering Model
Groups champions by playstyle using K-Means clustering
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from sklearn.decomposition import PCA
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List
import os


class ChampionClusterer:
    """Clusters champions based on performance statistics"""

    def __init__(self, n_clusters: int = 6):
        """
        Initialize the clustering model

        Args:
            n_clusters: Number of clusters to create
        """
        self.n_clusters = n_clusters
        self.model = KMeans(
            n_clusters=n_clusters,
            random_state=42,
            n_init=10,
            max_iter=300
        )
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=2, random_state=42)
        self.feature_names = None
        self.is_trained = False
        self.champion_data = None

    def prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare features for clustering

        Args:
            df: DataFrame with champion statistics

        Returns:
            DataFrame with selected features
        """
        # Select relevant features for clustering
        feature_cols = [
            'winRate',
            'avgKills',
            'avgDeaths',
            'avgAssists',
            'avgKDA',
            'avgGold',
            'avgDamage',
            'avgDamageTaken',
            'avgCS',
            'avgVisionScore'
        ]

        # Filter champions with sufficient games (e.g., at least 100 games)
        df_filtered = df[df['totalGames'] >= 100].copy()

        print(f"Filtering champions with at least 100 games: {len(df_filtered)} champions")

        X = df_filtered[feature_cols].copy()
        self.feature_names = feature_cols
        self.champion_data = df_filtered

        return X

    def find_optimal_clusters(self, X: pd.DataFrame, max_clusters: int = 10) -> Dict:
        """
        Find optimal number of clusters using elbow method and silhouette score

        Args:
            X: Feature DataFrame
            max_clusters: Maximum number of clusters to test

        Returns:
            Dictionary with scores for different cluster counts
        """
        print("Finding optimal number of clusters...")

        X_scaled = self.scaler.fit_transform(X)

        inertias = []
        silhouette_scores = []
        davies_bouldin_scores = []
        calinski_harabasz_scores = []

        cluster_range = range(2, max_clusters + 1)

        for k in cluster_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = kmeans.fit_predict(X_scaled)

            inertias.append(kmeans.inertia_)
            silhouette_scores.append(silhouette_score(X_scaled, labels))
            davies_bouldin_scores.append(davies_bouldin_score(X_scaled, labels))
            calinski_harabasz_scores.append(calinski_harabasz_score(X_scaled, labels))

        results = {
            'cluster_range': list(cluster_range),
            'inertias': inertias,
            'silhouette_scores': silhouette_scores,
            'davies_bouldin_scores': davies_bouldin_scores,
            'calinski_harabasz_scores': calinski_harabasz_scores
        }

        # Plot elbow curve
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))

        # Inertia (Elbow Method)
        axes[0, 0].plot(cluster_range, inertias, 'bo-', linewidth=2, markersize=8)
        axes[0, 0].set_xlabel('Number of Clusters')
        axes[0, 0].set_ylabel('Inertia')
        axes[0, 0].set_title('Elbow Method - Inertia', fontweight='bold')
        axes[0, 0].grid(alpha=0.3)

        # Silhouette Score (higher is better)
        axes[0, 1].plot(cluster_range, silhouette_scores, 'go-', linewidth=2, markersize=8)
        axes[0, 1].set_xlabel('Number of Clusters')
        axes[0, 1].set_ylabel('Silhouette Score')
        axes[0, 1].set_title('Silhouette Score (Higher is Better)', fontweight='bold')
        axes[0, 1].grid(alpha=0.3)

        # Davies-Bouldin Score (lower is better)
        axes[1, 0].plot(cluster_range, davies_bouldin_scores, 'ro-', linewidth=2, markersize=8)
        axes[1, 0].set_xlabel('Number of Clusters')
        axes[1, 0].set_ylabel('Davies-Bouldin Score')
        axes[1, 0].set_title('Davies-Bouldin Score (Lower is Better)', fontweight='bold')
        axes[1, 0].grid(alpha=0.3)

        # Calinski-Harabasz Score (higher is better)
        axes[1, 1].plot(cluster_range, calinski_harabasz_scores, 'mo-', linewidth=2, markersize=8)
        axes[1, 1].set_xlabel('Number of Clusters')
        axes[1, 1].set_ylabel('Calinski-Harabasz Score')
        axes[1, 1].set_title('Calinski-Harabasz Score (Higher is Better)', fontweight='bold')
        axes[1, 1].grid(alpha=0.3)

        plt.tight_layout()
        os.makedirs('ml_results', exist_ok=True)
        plt.savefig('ml_results/clustering_optimal_k.png', dpi=300)
        plt.close()

        print(f"Optimal cluster analysis plot saved to ml_results/clustering_optimal_k.png")

        return results

    def train(self, X: pd.DataFrame) -> Dict:
        """
        Train the clustering model

        Args:
            X: Feature DataFrame

        Returns:
            Dictionary with clustering metrics
        """
        print(f"Training Champion Clustering Model with {self.n_clusters} clusters...")
        print(f"Dataset size: {len(X)} champions")

        # Scale features
        X_scaled = self.scaler.fit_transform(X)

        # Fit clustering model
        self.model.fit(X_scaled)
        labels = self.model.labels_

        # Add cluster labels to champion data
        self.champion_data['cluster'] = labels

        # Calculate metrics
        silhouette = silhouette_score(X_scaled, labels)
        davies_bouldin = davies_bouldin_score(X_scaled, labels)
        calinski_harabasz = calinski_harabasz_score(X_scaled, labels)

        # PCA for visualization
        X_pca = self.pca.fit_transform(X_scaled)
        self.champion_data['pca1'] = X_pca[:, 0]
        self.champion_data['pca2'] = X_pca[:, 1]

        # Analyze clusters
        cluster_profiles = self.analyze_clusters()

        metrics = {
            'n_clusters': self.n_clusters,
            'silhouette_score': silhouette,
            'davies_bouldin_score': davies_bouldin,
            'calinski_harabasz_score': calinski_harabasz,
            'cluster_profiles': cluster_profiles,
            'cluster_sizes': self.champion_data['cluster'].value_counts().to_dict()
        }

        self.is_trained = True

        print("\n" + "=" * 50)
        print("CLUSTERING PERFORMANCE")
        print("=" * 50)
        print(f"Number of Clusters: {self.n_clusters}")
        print(f"Silhouette Score: {silhouette:.4f} (higher is better, range: -1 to 1)")
        print(f"Davies-Bouldin Score: {davies_bouldin:.4f} (lower is better)")
        print(f"Calinski-Harabasz Score: {calinski_harabasz:.2f} (higher is better)")
        print("\nCluster Sizes:")
        for cluster_id, size in sorted(metrics['cluster_sizes'].items()):
            print(f"  Cluster {cluster_id}: {size} champions")
        print("=" * 50)

        return metrics

    def analyze_clusters(self) -> Dict:
        """
        Analyze cluster characteristics with unique archetype naming

        Returns:
            Dictionary with cluster profiles
        """
        profiles = {}

        # First pass: collect all base archetypes and profiles
        base_archetypes = {}
        for cluster_id in range(self.n_clusters):
            cluster_data = self.champion_data[self.champion_data['cluster'] == cluster_id]

            profile = {
                'size': len(cluster_data),
                'avg_winRate': cluster_data['winRate'].mean(),
                'avg_kills': cluster_data['avgKills'].mean(),
                'avg_deaths': cluster_data['avgDeaths'].mean(),
                'avg_assists': cluster_data['avgAssists'].mean(),
                'avg_kda': cluster_data['avgKDA'].mean(),
                'avg_gold': cluster_data['avgGold'].mean(),
                'avg_damage': cluster_data['avgDamage'].mean(),
                'avg_damageTaken': cluster_data['avgDamageTaken'].mean(),
                'avg_cs': cluster_data['avgCS'].mean(),
                'avg_visionScore': cluster_data['avgVisionScore'].mean(),
                'top_champions': cluster_data.nlargest(5, 'totalGames')['champion'].tolist()
            }

            # Determine base archetype
            archetype_info = self._determine_archetype(profile)
            base_archetypes[cluster_id] = archetype_info['name']
            profiles[cluster_id] = profile
            profiles[cluster_id]['base_archetype_info'] = archetype_info

        # Second pass: detect duplicates and add distinguishing characteristics
        name_counts = {}
        for name in base_archetypes.values():
            name_counts[name] = name_counts.get(name, 0) + 1

        # Group duplicate clusters together
        duplicate_groups = {}
        for cluster_id, name in base_archetypes.items():
            if name_counts[name] > 1:
                if name not in duplicate_groups:
                    duplicate_groups[name] = []
                duplicate_groups[name].append(cluster_id)

        # For each group of duplicates, assign different suffixes by comparing stats
        for base_name, cluster_ids in duplicate_groups.items():
            # Get all profiles for this duplicate group
            duplicate_profiles = [(cid, profiles[cid]) for cid in cluster_ids]

            # Sort by a distinguishing stat and assign comparative suffixes
            suffixes = self._assign_comparative_suffixes(duplicate_profiles, base_name)

            # Apply suffixes to each cluster
            for cluster_id, suffix in zip(cluster_ids, suffixes):
                archetype_info = profiles[cluster_id]['base_archetype_info']
                archetype_info['name'] = f"{base_name} ({suffix})"
                archetype_info['description'] = f"{archetype_info['description']} - {suffix} variant"

        # Apply archetype info to all profiles
        for cluster_id in range(self.n_clusters):
            archetype_info = profiles[cluster_id]['base_archetype_info']
            profiles[cluster_id]['archetype'] = archetype_info['name']
            profiles[cluster_id]['description'] = archetype_info['description']
            profiles[cluster_id]['playstyle'] = archetype_info['playstyle']

            # Clean up temporary data
            del profiles[cluster_id]['base_archetype_info']

        return profiles

    def _determine_archetype(self, profile: Dict) -> Dict:
        """
        Determine champion archetype based on cluster profile using multi-criteria analysis
        Uses a scoring system to create more distinct archetypes
        """
        kills = profile['avg_kills']
        deaths = profile['avg_deaths']
        assists = profile['avg_assists']
        kda = profile['avg_kda']
        damage = profile['avg_damage']
        damage_taken = profile['avg_damageTaken']
        cs = profile['avg_cs']
        gold = profile['avg_gold']
        vision = profile['avg_visionScore']

        # High kills + high damage = Assassins/Burst
        if kills > 6.5 and damage > 18000 and kda > 2.8:
            return {
                'name': 'Assassins & Burst Carries',
                'description': 'High-damage champions who excel at eliminating key targets quickly',
                'playstyle': 'Focus on securing kills, dealing massive burst damage, and creating picks. These champions thrive on catching enemies out of position.'
            }

        # High assists + high vision = Pure Supports
        elif assists > 10 and vision > 35:
            return {
                'name': 'Enchanter Supports',
                'description': 'Champions who protect and empower allies through healing, shielding, and buffs',
                'playstyle': 'Provide vision, peel for carries, and enable teammates with buffs/shields. These champions excel at keeping their team alive.'
            }

        # High assists + moderate vision = Utility/Engage Supports
        elif assists > 8.5 and vision > 25 and damage < 14000:
            return {
                'name': 'Engage & Utility Supports',
                'description': 'Champions who initiate fights and provide crowd control for the team',
                'playstyle': 'Start team fights, provide hard CC, and create opportunities. These champions dictate the pace of the game.'
            }

        # Low deaths + high damage taken = Tanks
        elif deaths < 4.8 and damage_taken > 23000:
            return {
                'name': 'Tanks & Frontline',
                'description': 'Durable champions who absorb damage and protect their team',
                'playstyle': 'Initiate fights, soak damage for the team, and provide crowd control. These champions are the backbone of team fights.'
            }

        # High CS + high gold = Farming carries
        elif cs > 195 and gold > 11500:
            return {
                'name': 'Scaling Carries (ADC)',
                'description': 'Champions who scale with gold and become powerful late-game threats',
                'playstyle': 'Focus on farming efficiently, scaling into late game, and dealing consistent damage. These champions need time and gold to reach their potential.'
            }

        # Moderate damage + good KDA + decent CS = Fighters
        elif damage > 15500 and kda > 2.5 and cs > 155:
            return {
                'name': 'Skirmishers & Fighters',
                'description': 'Balanced champions who excel in extended fights and duels',
                'playstyle': 'Engage in prolonged fights, split-push effectively, and duel opponents. These champions are versatile in side lanes and team fights.'
            }

        # High assists + good damage = Team fight mages/initiators
        elif assists > 7.5 and damage > 15000:
            return {
                'name': 'Team Fight Controllers',
                'description': 'Champions who excel in coordinated team fights with area damage and CC',
                'playstyle': 'Maximize team fight presence, deal area damage, and create opportunities. These champions shine in 5v5 engagements.'
            }

        # Moderate-high damage + decent survival = Battle mages/bruisers
        elif damage > 14000 and damage_taken > 19000 and kda > 2.2:
            return {
                'name': 'Battle Mages & Bruisers',
                'description': 'Durable damage dealers who thrive in extended combat',
                'playstyle': 'Deal sustained damage while surviving in fights. These champions combine durability with damage output.'
            }

        # Fallback for balanced stats
        else:
            return {
                'name': 'Versatile All-Rounders',
                'description': 'Flexible champions who can adapt to multiple roles and playstyles',
                'playstyle': 'Adapt to team needs, fill gaps in composition, and provide balanced contributions. These champions can be played in various ways.'
            }

    def _assign_comparative_suffixes(self, duplicate_profiles: list, base_archetype: str) -> list:
        """
        Assign unique suffixes to duplicate archetypes by comparing their stats

        Args:
            duplicate_profiles: List of (cluster_id, profile) tuples for duplicates
            base_archetype: The base archetype name

        Returns:
            List of unique suffixes in the same order as input profiles
        """
        if len(duplicate_profiles) == 1:
            return ['']

        # Extract profiles for comparison
        profiles = [p[1] for p in duplicate_profiles]

        # Determine which stat varies most between duplicates (highest variance)
        stat_variances = {}
        stats_to_check = ['avg_kills', 'avg_deaths', 'avg_assists', 'avg_kda',
                          'avg_damage', 'avg_damageTaken', 'avg_cs', 'avg_gold', 'avg_visionScore']

        for stat in stats_to_check:
            values = [p[stat] for p in profiles]
            if len(values) > 1:
                variance = max(values) - min(values)
                stat_variances[stat] = variance

        # Find the most distinguishing stat
        most_distinguishing_stat = max(stat_variances, key=stat_variances.get)

        # Sort profiles by the most distinguishing stat
        sorted_profiles = sorted(enumerate(profiles), key=lambda x: x[1][most_distinguishing_stat])

        # Create suffixes based on archetype type and distinguishing stat
        suffixes_map = {}

        if 'Support' in base_archetype or 'Enchanter' in base_archetype:
            if most_distinguishing_stat == 'avg_visionScore':
                suffix_options = ['Low Vision', 'High Vision', 'Max Vision']
            elif most_distinguishing_stat == 'avg_assists':
                suffix_options = ['Protective', 'Engage-Focused', 'Roaming']
            else:
                suffix_options = ['Type A', 'Type B', 'Type C']

        elif 'Versatile' in base_archetype or 'All-Rounder' in base_archetype:
            if most_distinguishing_stat == 'avg_damage':
                suffix_options = ['Balanced', 'Damage-Focused', 'High Damage']
            elif most_distinguishing_stat == 'avg_damageTaken':
                suffix_options = ['Glass Cannon', 'Bruiser-Style', 'Tank-Style']
            elif most_distinguishing_stat == 'avg_cs':
                suffix_options = ['Roaming', 'Farming', 'Hyper-Farming']
            else:
                suffix_options = ['Type A', 'Type B', 'Type C']

        elif 'Tank' in base_archetype or 'Frontline' in base_archetype:
            if most_distinguishing_stat == 'avg_damageTaken':
                suffix_options = ['Moderate Durability', 'High Durability', 'Ultra Tank']
            elif most_distinguishing_stat == 'avg_damage':
                suffix_options = ['Pure Tank', 'Bruiser Tank', 'Fighter Tank']
            else:
                suffix_options = ['Type A', 'Type B', 'Type C']

        elif 'Carry' in base_archetype or 'ADC' in base_archetype:
            if most_distinguishing_stat == 'avg_damage':
                suffix_options = ['Standard', 'High DPS', 'Hyper Carry']
            elif most_distinguishing_stat == 'avg_cs':
                suffix_options = ['Early Game', 'Mid Game', 'Late Game']
            else:
                suffix_options = ['Type A', 'Type B', 'Type C']

        elif 'Mage' in base_archetype or 'Battle Mage' in base_archetype or 'Controller' in base_archetype:
            if most_distinguishing_stat == 'avg_damage':
                suffix_options = ['Poke', 'Burst', 'Sustained']
            elif most_distinguishing_stat == 'avg_damageTaken':
                suffix_options = ['Squishy', 'Bruiser-Style', 'Tanky']
            else:
                suffix_options = ['Type A', 'Type B', 'Type C']

        elif 'Fighter' in base_archetype or 'Skirmisher' in base_archetype:
            if most_distinguishing_stat == 'avg_kills':
                suffix_options = ['Utility', 'Balanced', 'Aggressive']
            elif most_distinguishing_stat == 'avg_damageTaken':
                suffix_options = ['Assassin-Style', 'Balanced', 'Juggernaut']
            else:
                suffix_options = ['Type A', 'Type B', 'Type C']

        else:
            # Generic suffixes
            suffix_options = ['Type A', 'Type B', 'Type C', 'Type D']

        # Assign suffixes based on sorted order
        for i, (original_idx, profile) in enumerate(sorted_profiles):
            suffix_idx = min(i, len(suffix_options) - 1)
            suffixes_map[original_idx] = suffix_options[suffix_idx]

        # Return suffixes in original order
        return [suffixes_map[i] for i in range(len(profiles))]

    def plot_results(self, metrics: Dict, save_dir: str = 'ml_results'):
        """
        Generate visualization plots

        Args:
            metrics: Dictionary with clustering metrics
            save_dir: Directory to save plots
        """
        os.makedirs(save_dir, exist_ok=True)

        # 1. PCA Scatter Plot with cluster names
        plt.figure(figsize=(14, 10))

        # Create color map
        colors = plt.cm.tab10(np.linspace(0, 1, self.n_clusters))

        # Plot each cluster separately with its name
        for cluster_id in range(self.n_clusters):
            cluster_mask = self.champion_data['cluster'] == cluster_id
            cluster_name = metrics['cluster_profiles'][cluster_id]['archetype']

            plt.scatter(
                self.champion_data.loc[cluster_mask, 'pca1'],
                self.champion_data.loc[cluster_mask, 'pca2'],
                c=[colors[cluster_id]],
                label=f'{cluster_name}',
                s=100,
                alpha=0.6,
                edgecolors='black',
                linewidth=0.5
            )

        plt.xlabel(f'First Principal Component ({self.pca.explained_variance_ratio_[0]:.2%} variance)', fontsize=12)
        plt.ylabel(f'Second Principal Component ({self.pca.explained_variance_ratio_[1]:.2%} variance)', fontsize=12)
        plt.title('Champion Clustering by Playstyle', fontsize=16, fontweight='bold', pad=20)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', frameon=True, fancybox=True, shadow=True)
        plt.grid(alpha=0.3, linestyle='--')
        plt.tight_layout()
        plt.savefig(os.path.join(save_dir, 'champion_clustering_pca.png'), dpi=300, bbox_inches='tight')
        plt.close()

        # 2. Cluster Sizes with meaningful names
        cluster_data = []
        for cluster_id, size in sorted(metrics['cluster_sizes'].items()):
            cluster_name = metrics['cluster_profiles'][cluster_id]['archetype']
            cluster_data.append({
                'Archetype': cluster_name,
                'Size': size
            })

        cluster_sizes_df = pd.DataFrame(cluster_data)

        plt.figure(figsize=(12, 7))
        bars = sns.barplot(data=cluster_sizes_df, x='Archetype', y='Size', hue='Archetype', palette='viridis', legend=False)
        plt.title('Champion Distribution by Playstyle', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Champion Archetype', fontsize=12, fontweight='bold')
        plt.ylabel('Number of Champions', fontsize=12, fontweight='bold')
        plt.xticks(rotation=45, ha='right')

        # Add value labels on bars
        for i, v in enumerate(cluster_sizes_df['Size']):
            plt.text(i, v + 0.5, str(v), ha='center', va='bottom', fontweight='bold', fontsize=11)

        plt.tight_layout()
        plt.savefig(os.path.join(save_dir, 'champion_clustering_sizes.png'), dpi=300, bbox_inches='tight')
        plt.close()

        # 3. Cluster Characteristics Heatmap with archetype names
        profiles_df = pd.DataFrame(metrics['cluster_profiles']).T
        numeric_cols = ['avg_kills', 'avg_deaths', 'avg_assists', 'avg_kda',
                       'avg_damage', 'avg_damageTaken', 'avg_cs', 'avg_visionScore']

        # Create column labels with archetype names
        archetype_labels = [profiles_df.loc[i, 'archetype'] for i in range(self.n_clusters)]

        # Prepare data for heatmap (ensure numeric types)
        heatmap_data = profiles_df[numeric_cols].astype(float).T
        heatmap_data.columns = archetype_labels

        # Better stat names for display
        stat_display_names = {
            'avg_kills': 'Kills',
            'avg_deaths': 'Deaths',
            'avg_assists': 'Assists',
            'avg_kda': 'KDA Ratio',
            'avg_damage': 'Damage Dealt',
            'avg_damageTaken': 'Damage Taken',
            'avg_cs': 'CS (Farm)',
            'avg_visionScore': 'Vision Score'
        }
        heatmap_data.index = [stat_display_names.get(idx, idx) for idx in heatmap_data.index]

        plt.figure(figsize=(14, 8))
        sns.heatmap(
            heatmap_data,
            annot=True,
            fmt='.1f',
            cmap='YlOrRd',
            cbar_kws={'label': 'Average Value'},
            linewidths=0.5,
            linecolor='gray'
        )
        plt.xlabel('Champion Archetype', fontsize=12, fontweight='bold')
        plt.ylabel('Performance Statistic', fontsize=12, fontweight='bold')
        plt.title('Playstyle Characteristics by Archetype', fontsize=16, fontweight='bold', pad=20)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(save_dir, 'champion_clustering_heatmap.png'), dpi=300, bbox_inches='tight')
        plt.close()

        # 4. Radar Chart for Cluster Profiles
        self._plot_radar_charts(metrics['cluster_profiles'], save_dir)

        print(f"Clustering plots saved to {save_dir}/")

    def _plot_radar_charts(self, profiles: Dict, save_dir: str):
        """Create radar charts for each cluster"""
        categories = ['Kills', 'Deaths', 'Assists', 'Damage', 'CS', 'Vision']

        # Normalize values for radar chart
        all_values = {
            'kills': [p['avg_kills'] for p in profiles.values()],
            'deaths': [p['avg_deaths'] for p in profiles.values()],
            'assists': [p['avg_assists'] for p in profiles.values()],
            'damage': [p['avg_damage'] for p in profiles.values()],
            'cs': [p['avg_cs'] for p in profiles.values()],
            'vision': [p['avg_visionScore'] for p in profiles.values()]
        }

        # Min-max normalization
        normalized_profiles = {}
        for cluster_id, profile in profiles.items():
            normalized_profiles[cluster_id] = [
                (profile['avg_kills'] - min(all_values['kills'])) / (max(all_values['kills']) - min(all_values['kills'])),
                (profile['avg_deaths'] - min(all_values['deaths'])) / (max(all_values['deaths']) - min(all_values['deaths'])),
                (profile['avg_assists'] - min(all_values['assists'])) / (max(all_values['assists']) - min(all_values['assists'])),
                (profile['avg_damage'] - min(all_values['damage'])) / (max(all_values['damage']) - min(all_values['damage'])),
                (profile['avg_cs'] - min(all_values['cs'])) / (max(all_values['cs']) - min(all_values['cs'])),
                (profile['avg_visionScore'] - min(all_values['vision'])) / (max(all_values['vision']) - min(all_values['vision']))
            ]

        # Create subplots for radar charts
        n_clusters = len(profiles)
        cols = 3
        rows = (n_clusters + cols - 1) // cols

        fig, axes = plt.subplots(rows, cols, figsize=(15, 5 * rows), subplot_kw=dict(projection='polar'))
        axes = axes.flatten() if n_clusters > 1 else [axes]

        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        angles += angles[:1]

        for idx, (cluster_id, values) in enumerate(normalized_profiles.items()):
            values += values[:1]
            ax = axes[idx]
            ax.plot(angles, values, 'o-', linewidth=2)
            ax.fill(angles, values, alpha=0.25)
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(categories)
            ax.set_ylim(0, 1)
            ax.set_title(f'Cluster {cluster_id}: {profiles[cluster_id]["archetype"]}',
                        fontweight='bold', pad=20)
            ax.grid(True)

        # Hide unused subplots
        for idx in range(n_clusters, len(axes)):
            axes[idx].axis('off')

        plt.tight_layout()
        plt.savefig(os.path.join(save_dir, 'champion_clustering_radar.png'), dpi=300)
        plt.close()

    def get_cluster_summary(self) -> pd.DataFrame:
        """Get summary of champions in each cluster"""
        if self.champion_data is None:
            raise ValueError("Model must be trained first")

        return self.champion_data[['champion', 'cluster', 'totalGames', 'winRate',
                                   'avgKDA', 'avgDamage']].sort_values(['cluster', 'totalGames'],
                                                                       ascending=[True, False])

    def save_model(self, path: str = 'ml_models/saved_models/champion_clusterer.pkl'):
        """Save the trained model"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'pca': self.pca,
            'feature_names': self.feature_names,
            'n_clusters': self.n_clusters
        }, path)
        print(f"Model saved to {path}")

    def load_model(self, path: str = 'ml_models/saved_models/champion_clusterer.pkl'):
        """Load a trained model"""
        data = joblib.load(path)
        self.model = data['model']
        self.scaler = data['scaler']
        self.pca = data['pca']
        self.feature_names = data['feature_names']
        self.n_clusters = data['n_clusters']
        self.is_trained = True
        print(f"Model loaded from {path}")
