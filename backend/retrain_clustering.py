"""
Retrain clustering model with improved archetype names
"""
from ml_models.data_preprocessor import DataPreprocessor
from ml_models.champion_clustering import ChampionClusterer
import json
import os

print("Extracting champion statistics...")
prep = DataPreprocessor()
df = prep.extract_champion_statistics()

print("Training clustering model...")
clusterer = ChampionClusterer(n_clusters=6)
X = clusterer.prepare_features(df)
metrics = clusterer.train(X)

print("Generating visualizations...")
clusterer.plot_results(metrics)

print("Saving model and cluster summary...")
clusterer.save_model()
cluster_summary = clusterer.get_cluster_summary()
cluster_summary.to_csv('ml_results/champion_clusters.csv', index=False)

print("Saving cluster profiles...")
os.makedirs('ml_results', exist_ok=True)
with open('ml_results/cluster_profiles.json', 'w') as f:
    json.dump(metrics['cluster_profiles'], f, indent=2)

print("\nCluster Archetypes:")
for cluster_id, profile in metrics['cluster_profiles'].items():
    print(f"\nCluster {cluster_id}: {profile['archetype']}")
    print(f"  Description: {profile['description']}")
    print(f"  Size: {profile['size']} champions")

print("\n\nClustering complete!")
