## 🏁 Final Summary: Premier League Match Prediction & Betting Strategy

### 🎯 Project Objective
The goal of this project was to build a machine learning model capable of predicting English Premier League match outcomes and simulating real-world betting strategies based on model predictions. We aimed to evaluate not just accuracy, but profitability through realistic simulations.

---

### 🧠 Models Tested
We experimented with several models:
- **Logistic Regression** (baseline with scaling)
- **Random Forest** (with class balancing)
- **XGBoost (Gradient Boosting)** — tuned & team-encoded

🏆 **Best Model:** Tuned **XGBoost**  
- Accuracy: **54%**
- Best HOME_TEAM recall
- Used for all final simulations

---

### 💸 Betting Strategies Simulated

| Strategy Type        | Matches Bet | Profit | Profit % |
|----------------------|-------------|--------|----------|
| **Flat Strategy (all predictions)** | 100         | –$2,616 | –26.16% |
| **Value Strategy** (`model_prob > implied_prob + 0.05`) | 42 | **+$926** | **+22.05%** ✅ |
| EV Strategy (`expected_value > 0.05`) | 42 | –$391  | –9.31% |
| Hybrid Strategy (Value + EV) | 40 | –$753 | –18.82% |

---

### 📈 Key Takeaways
- Accuracy **alone** doesn’t lead to betting profitability.
- **Simple value-based filtering** of model predictions yielded a **+22% ROI** — outperforming more complex strategies.
- Betting on all matches led to losses, showing the importance of selectivity.
- This project shows that even in noisy environments like sports, a good model with simple logic can outperform the market in narrow windows.

---

### ✅ What's Next?
- Apply this framework across **other seasons** or leagues
- Incorporate live-data APIs and update predictions in real-time
- Explore ensemble models or calibrate probabilities for sharper expected values

---

🧠 Built with Python, Scikit-learn, XGBoost, and a lot of Premier League obsession.
