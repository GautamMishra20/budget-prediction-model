import os
import joblib
import pandas as pd
from src.config import DATA_PATH, MODEL_DIR, FEATURE_COLUMNS, GROUP_COLUMNS
from src.feature_engineering import create_features

def predict_next_month():

    df = pd.read_csv(DATA_PATH)
    df["date"] = pd.to_datetime(df["date"])
    df = create_features(df)

    latest_date = df["date"].max()
    latest_data = df[df["date"] == latest_date]

    predictions = []

    for (etype, ecat), group in latest_data.groupby(GROUP_COLUMNS):

        model_name = f"{etype}_{ecat}_model.pkl"
        model_path = os.path.join(MODEL_DIR, model_name)

        model = joblib.load(model_path)

        X_latest = group[FEATURE_COLUMNS]
        prediction = model.predict(X_latest)[0]

        predictions.append({
            "expense_type": etype,
            "expense_category": ecat,
            "predicted_next_month_budget": round(prediction,2)
        })

    return pd.DataFrame(predictions)