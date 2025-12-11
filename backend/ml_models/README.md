## Machine Learning Models

This directory contains three machine learning models for analyzing League of Legends match data.

---

## Models Implemented

### 1. Match Outcome Prediction (Classification)
**File:** `match_prediction.py`
**Algorithm:** Random Forest Classifier
**Objective:** Predict which team (Blue or Red) will win based on in-game statistics

**Features used:**
- Team statistics (kills, deaths, assists, gold, damage, CS)
- Objective control (barons, dragons, towers)
- Team performance differences

**Metrics:**
- Accuracy
- Precision, Recall, F1-Score
- ROC-AUC
- Confusion Matrix
- 5-Fold Cross-Validation

---

### 2. Champion Clustering (Unsupervised Learning)
**File:** `champion_clustering.py`
**Algorithm:** K-Means Clustering
**Objective:** Group champions into distinct playstyle archetypes

**Features used:**
- Win rate
- KDA statistics
- Gold and damage output
- CS and vision score
- Damage taken

**Metrics:**
- Silhouette Score
- Davies-Bouldin Score
- Calinski-Harabasz Score
- PCA visualization

**Archetypes identified:**
- Assassin/High Damage Carry
- Tank/Frontline
- Support/Utility
- Farming Carry
- Balanced Fighter
- Versatile/Mixed

---

### 3. Game Duration Prediction (Regression)
**File:** `duration_prediction.py`
**Algorithm:** Random Forest Regressor
**Objective:** Predict match duration in minutes

**Features used:**
- Team kills, deaths, assists
- Gold and damage statistics
- CS and objective control
- Game pace indicators

**Metrics:**
- RMSE (Root Mean Squared Error)
- MAE (Mean Absolute Error)
- R² Score
- MAPE (Mean Absolute Percentage Error)
- Comparison with Linear Regression baseline

---

## Setup and Installation

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

Required packages:
- scikit-learn >= 1.3.0
- matplotlib >= 3.7.0
- seaborn >= 0.12.0
- joblib >= 1.3.0
- pandas >= 2.2.0
- numpy >= 1.26.0
- pymongo >= 4.6.1

### 2. Ensure MongoDB is Running

Make sure MongoDB is running with your League of Legends data loaded.

```bash
# Check if MongoDB is running
# Windows: Check Services
# Mac/Linux: sudo systemctl status mongod
```

---

## How to Train Models

### Option 1: Train All Models at Once (Recommended)

```bash
cd backend
python ml_models/train_all_models.py
```

This will:
1. Train all three models
2. Generate evaluation metrics
3. Create visualization plots
4. Save trained models
5. Generate a comprehensive ML_REPORT.md

**Estimated time:** 5-15 minutes (depending on dataset size and computer speed)

### Option 2: Train Individual Models

#### Match Outcome Prediction
```python
from ml_models.data_preprocessor import DataPreprocessor
from ml_models.match_prediction import MatchOutcomePredictor

# Load data
preprocessor = DataPreprocessor()
df = preprocessor.extract_match_features(limit=10000)

# Train model
predictor = MatchOutcomePredictor()
X, y = predictor.prepare_features(df)
metrics = predictor.train(X, y)

# Generate plots
predictor.plot_results(metrics)

# Save model
predictor.save_model()
```

#### Champion Clustering
```python
from ml_models.data_preprocessor import DataPreprocessor
from ml_models.champion_clustering import ChampionClusterer

# Load data
preprocessor = DataPreprocessor()
df = preprocessor.extract_champion_statistics()

# Train model
clusterer = ChampionClusterer(n_clusters=6)
X = clusterer.prepare_features(df)
metrics = clusterer.train(X)

# Generate plots
clusterer.plot_results(metrics)

# Save model and cluster assignments
clusterer.save_model()
cluster_summary = clusterer.get_cluster_summary()
cluster_summary.to_csv('champion_clusters.csv')
```

#### Game Duration Prediction
```python
from ml_models.data_preprocessor import DataPreprocessor
from ml_models.duration_prediction import GameDurationPredictor

# Load data
preprocessor = DataPreprocessor()
df = preprocessor.extract_duration_features(limit=10000)

# Train model
predictor = GameDurationPredictor()
X, y = predictor.prepare_features(df)
metrics = predictor.train(X, y)

# Generate plots
predictor.plot_results(metrics)

# Save model
predictor.save_model()
```

