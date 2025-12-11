# Machine Learning Models - Evaluation Report

**Generated:** 2025-12-06 02:32:27

---

## 1. Match Outcome Prediction (Classification)

### Model: Random Forest Classifier

**Objective:** Predict which team (Blue or Red) will win the match based on in-game statistics.

### Performance Metrics

| Metric | Score |
|--------|-------|
| Test Accuracy | 0.9835 |
| Precision | 0.9842 |
| Recall | 0.9832 |
| F1-Score | 0.9837 |
| ROC-AUC | 0.9990 |
| Cross-Validation Accuracy | 0.9826 (+/- 0.0020) |

### Top 10 Most Important Features

| Feature | Importance |
|---------|------------|
| gold_diff | 0.3377 |
| tower_diff | 0.1588 |
| kills_diff | 0.1056 |
| red_towers | 0.0961 |
| damage_diff | 0.0760 |
| blue_towers | 0.0619 |
| dragon_diff | 0.0253 |
| red_kills | 0.0180 |
| blue_dragons | 0.0149 |
| red_dragons | 0.0126 |

### Visualizations

- Confusion Matrix: `match_prediction_confusion_matrix.png`
- Feature Importance: `match_prediction_feature_importance.png`
- ROC Curve: `match_prediction_roc_curve.png`
- Performance Metrics: `match_prediction_metrics.png`

---

## 2. Champion Clustering (Unsupervised Learning)

### Model: K-Means Clustering

**Objective:** Group champions into distinct playstyle categories based on performance statistics.

---

## 3. Game Duration Prediction (Regression)

### Model: Random Forest Regressor

**Objective:** Predict the duration of a match based on in-game statistics.

### Performance Metrics

| Metric | Random Forest | Linear Regression (Baseline) |
|--------|---------------|-------------------------------|
| RMSE (minutes) | 1.02 | 0.98 |
| MAE (minutes) | 0.77 | 0.76 |
| R² Score | 0.9836 | 0.9848 |
| MAPE | 0.0262 | - |
| CV RMSE | 1.07 (+/- 0.04) | - |

**Improvement over baseline:** -3.92%

### Top 10 Most Important Features

| Feature | Importance |
|---------|------------|
| total_objectives | 0.7079 |
| red_gold | 0.1017 |
| blue_cs | 0.0827 |
| blue_gold | 0.0478 |
| red_cs | 0.0314 |
| red_damage | 0.0124 |
| blue_damage | 0.0054 |
| total_kills | 0.0019 |
| gold_diff | 0.0009 |
| red_assists | 0.0009 |

### Visualizations

- Actual vs Predicted: `duration_prediction_scatter.png`
- Residuals Plot: `duration_prediction_residuals.png`
- Residuals Distribution: `duration_prediction_residuals_dist.png`
- Feature Importance: `duration_prediction_feature_importance.png`
- Model Comparison: `duration_prediction_comparison.png`
- Error by Duration Range: `duration_prediction_error_by_range.png`

---

## Summary

This project successfully implemented three machine learning models:

1. **Classification Model:** Accurately predicts match outcomes with high precision
2. **Clustering Model:** Identifies distinct champion playstyle archetypes
3. **Regression Model:** Predicts game duration with reasonable accuracy

All models were evaluated using appropriate metrics and visualizations.
