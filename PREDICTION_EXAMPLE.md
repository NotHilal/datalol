# Match Outcome Prediction - Usage Guide

## How the Prediction Works

### Machine Learning Model
- **Algorithm:** Random Forest Classifier (100 trees)
- **Accuracy:** 98.35% on test data
- **Training Data:** 10,000 League of Legends matches
- **Prediction Speed:** ~50ms per prediction

---

## Method 1: Use the Web Interface

### Step 1: Start the Application
```bash
# Terminal 1 - Backend
cd backend
python run.py

# Terminal 2 - Frontend
cd frontend
npm start
```

### Step 2: Navigate to ML Page
- Open browser: `http://localhost:4200/ml`
- Click the **"Make Predictions"** tab

### Step 3: Enter Match Statistics

**Blue Team Stats:**
- Kills: 25
- Deaths: 18
- Assists: 55
- Gold: 65000
- Damage: 140000
- CS: 750
- Barons: 2
- Dragons: 3
- Towers: 9
- Avg Level: 17

**Red Team Stats:**
- Kills: 18
- Deaths: 25
- Assists: 40
- Gold: 55000
- Damage: 110000
- CS: 620
- Barons: 0
- Dragons: 1
- Towers: 3
- Avg Level: 15

### Step 4: Get Prediction
Click **"Predict Winner"** button

**Result:**
```
Predicted Winner: Blue Team
Confidence: 100.0%
```

---

## Method 2: Use the API Directly

### cURL Example
```bash
curl -X POST http://localhost:5000/api/v1/ml/predict/match-outcome \
  -H "Content-Type: application/json" \
  -d '{
    "blue_kills": 25,
    "red_kills": 18,
    "blue_deaths": 18,
    "red_deaths": 25,
    "blue_assists": 55,
    "red_assists": 40,
    "blue_gold": 65000,
    "red_gold": 55000,
    "blue_damage": 140000,
    "red_damage": 110000,
    "blue_cs": 750,
    "red_cs": 620,
    "blue_barons": 2,
    "red_barons": 0,
    "blue_dragons": 3,
    "red_dragons": 1,
    "blue_towers": 9,
    "red_towers": 3,
    "blue_avg_level": 17,
    "red_avg_level": 15
  }'
```

### Response
```json
{
  "success": true,
  "data": {
    "prediction": "Blue Team",
    "predicted_value": 1,
    "confidence": 1.0,
    "probabilities": {
      "red_team": 0.0,
      "blue_team": 1.0
    }
  }
}
```

### Python Example
```python
import requests
import json

url = "http://localhost:5000/api/v1/ml/predict/match-outcome"

match_data = {
    "blue_kills": 25,
    "red_kills": 18,
    "blue_deaths": 18,
    "red_deaths": 25,
    "blue_assists": 55,
    "red_assists": 40,
    "blue_gold": 65000,
    "red_gold": 55000,
    "blue_damage": 140000,
    "red_damage": 110000,
    "blue_cs": 750,
    "red_cs": 620,
    "blue_barons": 2,
    "red_barons": 0,
    "blue_dragons": 3,
    "red_dragons": 1,
    "blue_towers": 9,
    "red_towers": 3,
    "blue_avg_level": 17,
    "red_avg_level": 15
}

response = requests.post(url, json=match_data)
result = response.json()

print(f"Predicted Winner: {result['data']['prediction']}")
print(f"Confidence: {result['data']['confidence'] * 100:.1f}%")
```

---

## Method 3: Use in Python Code

```python
import sys
sys.path.append('backend')

from ml_models.match_prediction import MatchOutcomePredictor
import pandas as pd

# Load the trained model
predictor = MatchOutcomePredictor()
predictor.load_model('backend/ml_models/saved_models/match_predictor.pkl')

# Prepare match data
match_data = pd.DataFrame([{
    'blue_avg_level': 17,
    'red_avg_level': 15,
    'blue_kills': 25,
    'red_kills': 18,
    'blue_deaths': 18,
    'red_deaths': 25,
    'blue_assists': 55,
    'red_assists': 40,
    'blue_gold': 65000,
    'red_gold': 55000,
    'blue_damage': 140000,
    'red_damage': 110000,
    'blue_cs': 750,
    'red_cs': 620,
    'blue_barons': 2,
    'red_barons': 0,
    'blue_dragons': 3,
    'red_dragons': 1,
    'blue_towers': 9,
    'red_towers': 3,
    'gold_diff': 10000,
    'kills_diff': 7,
    'damage_diff': 30000,
    'cs_diff': 130,
    'tower_diff': 6,
    'dragon_diff': 2
}])

# Make prediction
prediction = predictor.predict(match_data)[0]
probabilities = predictor.predict_proba(match_data)[0]

winner = "Blue Team" if prediction == 1 else "Red Team"
confidence = probabilities[prediction] * 100

print(f"Predicted Winner: {winner}")
print(f"Confidence: {confidence:.1f}%")
```