---

## Output Files

After training, the following files will be generated:

### Trained Models
- `ml_models/saved_models/match_predictor.pkl`
- `ml_models/saved_models/champion_clusterer.pkl`
- `ml_models/saved_models/duration_predictor.pkl`

### Visualizations (in `ml_results/`)

**Match Prediction:**
- `match_prediction_confusion_matrix.png`
- `match_prediction_feature_importance.png`
- `match_prediction_roc_curve.png`
- `match_prediction_metrics.png`

**Champion Clustering:**
- `champion_clustering_pca.png`
- `champion_clustering_sizes.png`
- `champion_clustering_heatmap.png`
- `champion_clustering_radar.png`
- `clustering_optimal_k.png`

**Duration Prediction:**
- `duration_prediction_scatter.png`
- `duration_prediction_residuals.png`
- `duration_prediction_residuals_dist.png`
- `duration_prediction_feature_importance.png`
- `duration_prediction_comparison.png`
- `duration_prediction_error_by_range.png`

### Reports
- `ml_results/ML_REPORT.md` - Comprehensive markdown report
- `ml_results/results_summary.json` - JSON with all metrics
- `ml_results/champion_clusters.csv` - Champion cluster assignments

---

## Using Trained Models

### Load and Use for Predictions

```python
from ml_models.match_prediction import MatchOutcomePredictor
import pandas as pd

# Load trained model
predictor = MatchOutcomePredictor()
predictor.load_model('ml_models/saved_models/match_predictor.pkl')

# Prepare new data (same features as training)
new_data = pd.DataFrame({
    'blue_kills': [25],
    'red_kills': [18],
    # ... all other features
})

# Make prediction
prediction = predictor.predict(new_data)
probabilities = predictor.predict_proba(new_data)

print(f"Predicted winner: {'Blue' if prediction[0] == 1 else 'Red'}")
print(f"Confidence: {probabilities[0][prediction[0]]:.2%}")
```

---

## Model Performance Summary

### Match Outcome Prediction
- **Expected Accuracy:** 90-95%
- **ROC-AUC:** > 0.95
- **Key Features:** Gold difference, tower difference, kills difference

### Champion Clustering
- **Clusters:** 6 distinct archetypes
- **Silhouette Score:** 0.3-0.5 (moderate separation)
- **Champions per cluster:** 20-40

### Game Duration Prediction
- **Expected RMSE:** 2-3 minutes
- **R² Score:** 0.7-0.85
- **Improvement over baseline:** 15-25%

---

## Troubleshooting

### Issue: ModuleNotFoundError
```bash
# Make sure you're in the backend directory
cd backend
python -m ml_models.train_all_models
```

### Issue: MongoDB Connection Error
```python
# Check your .env file or update connection string
MONGO_URI=mongodb://localhost:27017/
```

### Issue: Out of Memory
```python
# Reduce the limit parameter when extracting data
match_df = preprocessor.extract_match_features(limit=5000)  # Instead of 10000
```

### Issue: Slow Training
- Use fewer samples with the `limit` parameter
- Reduce `n_estimators` in Random Forest models
- Use a smaller number of clusters for K-Means

---

## Model Architecture

### Data Flow
```
MongoDB
   ↓
DataPreprocessor (extract features)
   ↓
Feature Engineering (scaling, transformations)
   ↓
Train/Test Split
   ↓
Model Training (Random Forest, K-Means)
   ↓
Evaluation (metrics, cross-validation)
   ↓
Visualization (plots, charts)
   ↓
Save Models & Reports
```

---

## Next Steps

1. **Integrate with API:** Create Flask endpoints to serve predictions
2. **Hyperparameter Tuning:** Use GridSearchCV for optimization
3. **Feature Engineering:** Add more derived features
4. **Deep Learning:** Experiment with neural networks
5. **Real-time Predictions:** Implement streaming predictions

---

## References

- Scikit-learn Documentation: https://scikit-learn.org/
- Random Forest Algorithm: https://scikit-learn.org/stable/modules/ensemble.html#forest
- K-Means Clustering: https://scikit-learn.org/stable/modules/clustering.html#k-means

---

## Authors

League of Legends Analytics Project
Date: 2025

---

For questions or issues, please refer to the main project README.
