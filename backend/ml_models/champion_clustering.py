"""
Champion Clustering Model
Groups champions by predefined roles: Fighter, Tank, Assassin, Mage, ADC, Support
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List
import os


class ChampionClusterer:
    """Clusters champions based on predefined roles"""

    def __init__(self, n_clusters: int = 6):
        """
        Initialize the clustering model

        Args:
            n_clusters: Number of role-based clusters (6: Fighter, Tank, Assassin, Mage, ADC, Support)
        """
        self.n_clusters = n_clusters
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=2, random_state=42)
        self.feature_names = None
        self.is_trained = False
        self.champion_data = None
        self.champion_roles = self._initialize_champion_roles()

        # Map role names to cluster IDs
        self.role_to_cluster = {
            'Tank': 0,
            'Fighter': 1,
            'Assassin': 2,
            'Mage': 3,
            'ADC': 4,
            'Support': 5
        }
        self.cluster_to_role = {v: k for k, v in self.role_to_cluster.items()}

    def _initialize_champion_roles(self) -> Dict[str, str]:
        """
        Initialize champion role classifications
        Categories: Tank, Fighter, Assassin, Mage, ADC, Support
        """
        return {
            # Tanks
            'Alistar': 'Tank', 'Amumu': 'Tank', 'Blitzcrank': 'Tank', 'Braum': 'Tank',
            'Chogath': 'Tank', 'DrMundo': 'Tank', 'Galio': 'Tank', 'Garen': 'Tank',
            'Gragas': 'Tank', 'JarvanIV': 'Tank', 'Leona': 'Tank',
            'Malphite': 'Tank', 'Maokai': 'Tank', 'Nautilus': 'Tank', 'Nunu': 'Tank',
            'Ornn': 'Tank', 'Poppy': 'Tank', 'Rammus': 'Tank', 'RekSai': 'Tank',
            'Rell': 'Tank', 'Sejuani': 'Tank', 'Shen': 'Tank', 'Singed': 'Tank',
            'Sion': 'Tank', 'Skarner': 'Tank', 'TahmKench': 'Tank',
            'Taric': 'Tank', 'Thresh': 'Tank', 'Urgot': 'Tank', 'Zac': 'Tank',
            'KSante': 'Tank',

            # Fighters
            'Aatrox': 'Fighter', 'Ambessa': 'Fighter', 'Camille': 'Fighter', 'Darius': 'Fighter',
            'Fiora': 'Fighter', 'Gangplank': 'Fighter', 'Gnar': 'Fighter', 'Gwen': 'Fighter',
            'Hecarim': 'Fighter', 'Illaoi': 'Fighter', 'Irelia': 'Fighter', 'Jax': 'Fighter',
            'Jayce': 'Fighter', 'Kayle': 'Fighter', 'Kled': 'Fighter', 'LeeSin': 'Fighter',
            'MasterYi': 'Fighter', 'Mordekaiser': 'Fighter',
            'Nasus': 'Fighter', 'Olaf': 'Fighter', 'Pantheon': 'Fighter', 'Renekton': 'Fighter',
            'Riven': 'Fighter', 'Rumble': 'Fighter', 'Sett': 'Fighter', 'Shyvana': 'Fighter',
            'Sylas': 'Fighter', 'Trundle': 'Fighter', 'Tryndamere': 'Fighter',
            'Udyr': 'Fighter', 'Vi': 'Fighter', 'Viego': 'Fighter', 'Volibear': 'Fighter',
            'Warwick': 'Fighter', 'Wukong': 'Fighter', 'XinZhao': 'Fighter',
            'Yasuo': 'Fighter', 'Yone': 'Fighter', 'Yorick': 'Fighter',

            # Assassins
            'Akali': 'Assassin', 'Akshan': 'Assassin', 'Belveth': 'Assassin', 'Briar': 'Assassin',
            'Diana': 'Assassin', 'Ekko': 'Assassin', 'Elise': 'Assassin', 'Evelynn': 'Assassin',
            'Fizz': 'Assassin', 'Graves': 'Assassin', 'Kassadin': 'Assassin', 'Katarina': 'Assassin',
            'Kayn': 'Assassin', 'Khazix': 'Assassin', 'Leblanc': 'Assassin', 'Lillia': 'Assassin',
            'Naafiri': 'Assassin', 'Nidalee': 'Assassin', 'Nilah': 'Assassin', 'Nocturne': 'Assassin',
            'Pyke': 'Assassin', 'Qiyana': 'Assassin', 'Rengar': 'Assassin', 'Shaco': 'Assassin',
            'Talon': 'Assassin', 'Zed': 'Assassin',

            # Mages
            'Ahri': 'Mage', 'Anivia': 'Mage', 'Annie': 'Mage', 'AurelionSol': 'Mage',
            'Aurora': 'Mage', 'Azir': 'Mage', 'Brand': 'Mage', 'Cassiopeia': 'Mage',
            'Corki': 'Mage', 'FiddleSticks': 'Mage', 'Heimerdinger': 'Mage', 'Hwei': 'Mage',
            'Karma': 'Mage', 'Karthus': 'Mage', 'Kennen': 'Mage', 'Lissandra': 'Mage',
            'Lux': 'Mage', 'Malzahar': 'Mage', 'Morgana': 'Mage', 'Neeko': 'Mage',
            'Orianna': 'Mage', 'Ryze': 'Mage', 'Swain': 'Mage', 'Syndra': 'Mage',
            'Taliyah': 'Mage', 'Teemo': 'Mage', 'TwistedFate': 'Mage',
            'Veigar': 'Mage', 'Velkoz': 'Mage', 'Vex': 'Mage', 'Viktor': 'Mage',
            'Vladimir': 'Mage', 'Xerath': 'Mage', 'Ziggs': 'Mage', 'Zilean': 'Mage',
            'Zoe': 'Mage', 'Zyra': 'Mage',

            # ADCs (Marksmen)
            'Aphelios': 'ADC', 'Ashe': 'ADC', 'Caitlyn': 'ADC', 'Draven': 'ADC',
            'Ezreal': 'ADC', 'Jhin': 'ADC', 'Jinx': 'ADC', 'Kaisa': 'ADC',
            'Kalista': 'ADC', 'KogMaw': 'ADC', 'Lucian': 'ADC', 'MissFortune': 'ADC',
            'Quinn': 'ADC', 'Samira': 'ADC', 'Sivir': 'ADC', 'Smolder': 'ADC',
            'Tristana': 'ADC', 'Twitch': 'ADC', 'Varus': 'ADC', 'Vayne': 'ADC',
            'Xayah': 'ADC', 'Zeri': 'ADC',

            # Supports
            'Bard': 'Support', 'Janna': 'Support', 'Lulu': 'Support', 'Milio': 'Support',
            'Nami': 'Support', 'Rakan': 'Support', 'Renata': 'Support', 'Senna': 'Support',
            'Seraphine': 'Support', 'Sona': 'Support', 'Soraka': 'Support', 'Yuumi': 'Support'
        }

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

    def train(self, X: pd.DataFrame) -> Dict:
        """
        Assign champions to clusters based on predefined roles

        Args:
            X: Feature DataFrame

        Returns:
            Dictionary with clustering metrics
        """
        print(f"Assigning champions to role-based clusters ({self.n_clusters} roles)...")
        print(f"Dataset size: {len(X)} champions")

        # Assign cluster based on champion role
        # Use apply to ensure alignment with DataFrame index
        def get_cluster_id(champion_name):
            role = self.champion_roles.get(champion_name, 'Fighter')  # Default to Fighter if unknown
            return self.role_to_cluster[role]

        self.champion_data['cluster'] = self.champion_data['champion'].apply(get_cluster_id)

        # Scale features for PCA visualization
        X_scaled = self.scaler.fit_transform(X)

        # PCA for visualization
        X_pca = self.pca.fit_transform(X_scaled)
        self.champion_data['pca1'] = X_pca[:, 0]
        self.champion_data['pca2'] = X_pca[:, 1]

        # Analyze clusters
        cluster_profiles = self.analyze_clusters()

        metrics = {
            'n_clusters': self.n_clusters,
            'cluster_profiles': cluster_profiles,
            'cluster_sizes': self.champion_data['cluster'].value_counts().to_dict(),
            'role_based': True,
            'roles': list(self.role_to_cluster.keys())
        }

        self.is_trained = True

        print("\n" + "=" * 50)
        print("ROLE-BASED CLUSTERING")
        print("=" * 50)
        print(f"Number of Role Clusters: {self.n_clusters}")
        print("\nCluster Sizes (by Role):")
        for cluster_id, size in sorted(metrics['cluster_sizes'].items()):
            role_name = self.cluster_to_role[cluster_id]
            print(f"  Cluster {cluster_id} ({role_name}): {size} champions")
        print("=" * 50)

        return metrics

    def analyze_clusters(self) -> Dict:
        """
        Analyze cluster characteristics based on predefined roles

        Returns:
            Dictionary with cluster profiles
        """
        profiles = {}

        # Define role descriptions
        role_descriptions = {
            'Tank': {
                'description': 'Durable champions who absorb damage and protect their team',
                'playstyle': 'Initiate fights, soak damage for the team, and provide crowd control. These champions are the backbone of team fights.'
            },
            'Fighter': {
                'description': 'Balanced champions who excel in extended fights and duels',
                'playstyle': 'Engage in prolonged fights, split-push effectively, and duel opponents. These champions are versatile in side lanes and team fights.'
            },
            'Assassin': {
                'description': 'High-damage champions who excel at eliminating key targets quickly',
                'playstyle': 'Focus on securing kills, dealing massive burst damage, and creating picks. These champions thrive on catching enemies out of position.'
            },
            'Mage': {
                'description': 'Champions who deal magic damage and control the battlefield',
                'playstyle': 'Deal sustained or burst magic damage, control zones, and provide utility. These champions excel at range and area effects.'
            },
            'ADC': {
                'description': 'Ranged champions who scale with gold and become powerful late-game threats',
                'playstyle': 'Focus on farming efficiently, scaling into late game, and dealing consistent physical damage. These champions need protection and time to reach their potential.'
            },
            'Support': {
                'description': 'Champions who protect and empower allies through healing, shielding, and utility',
                'playstyle': 'Provide vision, peel for carries, and enable teammates. These champions excel at keeping their team alive and creating opportunities.'
            }
        }

        for cluster_id in range(self.n_clusters):
            cluster_data = self.champion_data[self.champion_data['cluster'] == cluster_id]

            if len(cluster_data) == 0:
                continue

            role_name = self.cluster_to_role[cluster_id]
            role_info = role_descriptions[role_name]

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
                'top_champions': cluster_data.nlargest(5, 'totalGames')['champion'].tolist(),
                'archetype': role_name,
                'description': role_info['description'],
                'playstyle': role_info['playstyle']
            }

            profiles[cluster_id] = profile

        return profiles

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
        plt.title('Champion Clustering by Role', fontsize=16, fontweight='bold', pad=20)
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
                'Role': cluster_name,
                'Size': size
            })

        cluster_sizes_df = pd.DataFrame(cluster_data)

        plt.figure(figsize=(12, 7))
        bars = sns.barplot(data=cluster_sizes_df, x='Role', y='Size', hue='Role', palette='viridis', legend=False)
        plt.title('Champion Distribution by Role', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Champion Role', fontsize=12, fontweight='bold')
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
        plt.xlabel('Champion Role', fontsize=12, fontweight='bold')
        plt.ylabel('Performance Statistic', fontsize=12, fontweight='bold')
        plt.title('Role Characteristics', fontsize=16, fontweight='bold', pad=20)
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
            ax.set_title(f'{profiles[cluster_id]["archetype"]}',
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
            'scaler': self.scaler,
            'pca': self.pca,
            'feature_names': self.feature_names,
            'n_clusters': self.n_clusters,
            'champion_roles': self.champion_roles,
            'role_to_cluster': self.role_to_cluster
        }, path)
        print(f"Model saved to {path}")

    def load_model(self, path: str = 'ml_models/saved_models/champion_clusterer.pkl'):
        """Load a trained model"""
        data = joblib.load(path)
        self.scaler = data['scaler']
        self.pca = data['pca']
        self.feature_names = data['feature_names']
        self.n_clusters = data['n_clusters']
        self.champion_roles = data.get('champion_roles', self._initialize_champion_roles())
        self.role_to_cluster = data.get('role_to_cluster', self.role_to_cluster)
        self.cluster_to_role = {v: k for k, v in self.role_to_cluster.items()}
        self.is_trained = True
        print(f"Model loaded from {path}")
