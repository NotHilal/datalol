"""
Quick script to train ONLY the draft prediction model
This updates the results_summary.json with real metrics
"""

import sys
import os
import json
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml_models.draft_prediction import ChampionDraftPredictor


def main():
    print("\n" + "=" * 80)
    print("  TRAINING DRAFT PREDICTION MODEL")
    print("=" * 80)
    print(f"  Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80 + "\n")

    try:
        # Initialize draft predictor
        print("Step 1: Initializing draft predictor...")
        draft_predictor = ChampionDraftPredictor()

        print("\nStep 2: Training draft prediction model...")
        print("Note: This may take 5-10 minutes as it analyzes champion synergies...")
        print("Training on full dataset for best accuracy...\n")

        # Train on full dataset without hyperparameter tuning (faster)
        draft_results = draft_predictor.train(limit=None, tune_hyperparameters=False)

        # Save model
        print("\nStep 3: Saving model...")
        draft_predictor.save_model()

        # Update results_summary.json
        print("\nStep 4: Updating results_summary.json...")
        results_path = 'ml_results/results_summary.json'

        # Load existing results
        if os.path.exists(results_path):
            with open(results_path, 'r') as f:
                results = json.load(f)
        else:
            results = {}

        # Add draft prediction metrics
        results['draft_prediction'] = draft_results['metrics']

        # Save updated results
        os.makedirs('ml_results', exist_ok=True)
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"Results saved to {results_path}")

        # Print summary
        print("\n" + "=" * 80)
        print("  TRAINING COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print(f"\nFinal Metrics:")
        print(f"  - Test Accuracy: {draft_results['metrics']['test_accuracy']:.2%}")
        print(f"  - ROC-AUC: {draft_results['metrics']['roc_auc']:.4f}")
        print(f"  - Precision: {draft_results['metrics']['precision']:.2%}")
        print(f"  - Recall: {draft_results['metrics']['recall']:.2%}")
        print(f"  - F1-Score: {draft_results['metrics']['f1_score']:.2%}")
        print(f"  - Cross-Val Accuracy: {draft_results['metrics']['cv_accuracy']:.2%} (±{draft_results['metrics']['cv_std']:.2%})")
        print(f"\n  End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80 + "\n")

        print("Next steps:")
        print("  1. Restart your backend server")
        print("  2. Reload the ML page in the frontend")
        print("  3. The draft prediction will now show REAL metrics!\n")

    except Exception as e:
        print(f"\n[ERROR] Error training draft predictor: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
