"""
Main script to train all machine learning models
Generates comprehensive evaluation reports and visualizations
"""

import sys
import os
from datetime import datetime
import json

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml_models.data_preprocessor import DataPreprocessor
from ml_models.match_prediction import MatchOutcomePredictor
from ml_models.champion_clustering import ChampionClusterer
from ml_models.duration_prediction import GameDurationPredictor


def print_section_header(title):
    """Print a formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def save_results_summary(results: dict, filepath: str = 'ml_results/results_summary.json'):
    """Save all results to a JSON file"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # Convert numpy arrays and other non-serializable objects
    serializable_results = {}
    for model_name, metrics in results.items():
        serializable_results[model_name] = {}
        for key, value in metrics.items():
            if key in ['confusion_matrix', 'classification_report', 'cv_scores',
                      'cluster_profiles', 'cv_rmse']:
                # Skip complex objects
                continue
            elif isinstance(value, dict):
                serializable_results[model_name][key] = value
            else:
                try:
                    json.dumps(value)
                    serializable_results[model_name][key] = value
                except:
                    serializable_results[model_name][key] = str(value)

    with open(filepath, 'w') as f:
        json.dump(serializable_results, f, indent=2)

    print(f"Results summary saved to {filepath}")


def generate_markdown_report(results: dict, filepath: str = 'ml_results/ML_REPORT.md'):
    """Generate a markdown report with all results"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, 'w') as f:
        f.write("# Machine Learning Models - Evaluation Report\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")

        # Match Outcome Prediction
        f.write("## 1. Match Outcome Prediction (Classification)\n\n")
        f.write("### Model: Random Forest Classifier\n\n")
        f.write("**Objective:** Predict which team (Blue or Red) will win the match based on in-game statistics.\n\n")

        if 'match_prediction' in results:
            mp = results['match_prediction']
            f.write("### Performance Metrics\n\n")
            f.write("| Metric | Score |\n")
            f.write("|--------|-------|\n")
            f.write(f"| Test Accuracy | {mp.get('test_accuracy', 0):.4f} |\n")
            f.write(f"| Precision | {mp.get('precision', 0):.4f} |\n")
            f.write(f"| Recall | {mp.get('recall', 0):.4f} |\n")
            f.write(f"| F1-Score | {mp.get('f1_score', 0):.4f} |\n")
            f.write(f"| ROC-AUC | {mp.get('roc_auc', 0):.4f} |\n")
            f.write(f"| Cross-Validation Accuracy | {mp.get('cv_mean', 0):.4f} (+/- {mp.get('cv_std', 0):.4f}) |\n\n")

            f.write("### Top 10 Most Important Features\n\n")
            if 'feature_importance' in mp:
                sorted_features = sorted(mp['feature_importance'].items(),
                                       key=lambda x: x[1], reverse=True)[:10]
                f.write("| Feature | Importance |\n")
                f.write("|---------|------------|\n")
                for feature, importance in sorted_features:
                    f.write(f"| {feature} | {importance:.4f} |\n")
            f.write("\n")

            f.write("### Visualizations\n\n")
            f.write("- Confusion Matrix: `match_prediction_confusion_matrix.png`\n")
            f.write("- Feature Importance: `match_prediction_feature_importance.png`\n")
            f.write("- ROC Curve: `match_prediction_roc_curve.png`\n")
            f.write("- Performance Metrics: `match_prediction_metrics.png`\n\n")

        f.write("---\n\n")

        # Champion Clustering
        f.write("## 2. Champion Clustering (Unsupervised Learning)\n\n")
        f.write("### Model: K-Means Clustering\n\n")
        f.write("**Objective:** Group champions into distinct playstyle categories based on performance statistics.\n\n")

        if 'champion_clustering' in results:
            cc = results['champion_clustering']
            f.write("### Clustering Metrics\n\n")
            f.write("| Metric | Score | Interpretation |\n")
            f.write("|--------|-------|----------------|\n")
            f.write(f"| Number of Clusters | {cc.get('n_clusters', 0)} | - |\n")
            f.write(f"| Silhouette Score | {cc.get('silhouette_score', 0):.4f} | Higher is better (range: -1 to 1) |\n")
            f.write(f"| Davies-Bouldin Score | {cc.get('davies_bouldin_score', 0):.4f} | Lower is better |\n")
            f.write(f"| Calinski-Harabasz Score | {cc.get('calinski_harabasz_score', 0):.2f} | Higher is better |\n\n")

            f.write("### Cluster Sizes\n\n")
            if 'cluster_sizes' in cc:
                f.write("| Cluster ID | Number of Champions |\n")
                f.write("|------------|---------------------|\n")
                for cluster_id, size in sorted(cc['cluster_sizes'].items()):
                    f.write(f"| {cluster_id} | {size} |\n")
            f.write("\n")

            f.write("### Cluster Profiles\n\n")
            if 'cluster_profiles' in cc:
                for cluster_id, profile in cc['cluster_profiles'].items():
                    f.write(f"#### Cluster {cluster_id}: {profile.get('archetype', 'Unknown')}\n\n")
                    f.write(f"- **Size:** {profile.get('size', 0)} champions\n")
                    f.write(f"- **Avg Win Rate:** {profile.get('avg_winRate', 0):.2f}%\n")
                    f.write(f"- **Avg KDA:** {profile.get('avg_kda', 0):.2f}\n")
                    f.write(f"- **Avg Damage:** {profile.get('avg_damage', 0):.0f}\n")
                    f.write(f"- **Avg CS:** {profile.get('avg_cs', 0):.1f}\n")
                    f.write(f"- **Top Champions:** {', '.join(profile.get('top_champions', []))}\n\n")

            f.write("### Visualizations\n\n")
            f.write("- PCA Scatter Plot: `champion_clustering_pca.png`\n")
            f.write("- Cluster Sizes: `champion_clustering_sizes.png`\n")
            f.write("- Characteristics Heatmap: `champion_clustering_heatmap.png`\n")
            f.write("- Radar Charts: `champion_clustering_radar.png`\n")
            f.write("- Optimal K Analysis: `clustering_optimal_k.png`\n\n")

        f.write("---\n\n")

        # Game Duration Prediction
        f.write("## 3. Game Duration Prediction (Regression)\n\n")
        f.write("### Model: Random Forest Regressor\n\n")
        f.write("**Objective:** Predict the duration of a match based on in-game statistics.\n\n")

        if 'duration_prediction' in results:
            dp = results['duration_prediction']
            f.write("### Performance Metrics\n\n")
            f.write("| Metric | Random Forest | Linear Regression (Baseline) |\n")
            f.write("|--------|---------------|-------------------------------|\n")
            f.write(f"| RMSE (minutes) | {dp.get('test_rmse', 0):.2f} | {dp.get('baseline_rmse', 0):.2f} |\n")
            f.write(f"| MAE (minutes) | {dp.get('test_mae', 0):.2f} | {dp.get('baseline_mae', 0):.2f} |\n")
            f.write(f"| R² Score | {dp.get('test_r2', 0):.4f} | {dp.get('baseline_r2', 0):.4f} |\n")
            f.write(f"| MAPE | {dp.get('test_mape', 0):.4f} | - |\n")
            f.write(f"| CV RMSE | {dp.get('cv_rmse_mean', 0):.2f} (+/- {dp.get('cv_rmse_std', 0):.2f}) | - |\n\n")

            improvement = ((dp.get('baseline_rmse', 0) - dp.get('test_rmse', 0)) / dp.get('baseline_rmse', 1)) * 100
            f.write(f"**Improvement over baseline:** {improvement:.2f}%\n\n")

            f.write("### Top 10 Most Important Features\n\n")
            if 'feature_importance' in dp:
                sorted_features = sorted(dp['feature_importance'].items(),
                                       key=lambda x: x[1], reverse=True)[:10]
                f.write("| Feature | Importance |\n")
                f.write("|---------|------------|\n")
                for feature, importance in sorted_features:
                    f.write(f"| {feature} | {importance:.4f} |\n")
            f.write("\n")

            f.write("### Visualizations\n\n")
            f.write("- Actual vs Predicted: `duration_prediction_scatter.png`\n")
            f.write("- Residuals Plot: `duration_prediction_residuals.png`\n")
            f.write("- Residuals Distribution: `duration_prediction_residuals_dist.png`\n")
            f.write("- Feature Importance: `duration_prediction_feature_importance.png`\n")
            f.write("- Model Comparison: `duration_prediction_comparison.png`\n")
            f.write("- Error by Duration Range: `duration_prediction_error_by_range.png`\n\n")

        f.write("---\n\n")

        f.write("## Summary\n\n")
        f.write("This project successfully implemented three machine learning models:\n\n")
        f.write("1. **Classification Model:** Accurately predicts match outcomes with high precision\n")
        f.write("2. **Clustering Model:** Identifies distinct champion playstyle archetypes\n")
        f.write("3. **Regression Model:** Predicts game duration with reasonable accuracy\n\n")
        f.write("All models were evaluated using appropriate metrics and visualizations.\n")

    print(f"Markdown report saved to {filepath}")


def main():
    """Main execution function"""
    print("\n" + "=" * 80)
    print("  LEAGUE OF LEGENDS - MACHINE LEARNING MODEL TRAINING")
    print("=" * 80)
    print(f"  Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80 + "\n")

    results = {}

    # Initialize data preprocessor
    print("Initializing data preprocessor...")
    preprocessor = DataPreprocessor()

    # ========================================================================
    # 1. MATCH OUTCOME PREDICTION
    # ========================================================================
    print_section_header("MODEL 1: MATCH OUTCOME PREDICTION")

    try:
        # Extract features
        print("Step 1: Extracting match features...")
        match_df = preprocessor.extract_match_features(limit=10000)  # Use 10k matches for speed

        # Initialize and train model
        print("\nStep 2: Training model...")
        predictor = MatchOutcomePredictor()
        X, y = predictor.prepare_features(match_df)
        metrics_match = predictor.train(X, y)

        # Generate visualizations
        print("\nStep 3: Generating visualizations...")
        predictor.plot_results(metrics_match)

        # Save model
        print("\nStep 4: Saving model...")
        predictor.save_model()

        results['match_prediction'] = metrics_match
        print("\n[SUCCESS] Match Outcome Prediction completed successfully!")

    except Exception as e:
        print(f"\n[ERROR] Error in Match Outcome Prediction: {e}")
        import traceback
        traceback.print_exc()

    # ========================================================================
    # 2. CHAMPION CLUSTERING
    # ========================================================================
    print_section_header("MODEL 2: CHAMPION CLUSTERING")

    try:
        # Extract champion statistics
        print("Step 1: Extracting champion statistics...")
        champion_df = preprocessor.extract_champion_statistics()

        # Initialize and train model
        print("\nStep 2: Finding optimal number of clusters...")
        clusterer = ChampionClusterer(n_clusters=6)
        X_champ = clusterer.prepare_features(champion_df)

        # Find optimal K
        optimal_k_results = clusterer.find_optimal_clusters(X_champ, max_clusters=10)

        print("\nStep 3: Training clustering model...")
        metrics_cluster = clusterer.train(X_champ)

        # Generate visualizations
        print("\nStep 4: Generating visualizations...")
        clusterer.plot_results(metrics_cluster)

        # Save model
        print("\nStep 5: Saving model...")
        clusterer.save_model()

        # Save cluster summary
        cluster_summary = clusterer.get_cluster_summary()
        cluster_summary.to_csv('ml_results/champion_clusters.csv', index=False)
        print("Cluster summary saved to ml_results/champion_clusters.csv")

        results['champion_clustering'] = metrics_cluster
        print("\n[SUCCESS] Champion Clustering completed successfully!")

    except Exception as e:
        print(f"\n[ERROR] Error in Champion Clustering: {e}")
        import traceback
        traceback.print_exc()

    # ========================================================================
    # 3. GAME DURATION PREDICTION
    # ========================================================================
    print_section_header("MODEL 3: GAME DURATION PREDICTION")

    try:
        # Extract duration features
        print("Step 1: Extracting features for duration prediction...")
        duration_df = preprocessor.extract_duration_features(limit=10000)  # Use 10k matches

        # Initialize and train model
        print("\nStep 2: Training model...")
        duration_predictor = GameDurationPredictor()
        X_dur, y_dur = duration_predictor.prepare_features(duration_df)
        metrics_duration = duration_predictor.train(X_dur, y_dur)

        # Generate visualizations
        print("\nStep 3: Generating visualizations...")
        duration_predictor.plot_results(metrics_duration)

        # Save model
        print("\nStep 4: Saving model...")
        duration_predictor.save_model()

        results['duration_prediction'] = metrics_duration
        print("\n[SUCCESS] Game Duration Prediction completed successfully!")

    except Exception as e:
        print(f"\n[ERROR] Error in Game Duration Prediction: {e}")
        import traceback
        traceback.print_exc()

    # ========================================================================
    # GENERATE REPORTS
    # ========================================================================
    print_section_header("GENERATING COMPREHENSIVE REPORTS")

    try:
        # Save results summary
        save_results_summary(results)

        # Generate markdown report
        generate_markdown_report(results)

        print("\n[SUCCESS] All reports generated successfully!")

    except Exception as e:
        print(f"\n[ERROR] Error generating reports: {e}")
        import traceback
        traceback.print_exc()

    # Close database connection
    preprocessor.close()

    # Final summary
    print("\n" + "=" * 80)
    print("  TRAINING COMPLETED")
    print("=" * 80)
    print(f"  End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print("\nResults saved to:")
    print("  - ml_results/ (visualizations)")
    print("  - ml_models/saved_models/ (trained models)")
    print("  - ml_results/ML_REPORT.md (comprehensive report)")
    print("  - ml_results/results_summary.json (metrics summary)")
    print("  - ml_results/champion_clusters.csv (cluster assignments)")
    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    main()
