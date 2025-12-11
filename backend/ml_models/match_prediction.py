"""
Match Outcome Prediction Model
Predicts which team will win based on in-game statistics
Uses Random Forest Classification
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve
)
from sklearn.preprocessing import StandardScaler
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Tuple
import os


class MatchOutcomePredictor:
    """Predicts match outcomes using Random Forest Classification"""

    def __init__(self):
        """Initialize the model"""
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        self.scaler = StandardScaler()
        self.feature_names = None
        self.is_trained = False

    def prepare_features(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Prepare features and target from dataframe

        Args:
            df: DataFrame with match data

        Returns:
            Tuple of (features, target)
        """
        # Select feature columns (exclude identifiers and target)
        feature_cols = [
            'blue_avg_level', 'red_avg_level',
            'blue_kills', 'red_kills',
            'blue_deaths', 'red_deaths',
            'blue_assists', 'red_assists',
            'blue_gold', 'red_gold',
            'blue_damage', 'red_damage',
            'blue_cs', 'red_cs',
            'blue_barons', 'red_barons',
            'blue_dragons', 'red_dragons',
            'blue_towers', 'red_towers',
            'gold_diff', 'kills_diff', 'damage_diff', 'cs_diff',
            'tower_diff', 'dragon_diff'
        ]

        X = df[feature_cols].copy()
        y = df['blue_win'].copy()

        self.feature_names = feature_cols

        return X, y

    def train(self, X: pd.DataFrame, y: pd.Series, test_size: float = 0.2) -> Dict:
        """
        Train the model and return evaluation metrics

        Args:
            X: Feature DataFrame
            y: Target Series
            test_size: Proportion of data for testing

        Returns:
            Dictionary with evaluation metrics
        """
        print("Training Match Outcome Prediction Model...")
        print(f"Dataset size: {len(X)} samples")

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )

        print(f"Training set: {len(X_train)} samples")
        print(f"Test set: {len(X_test)} samples")
        print(f"Class distribution - Blue wins: {y.sum()}, Red wins: {len(y) - y.sum()}")

        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # Train model
        print("Training Random Forest model...")
        self.model.fit(X_train_scaled, y_train)
        self.is_trained = True

        # Make predictions
        y_train_pred = self.model.predict(X_train_scaled)
        y_test_pred = self.model.predict(X_test_scaled)
        y_test_proba = self.model.predict_proba(X_test_scaled)[:, 1]

        # Calculate metrics
        metrics = {
            'train_accuracy': accuracy_score(y_train, y_train_pred),
            'test_accuracy': accuracy_score(y_test, y_test_pred),
            'precision': precision_score(y_test, y_test_pred),
            'recall': recall_score(y_test, y_test_pred),
            'f1_score': f1_score(y_test, y_test_pred),
            'roc_auc': roc_auc_score(y_test, y_test_proba),
            'confusion_matrix': confusion_matrix(y_test, y_test_pred),
            'classification_report': classification_report(y_test, y_test_pred,
                                                          target_names=['Red Win', 'Blue Win']),
            'feature_importance': dict(zip(self.feature_names, self.model.feature_importances_))
        }

        # Cross-validation
        cv_scores = cross_val_score(self.model, X_train_scaled, y_train, cv=5)
        metrics['cv_scores'] = cv_scores
        metrics['cv_mean'] = cv_scores.mean()
        metrics['cv_std'] = cv_scores.std()

        # Store for later use
        self.X_test = X_test_scaled
        self.y_test = y_test
        self.y_test_proba = y_test_proba

        print("\n" + "=" * 50)
        print("MODEL PERFORMANCE")
        print("=" * 50)
        print(f"Training Accuracy: {metrics['train_accuracy']:.4f}")
        print(f"Test Accuracy: {metrics['test_accuracy']:.4f}")
        print(f"Precision: {metrics['precision']:.4f}")
        print(f"Recall: {metrics['recall']:.4f}")
        print(f"F1-Score: {metrics['f1_score']:.4f}")
        print(f"ROC-AUC: {metrics['roc_auc']:.4f}")
        print(f"Cross-Validation Accuracy: {metrics['cv_mean']:.4f} (+/- {metrics['cv_std']:.4f})")
        print("\nClassification Report:")
        print(metrics['classification_report'])
        print("=" * 50)

        return metrics

    def plot_results(self, metrics: Dict, save_dir: str = 'ml_results'):
        """
        Generate visualization plots

        Args:
            metrics: Dictionary with evaluation metrics
            save_dir: Directory to save plots
        """
        os.makedirs(save_dir, exist_ok=True)

        # 1. Confusion Matrix
        plt.figure(figsize=(8, 6))
        sns.heatmap(metrics['confusion_matrix'], annot=True, fmt='d', cmap='Blues',
                    xticklabels=['Red Win', 'Blue Win'],
                    yticklabels=['Red Win', 'Blue Win'])
        plt.title('Match Outcome Prediction - Confusion Matrix', fontsize=14, fontweight='bold')
        plt.ylabel('Actual')
        plt.xlabel('Predicted')
        plt.tight_layout()
        plt.savefig(os.path.join(save_dir, 'match_prediction_confusion_matrix.png'), dpi=300)
        plt.close()

        # 2. Feature Importance
        feature_imp = pd.DataFrame({
            'feature': list(metrics['feature_importance'].keys()),
            'importance': list(metrics['feature_importance'].values())
        }).sort_values('importance', ascending=False).head(15)

        plt.figure(figsize=(10, 8))
        sns.barplot(data=feature_imp, y='feature', x='importance', palette='viridis')
        plt.title('Top 15 Feature Importances - Match Prediction', fontsize=14, fontweight='bold')
        plt.xlabel('Importance Score')
        plt.ylabel('Feature')
        plt.tight_layout()
        plt.savefig(os.path.join(save_dir, 'match_prediction_feature_importance.png'), dpi=300)
        plt.close()

        # 3. ROC Curve
        fpr, tpr, thresholds = roc_curve(self.y_test, self.y_test_proba)

        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2,
                label=f'ROC curve (AUC = {metrics["roc_auc"]:.4f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Classifier')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic (ROC) Curve', fontsize=14, fontweight='bold')
        plt.legend(loc="lower right")
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(save_dir, 'match_prediction_roc_curve.png'), dpi=300)
        plt.close()

        # 4. Model Performance Metrics
        metrics_data = {
            'Metric': ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC'],
            'Score': [
                metrics['test_accuracy'],
                metrics['precision'],
                metrics['recall'],
                metrics['f1_score'],
                metrics['roc_auc']
            ]
        }
        metrics_df = pd.DataFrame(metrics_data)

        plt.figure(figsize=(10, 6))
        sns.barplot(data=metrics_df, x='Metric', y='Score', palette='Set2')
        plt.title('Match Outcome Prediction - Performance Metrics', fontsize=14, fontweight='bold')
        plt.ylabel('Score')
        plt.ylim(0, 1)
        for i, v in enumerate(metrics_df['Score']):
            plt.text(i, v + 0.02, f'{v:.4f}', ha='center', va='bottom', fontweight='bold')
        plt.tight_layout()
        plt.savefig(os.path.join(save_dir, 'match_prediction_metrics.png'), dpi=300)
        plt.close()

        print(f"Plots saved to {save_dir}/")

    def save_model(self, path: str = 'ml_models/saved_models/match_predictor.pkl'):
        """Save the trained model"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'feature_names': self.feature_names
        }, path)
        print(f"Model saved to {path}")

    def load_model(self, path: str = 'ml_models/saved_models/match_predictor.pkl'):
        """Load a trained model"""
        data = joblib.load(path)
        self.model = data['model']
        self.scaler = data['scaler']
        self.feature_names = data['feature_names']
        self.is_trained = True
        print(f"Model loaded from {path}")

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Make predictions on new data"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")

        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """Get prediction probabilities"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")

        X_scaled = self.scaler.transform(X)
        return self.model.predict_proba(X_scaled)
