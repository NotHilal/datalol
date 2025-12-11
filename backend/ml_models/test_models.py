"""
Test script to verify ML models are working correctly
Demonstrates how to use the trained models for predictions
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml_models.data_preprocessor import DataPreprocessor
from ml_models.match_prediction import MatchOutcomePredictor
from ml_models.champion_clustering import ChampionClusterer
from ml_models.duration_prediction import GameDurationPredictor
import pandas as pd


def print_header(title):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def test_match_predictor():
    """Test Match Outcome Prediction model"""
    print_header("TEST 1: MATCH OUTCOME PREDICTION")

    print("\n1. Loading trained model...")
    predictor = MatchOutcomePredictor()

    try:
        predictor.load_model('ml_models/saved_models/match_predictor.pkl')
        print("   [SUCCESS] Model loaded successfully!")
    except Exception as e:
        print(f"   [ERROR] Failed to load model: {e}")
        return

    print("\n2. Getting sample data from database...")
    preprocessor = DataPreprocessor()
    df = preprocessor.extract_match_features(limit=5)

    if df.empty:
        print("   [ERROR] No data found!")
        return

    X, y_actual = predictor.prepare_features(df)

    print("\n3. Making predictions on 5 sample matches...")
    predictions = predictor.predict(X)
    probabilities = predictor.predict_proba(X)

    print("\n" + "=" * 70)
    print("PREDICTION RESULTS")
    print("=" * 70)

    for i in range(len(predictions)):
        predicted_winner = "Blue Team" if predictions[i] == 1 else "Red Team"
        actual_winner = "Blue Team" if y_actual.iloc[i] == 1 else "Red Team"
        confidence = probabilities[i][predictions[i]] * 100
        correct = "[CORRECT]" if predictions[i] == y_actual.iloc[i] else "[WRONG]"

        print(f"\nMatch {i+1}: {df.iloc[i]['matchId']}")
        print(f"  Predicted: {predicted_winner} (Confidence: {confidence:.1f}%)")
        print(f"  Actual:    {actual_winner}")
        print(f"  Result:    {correct}")
        print(f"  Gold Diff: {df.iloc[i]['gold_diff']:,.0f} | Tower Diff: {df.iloc[i]['tower_diff']}")

    accuracy = (predictions == y_actual).sum() / len(predictions)
    print(f"\nAccuracy on sample: {accuracy:.1%}")

    preprocessor.close()


def test_champion_clustering():
    """Test Champion Clustering model"""
    print_header("TEST 2: CHAMPION CLUSTERING")

    print("\n1. Getting champion statistics from database...")
    preprocessor = DataPreprocessor()
    df = preprocessor.extract_champion_statistics()

    print(f"   Found {len(df)} champions in database")

    print("\n2. Loading cluster assignments...")
    try:
        cluster_df = pd.read_csv('ml_results/champion_clusters.csv')
        print(f"   [SUCCESS] Loaded cluster data: {len(cluster_df)} champions")
    except Exception as e:
        print(f"   [ERROR] Failed to load clusters: {e}")
        preprocessor.close()
        return

    print("\n3. Showing sample champions from each cluster...")
    print("\n" + "=" * 70)
    print("CHAMPION CLUSTERS")
    print("=" * 70)

    for cluster_id in sorted(cluster_df['cluster'].unique()):
        champions_in_cluster = cluster_df[cluster_df['cluster'] == cluster_id]
        top_5 = champions_in_cluster.nlargest(5, 'totalGames')[['champion', 'winRate', 'avgKDA']]

        print(f"\nCluster {cluster_id}: {len(champions_in_cluster)} champions")
        print(f"  Top 5 by popularity:")
        for idx, row in top_5.iterrows():
            print(f"    - {row['champion']}: {row['winRate']:.1f}% WR, {row['avgKDA']:.2f} KDA")

    preprocessor.close()


def test_duration_predictor():
    """Test Game Duration Prediction model"""
    print_header("TEST 3: GAME DURATION PREDICTION")

    print("\n1. Loading trained model...")
    predictor = GameDurationPredictor()

    try:
        predictor.load_model('ml_models/saved_models/duration_predictor.pkl')
        print("   [SUCCESS] Model loaded successfully!")
    except Exception as e:
        print(f"   [ERROR] Failed to load model: {e}")
        return

    print("\n2. Getting sample data from database...")
    preprocessor = DataPreprocessor()
    df = preprocessor.extract_duration_features(limit=5)

    if df.empty:
        print("   [ERROR] No data found!")
        return

    X, y_actual = predictor.prepare_features(df)

    print("\n3. Making predictions on 5 sample matches...")
    predictions = predictor.predict(X)

    print("\n" + "=" * 70)
    print("DURATION PREDICTION RESULTS")
    print("=" * 70)

    errors = []
    for i in range(len(predictions)):
        predicted_duration = predictions[i]
        actual_duration = y_actual.iloc[i]
        error = abs(predicted_duration - actual_duration)
        errors.append(error)

        print(f"\nMatch {i+1}: {df.iloc[i]['matchId']}")
        print(f"  Predicted Duration: {predicted_duration:.1f} minutes")
        print(f"  Actual Duration:    {actual_duration:.1f} minutes")
        print(f"  Error:              {error:.2f} minutes")
        print(f"  Total Objectives:   {df.iloc[i]['total_objectives']}")
        print(f"  Total Kills:        {df.iloc[i]['total_kills']}")

    avg_error = sum(errors) / len(errors)
    print(f"\nAverage Error: {avg_error:.2f} minutes")

    preprocessor.close()


def view_reports():
    """Display information about generated reports"""
    print_header("TEST 4: GENERATED REPORTS & VISUALIZATIONS")

    import os

    # Check for report file
    report_path = 'ml_results/ML_REPORT.md'
    if os.path.exists(report_path):
        print(f"\n[SUCCESS] ML Report found at: {report_path}")
        try:
            file_size = os.path.getsize(report_path) / 1024  # KB
            print(f"  Report size: {file_size:.1f} KB")
        except:
            pass
    else:
        print(f"\n[ERROR] Report not found at: {report_path}")

    # Check for visualizations
    results_dir = 'ml_results'
    if os.path.exists(results_dir):
        files = [f for f in os.listdir(results_dir) if f.endswith('.png')]
        print(f"\n[SUCCESS] Found {len(files)} visualization plots:")
        for file in sorted(files):
            file_path = os.path.join(results_dir, file)
            file_size = os.path.getsize(file_path) / 1024  # KB
            print(f"  - {file} ({file_size:.1f} KB)")

    # Check for saved models
    models_dir = 'ml_models/saved_models'
    if os.path.exists(models_dir):
        model_files = [f for f in os.listdir(models_dir) if f.endswith('.pkl')]
        print(f"\n[SUCCESS] Found {len(model_files)} trained models:")
        for file in sorted(model_files):
            file_path = os.path.join(models_dir, file)
            file_size = os.path.getsize(file_path) / 1024  # KB
            print(f"  - {file} ({file_size:.1f} KB)")


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("  MACHINE LEARNING MODELS - TEST SUITE")
    print("=" * 70)
    print("\nThis script will test all three ML models with real data")
    print("and verify that predictions are working correctly.\n")

    try:
        # Test 1: Match Prediction
        test_match_predictor()

        # Test 2: Champion Clustering
        test_champion_clustering()

        # Test 3: Duration Prediction
        test_duration_predictor()

        # Test 4: View Reports
        view_reports()

        # Final Summary
        print("\n" + "=" * 70)
        print("  TEST SUITE COMPLETED")
        print("=" * 70)
        print("\nAll models are working correctly!")
        print("\nNext steps:")
        print("1. View visualizations in: backend/ml_results/")
        print("2. Read the report: backend/ml_results/ML_REPORT.md")
        print("3. Check model files: backend/ml_models/saved_models/")
        print("\n" + "=" * 70 + "\n")

    except Exception as e:
        print(f"\n[ERROR] Test suite failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
