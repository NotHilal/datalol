"""
Train Champion Role Classification Model
Generates role-based clustering using predefined categories
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_preprocessor import DataPreprocessor
from champion_clustering import ChampionClusterer
import json

def main():
    print("=" * 70)
    print("CHAMPION ROLE CLASSIFICATION TRAINING")
    print("=" * 70)

    # Initialize data preprocessor
    preprocessor = DataPreprocessor()

    # Extract champion statistics
    print("\nStep 1: Extracting champion statistics from MongoDB...")
    champion_stats = preprocessor.extract_champion_statistics()

    if champion_stats.empty:
        print("ERROR: No champion data found!")
        return

    print(f"Successfully extracted {len(champion_stats)} champions")

    # Initialize clusterer
    clusterer = ChampionClusterer(n_clusters=6)

    # Prepare features
    print("\nStep 2: Preparing features for role classification...")
    X = clusterer.prepare_features(champion_stats)

    # Assign champions to role-based clusters
    print("\nStep 3: Assigning champions to predefined roles...")
    metrics = clusterer.train(X)

    # Generate visualizations
    print("\nStep 4: Generating role visualizations...")
    save_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ml_results')
    clusterer.plot_results(metrics, save_dir=save_dir)

    # Save cluster assignments
    print("\nStep 5: Saving role assignments...")
    cluster_summary = clusterer.get_cluster_summary()
    csv_path = os.path.join(save_dir, 'champion_clusters.csv')
    cluster_summary.to_csv(csv_path, index=False)
    print(f"Saved role assignments to {csv_path}")

    # Save cluster profiles for API
    print("\nStep 5.5: Saving role profiles for API...")
    profiles_path = os.path.join(save_dir, 'cluster_profiles.json')
    # Convert numpy types to Python native types for JSON serialization
    cluster_profiles_json = {}
    for cluster_id, profile in metrics['cluster_profiles'].items():
        cluster_profiles_json[str(cluster_id)] = {
            'archetype': profile['archetype'],
            'description': profile['description'],
            'playstyle': profile['playstyle'],
            'size': int(profile['size']),
            'avg_winRate': float(profile['avg_winRate']),
            'avg_kills': float(profile['avg_kills']),
            'avg_deaths': float(profile['avg_deaths']),
            'avg_assists': float(profile['avg_assists']),
            'avg_kda': float(profile['avg_kda']),
            'top_champions': profile['top_champions']
        }

    with open(profiles_path, 'w') as f:
        json.dump(cluster_profiles_json, f, indent=2)
    print(f"Saved role profiles to {profiles_path}")

    # Save the model
    print("\nStep 6: Saving model...")
    clusterer.save_model()

    # Update results summary
    results_file = os.path.join(save_dir, 'results_summary.json')
    if os.path.exists(results_file):
        with open(results_file, 'r') as f:
            results = json.load(f)
    else:
        results = {}

    results['champion_clustering'] = {
        'n_clusters': metrics['n_clusters'],
        'cluster_sizes': metrics['cluster_sizes'],
        'role_based': True,
        'roles': metrics['roles']
    }

    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nUpdated {results_file}")

    print("\n" + "=" * 70)
    print("CHAMPION ROLE CLASSIFICATION COMPLETE!")
    print("=" * 70)
    print("\nRole Distribution:")
    for role in metrics['roles']:
        cluster_id = clusterer.role_to_cluster[role]
        size = metrics['cluster_sizes'].get(cluster_id, 0)
        print(f"  {role}: {size} champions")

    print("\nVisualizations saved to ml_results/:")
    print("  - champion_clustering_pca.png")
    print("  - champion_clustering_sizes.png")
    print("  - champion_clustering_heatmap.png")
    print("  - champion_clustering_radar.png")

    # Close MongoDB connection
    preprocessor.close()

if __name__ == "__main__":
    main()