---

## Understanding the Features

### Most Important Features (Feature Importance)

1. **gold_diff (33.77%)** - Gold advantage between teams
   - Positive = Blue ahead
   - Negative = Red ahead
   - Most predictive single feature

2. **tower_diff (15.88%)** - Tower advantage
   - Shows map control
   - Leads to objective access

3. **kills_diff (10.56%)** - Kill advantage
   - Indicates team fight performance
   - Correlates with gold advantage

4. **blue_gold (7.12%)** - Blue team total gold
   - Absolute values matter too
   - Higher gold = better items

5. **red_gold (6.85%)** - Red team total gold

6. **damage_diff (5.92%)** - Damage output difference

### Required Statistics

All values should be from the **same point in the game** (e.g., at 20 minutes, or end of game):

**Team Statistics:**
- `blue_kills` - Total kills by Blue team
- `blue_deaths` - Total deaths on Blue team
- `blue_assists` - Total assists by Blue team
- `blue_gold` - Total gold earned by Blue team
- `blue_damage` - Total damage dealt by Blue team
- `blue_cs` - Total creep score (minions killed)
- `blue_barons` - Number of Baron Nashors killed
- `blue_dragons` - Number of Dragons killed
- `blue_towers` - Number of enemy towers destroyed
- `blue_avg_level` - Average champion level

(Same fields for Red team with `red_` prefix)

---

## Prediction Scenarios

### Scenario 1: Clear Winner
```
Blue: 30 kills, 80000 gold, 10 towers
Red:  10 kills, 40000 gold, 1 tower
→ Prediction: Blue Team (99.9% confidence)
```

### Scenario 2: Close Match
```
Blue: 20 kills, 55000 gold, 5 towers
Red:  19 kills, 54000 gold, 4 towers
→ Prediction: Blue Team (65% confidence)
```

### Scenario 3: Comeback Potential
```
Blue: 15 kills, 50000 gold, 8 towers
Red:  25 kills, 52000 gold, 7 towers
→ Prediction: Red Team (72% confidence)
```

The model considers ALL features together, not just kills!

---

## Tips for Accurate Predictions

1. **Use consistent timing** - All stats should be from the same moment in the game
2. **Include all fields** - Missing data defaults to 0, which may skew results
3. **Realistic values** - Use actual game statistics, not random numbers
4. **Consider objectives** - Barons, Dragons, and Towers are very important
5. **Gold matters most** - Gold difference is the #1 predictor

---

## Confidence Interpretation

- **90-100%**: Very confident prediction (clear advantage)
- **70-89%**: Confident prediction (moderate advantage)
- **50-69%**: Uncertain prediction (close match)
- **Below 50%**: Model favors the other team

---

## Model Limitations

1. **Doesn't consider champion picks** - Only uses in-game statistics
2. **Doesn't know game context** - Can't see Baron/Elder buffs, item builds
3. **Based on historical data** - Reflects past meta, not current patches
4. **Assumes current state continues** - Can't predict sudden comebacks or throws

---

## Files Involved

### Backend
- `backend/ml_models/match_prediction.py` - Model class
- `backend/ml_models/saved_models/match_predictor.pkl` - Trained model
- `backend/app/routes/ml.py` - API endpoint (line 115-193)

### Frontend
- `frontend/src/app/pages/ml/ml.component.ts` - Prediction interface
- `frontend/src/app/services/ml.service.ts` - API service

---

## Troubleshooting

### Issue: "Model not available" error
**Solution:** Train the model first
```bash
cd backend
python ml_models/train_all_models.py
```

### Issue: "Feature names mismatch" error
**Solution:** Ensure all required fields are included in the request

### Issue: Prediction returns 50% confidence
**Solution:** Check that you're providing realistic match data, not zeros

---

## Next Steps

After getting a prediction, you can:
1. Compare against actual match result
2. Test different scenarios
3. Analyze feature importance
4. View confusion matrix in Visualizations tab
5. Check sample predictions for model performance
