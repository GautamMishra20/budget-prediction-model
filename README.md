# 📊 Budget Forecasting System 

## 🚀 Overview

This project is an enterprise-style financial forecasting system that predicts **next month’s budget** for different expense segments using machine learning.

Unlike traditional models that predict raw budget values, this system predicts **growth rate**, making it robust and scale-independent across companies of different sizes.

The system includes:

- Synthetic financial data generation  
- Growth-based feature engineering  
- Segment-wise machine learning models  
- Time-aware validation  
- Enterprise-level Streamlit dashboard  

---

## 🎯 Business Objective

Predict next month’s budget for:

- Vendor – Planned  
- Vendor – Unplanned  
- Reimbursement – Planned  
- Reimbursement – Unplanned  

The system models **budget growth behavior**, not absolute values.

---

## 🧠 Why Growth-Based Modeling?

Traditional forecasting models predict raw numbers, which causes scale mismatch issues when input data differs from training data.

This system predicts:

Growth Rate = (Current Budget - Previous Budget) / Previous Budget

Then calculates:

Next Month Budget = Last Month Budget × (1 + Predicted Growth)

### ✅ Benefits

- Works for small and large companies  
- Eliminates magnitude bias  
- Captures financial behavior patterns  
- More realistic financial modeling  
- Robust to scale differences  

---

## 🏗 Project Structure

finance_budget_forecasting/
│
├── data/
│   └── raw/
│
├── models/
│
├── src/
│   ├── config.py
│   ├── data_generator.py
│   ├── feature_engineering.py
│   ├── train.py
│   └── predict.py
│
├── main_train.py
├── app.py
├── requirements.txt
└── README.md

---

## 📊 Data Generation

Synthetic corporate financial data is generated for:

- 7 years (2018–2024)  
- Monthly frequency  
- Seasonal variation (Q4 boost, Q2 dip)  
- Vendor & Reimbursement segmentation  
- Planned & Unplanned categorization  
- Realistic random financial variation  

This ensures the model learns practical financial behavior.

---

## ⚙ Feature Engineering

Instead of raw budget values, the model uses growth-based features:

- growth_lag_1 → Previous month growth  
- growth_lag_3 → Growth 3 months ago  
- rolling_growth_3 → 3-month rolling growth average  

These features capture:

- Financial momentum  
- Trend stability  
- Acceleration or deceleration  

---

## 🤖 Model Training

- Model Type: XGBoost Regressor  
- Separate model per expense segment  
- Time-aware train/test split  
- Evaluation Metric: Mean Absolute Error (MAE)  

Example training output:

Reimbursement - Planned MAE: 0.12  
Vendor - Planned MAE: 0.14  
Vendor - Unplanned MAE: 0.22  
Reimbursement - Unplanned MAE: 0.26  

Lower MAE indicates better growth prediction accuracy.  
Unplanned expenses show higher error due to natural volatility.

---

## 🖥 Enterprise Dashboard

The Streamlit dashboard allows administrators to:

- Select expense type  
- Select expense category  
- Enter last 4 months budget  
- Generate forecast  
- View:
  - Predicted Growth Rate (%)
  - Predicted Next Month Budget (₹)
  - Mini trend projection chart  

Designed for executive-level financial decision support.

---

## ▶ How To Run The Project

### 1️⃣ Install Dependencies

pip install -r requirements.txt

---

### 2️⃣ Train Models

python main_train.py

This will:
- Generate synthetic dataset  
- Train 4 ML models  
- Save models inside `/models`  

---

### 3️⃣ Launch Dashboard

streamlit run app.py

---

## 📈 Example Scenario

If last 4 months budgets are:

Month -4: 180,000  
Month -3: 190,000  
Month -2: 195,000  
Month -1: 200,000  

The system:

1. Calculates historical growth  
2. Predicts next month growth  
3. Outputs something like:

Predicted Growth Rate: 4.85%  
Predicted Next Month Budget: ₹ 209,700  

---

## 🔍 Key Technical Highlights

- Scale-independent modeling  
- Segment-wise ML models  
- Time-series compliant validation  
- Modular production-ready structure  
- Enterprise UI visualization  
- Clean separation of data, features, training, and inference  

---

## 🛠 Tech Stack

- Python  
- Pandas  
- NumPy  
- XGBoost  
- Scikit-Learn  
- Streamlit  
- Plotly  

---

## 📌 Future Enhancements

- Confidence interval estimation  
- Forecast volatility indicator  
- Automated retraining pipeline  
- Model monitoring & logging  
- REST API deployment  
- Docker containerization  
- Role-based authentication  

---

## 🏆 Project Value

This project demonstrates:

- Financial domain understanding  
- Time-series modeling  
- Growth-based feature engineering  
- Production ML pipeline design  
- Enterprise UI implementation  

Suitable for:

- Data Science roles  
- Financial Analytics roles  
- Machine Learning Engineer roles  
- Business Intelligence roles  

---

Author: Gautam Mishra  
Project Type: Enterprise Financial Forecasting System  

url :- https://budget-prediction-model-h4p4y23uecbwuq45a6ixch.streamlit.app/
