"""
Game Duration Prediction Model
Predicts match duration based on game statistics
Uses Random Forest Regression
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, r2_score,
    mean_absolute_percentage_error
)
from sklearn.preprocessing import StandardScaler
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Tuple
import os


class GameDurationPredictor:
    """Predicts game duration using Random Forest Regression"""

    def __init__(self):
        """Initialize the model"""
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        self.baseline_model = LinearRegression()
        self.scaler = StandardScaler()
        self.feature_names = None
        self.is_trained = False

    def prepare_features(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Prepare features and target from dataframe

        Args:
            df: DataFrame with match data

        Returns:
            Tuple of (features, target - game duration in minutes)
        """
        # Select feature columns
        feature_cols = [
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
            'tower_diff', 'dragon_diff',
            'total_kills', 'total_objectives'
        ]

        X = df[feature_cols].copy()
        # Convert duration from seconds to minutes
        y = df['gameDuration'] / 60.0

        self.feature_names = feature_cols

        return X, y

    def train(self, X: pd.DataFrame, y: pd.Series, test_size: float = 0.2) -> Dict:
        """
        Train the model and return evaluation metrics

        Args:
            X: Feature DataFrame
            y: Target Series (game duration in minutes)
            test_size: Proportion of data for testing

        Returns:
            Dictionary with evaluation metrics
        """
        print("Training Game Duration Prediction Model...")
        print(f"Dataset size: {len(X)} samples")
        print(f"Duration range: {y.min():.1f} - {y.max():.1f} minutes")
        print(f"Average duration: {y.mean():.1f} minutes")

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )

        print(f"Training set: {len(X_train)} samples")
        print(f"Test set: {len(X_test)} samples")

        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # Train Random Forest model
        print("Training Random Forest model...")
        self.model.fit(X_train_scaled, y_train)

        # Train baseline Linear Regression model for comparison
        print("Training baseline Linear Regression model...")
        self.baseline_model.fit(X_train_scaled, y_train)

        self.is_trained = True

        # Make predictions
        y_train_pred = self.model.predict(X_train_scaled)
        y_test_pred = self.model.predict(X_test_scaled)

        y_test_pred_baseline = self.baseline_model.predict(X_test_scaled)

        # Calculate metrics for Random Forest
        train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
        test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
        test_mae = mean_absolute_error(y_test, y_test_pred)
        test_r2 = r2_score(y_test, y_test_pred)
        test_mape = mean_absolute_percentage_error(y_test, y_test_pred)

        # Calculate metrics for baseline
        baseline_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred_baseline))
        baseline_mae = mean_absolute_error(y_test, y_test_pred_baseline)
        baseline_r2 = r2_score(y_test, y_test_pred_baseline)

        metrics = {
            'train_rmse': train_rmse,
            'test_rmse': test_rmse,
            'test_mae': test_mae,
            'test_r2': test_r2,
            'test_mape': test_mape,
            'baseline_rmse': baseline_rmse,
            'baseline_mae': baseline_mae,
            'baseline_r2': baseline_r2,
            'feature_importance': dict(zip(self.feature_names, self.model.feature_importances_))
        }

        # Cross-validation
        cv_scores = cross_val_score(
            self.model, X_train_scaled, y_train,
            cv=5, scoring='neg_root_mean_squared_error'
        )
        metrics['cv_rmse'] = -cv_scores
        metrics['cv_rmse_mean'] = -cv_scores.mean()
        metrics['cv_rmse_std'] = cv_scores.std()

        # Store for plotting
        self.y_test = y_test
        self.y_test_pred = y_test_pred
        self.y_test_pred_baseline = y_test_pred_baseline

        print("\n" + "=" * 50)
        print("MODEL PERFORMANCE - RANDOM FOREST")
        print("=" * 50)
        print(f"Training RMSE: {train_rmse:.2f} minutes")
        print(f"Test RMSE: {test_rmse:.2f} minutes")
        print(f"Test MAE: {test_mae:.2f} minutes")
        print(f"Test R² Score: {test_r2:.4f}")
        print(f"Test MAPE: {test_mape:.4f}")
        print(f"Cross-Validation RMSE: {metrics['cv_rmse_mean']:.2f} (+/- {metrics['cv_rmse_std']:.2f})")
        print("\n" + "=" * 50)
        print("BASELINE MODEL - LINEAR REGRESSION")
        print("=" * 50)
        print(f"Baseline RMSE: {baseline_rmse:.2f} minutes")
        print(f"Baseline MAE: {baseline_mae:.2f} minutes")
        print(f"Baseline R² Score: {baseline_r2:.4f}")
        print(f"\nImprovement over baseline: {((baseline_rmse - test_rmse) / baseline_rmse * 100):.2f}%")
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

        # 1. Actual vs Predicted
        plt.figure(figsize=(10, 8))
        plt.scatter(self.y_test, self.y_test_pred, alpha=0.5, s=20, label='Random Forest')
        plt.scatter(self.y_test, self.y_test_pred_baseline, alpha=0.3, s=10,
                   label='Linear Regression', color='orange')

        # Perfect prediction line
        min_val = min(self.y_test.min(), self.y_test_pred.min())
        max_val = max(self.y_test.max(), self.y_test_pred.max())
        plt.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfect Prediction')

        plt.xlabel('Actual Duration (minutes)', fontsize=12)
        plt.ylabel('Predicted Duration (minutes)', fontsize=12)
        plt.title('Game Duration Prediction - Actual vs Predicted', fontsize=14, fontweight='bold')
        plt.legend()
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(save_dir, 'duration_prediction_scatter.png'), dpi=300)
        plt.close()

        # 2. Residuals Plot
        residuals = self.y_test - self.y_test_pred

        plt.figure(figsize=(10, 6))
        plt.scatter(self.y_test_pred, residuals, alpha=0.5, s=20)
        plt.axhline(y=0, color='r', linestyle='--', lw=2)
        plt.xlabel('Predicted Duration (minutes)')
        plt.ylabel('Residuals (minutes)')
        plt.title('Residual Plot - Game Duration Prediction', fontsize=14, fontweight='bold')
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(save_dir, 'duration_prediction_residuals.png'), dpi=300)
        plt.close()

        # 3. Residuals Distribution
        plt.figure(figsize=(10, 6))
        plt.hist(residuals, bins=50, edgecolor='black', alpha=0.7)
        plt.axvline(x=0, color='r', linestyle='--', lw=2)
        plt.xlabel('Residual (minutes)')
        plt.ylabel('Frequency')
        plt.title('Distribution of Prediction Errors', fontsize=14, fontweight='bold')
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(save_dir, 'duration_prediction_residuals_dist.png'), dpi=300)
        plt.close()

        # 4. Feature Importance
        feature_imp = pd.DataFrame({
            'feature': list(metrics['feature_importance'].keys()),
            'importance': list(metrics['feature_importance'].values())
        }).sort_values('importance', ascending=False).head(15)

        plt.figure(figsize=(10, 8))
        sns.barplot(data=feature_imp, y='feature', x='importance', palette='viridis')
        plt.title('Top 15 Feature Importances - Duration Prediction', fontsize=14, fontweight='bold')
        plt.xlabel('Importance Score')
        plt.ylabel('Feature')
        plt.tight_layout()
        plt.savefig(os.path.join(save_dir, 'duration_prediction_feature_importance.png'), dpi=300)
        plt.close()

        # 5. Model Comparison
        comparison_data = {
            'Model': ['Random Forest', 'Linear Regression'],
            'RMSE': [metrics['test_rmse'], metrics['baseline_rmse']],
            'MAE': [metrics['test_mae'], metrics['baseline_mae']],
            'R²': [metrics['test_r2'], metrics['baseline_r2']]
        }

        fig, axes = plt.subplots(1, 3, figsize=(15, 5))

        # RMSE comparison
        axes[0].bar(comparison_data['Model'], comparison_data['RMSE'],
                   color=['steelblue', 'orange'])
        axes[0].set_ylabel('RMSE (minutes)')
        axes[0].set_title('Root Mean Squared Error', fontweight='bold')
        axes[0].grid(axis='y', alpha=0.3)
        for i, v in enumerate(comparison_data['RMSE']):
            axes[0].text(i, v + 0.1, f'{v:.2f}', ha='center', va='bottom', fontweight='bold')

        # MAE comparison
        axes[1].bar(comparison_data['Model'], comparison_data['MAE'],
                   color=['steelblue', 'orange'])
        axes[1].set_ylabel('MAE (minutes)')
        axes[1].set_title('Mean Absolute Error', fontweight='bold')
        axes[1].grid(axis='y', alpha=0.3)
        for i, v in enumerate(comparison_data['MAE']):
            axes[1].text(i, v + 0.1, f'{v:.2f}', ha='center', va='bottom', fontweight='bold')

        # R² comparison
        axes[2].bar(comparison_data['Model'], comparison_data['R²'],
                   color=['steelblue', 'orange'])
        axes[2].set_ylabel('R² Score')
        axes[2].set_title('R² Score', fontweight='bold')
        axes[2].set_ylim(0, 1)
        axes[2].grid(axis='y', alpha=0.3)
        for i, v in enumerate(comparison_data['R²']):
            axes[2].text(i, v + 0.02, f'{v:.4f}', ha='center', va='bottom', fontweight='bold')

        plt.suptitle('Model Comparison - Duration Prediction', fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.savefig(os.path.join(save_dir, 'duration_prediction_comparison.png'), dpi=300)
        plt.close()

        # 6. Error Analysis by Duration Range
        y_test_array = np.array(self.y_test)
        errors = np.abs(residuals)

        duration_ranges = [(0, 20), (20, 25), (25, 30), (30, 35), (35, 100)]
        range_labels = ['<20', '20-25', '25-30', '30-35', '35+']
        avg_errors = []

        for min_dur, max_dur in duration_ranges:
            mask = (y_test_array >= min_dur) & (y_test_array < max_dur)
            if mask.sum() > 0:
                avg_errors.append(errors[mask].mean())
            else:
                avg_errors.append(0)

        plt.figure(figsize=(10, 6))
        plt.bar(range_labels, avg_errors, color='coral', edgecolor='black')
        plt.xlabel('Game Duration Range (minutes)')
        plt.ylabel('Average Absolute Error (minutes)')
        plt.title('Prediction Error by Game Duration Range', fontsize=14, fontweight='bold')
        plt.grid(axis='y', alpha=0.3)
        for i, v in enumerate(avg_errors):
            plt.text(i, v + 0.05, f'{v:.2f}', ha='center', va='bottom', fontweight='bold')
        plt.tight_layout()
        plt.savefig(os.path.join(save_dir, 'duration_prediction_error_by_range.png'), dpi=300)
        plt.close()

        print(f"Duration prediction plots saved to {save_dir}/")

    def save_model(self, path: str = 'ml_models/saved_models/duration_predictor.pkl'):
        """Save the trained model"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump({
            'model': self.model,
            'baseline_model': self.baseline_model,
            'scaler': self.scaler,
            'feature_names': self.feature_names
        }, path)
        print(f"Model saved to {path}")

    def load_model(self, path: str = 'ml_models/saved_models/duration_predictor.pkl'):
        """Load a trained model"""
        data = joblib.load(path)
        self.model = data['model']
        self.baseline_model = data['baseline_model']
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
