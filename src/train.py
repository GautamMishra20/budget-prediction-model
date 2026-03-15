import os
import joblib
import pandas as pd
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error
from src.config import DATA_PATH, MODEL_DIR, FEATURE_COLUMNS, TARGET_COLUMN, GROUP_COLUMNS
from src.feature_engineering import create_features

def train_models():

    df = pd.read_csv(DATA_PATH)
    df["date"] = pd.to_datetime(df["date"])
    df = create_features(df)

    os.makedirs(MODEL_DIR, exist_ok=True)

    for (etype, ecat), group in df.groupby(GROUP_COLUMNS):

        train = group[group["year"] < 2024]
        test = group[group["year"] == 2024]

        X_train = train[FEATURE_COLUMNS]
        y_train = train[TARGET_COLUMN]

        X_test = test[FEATURE_COLUMNS]
        y_test = test[TARGET_COLUMN]

        model = XGBRegressor(
            n_estimators=300,
            learning_rate=0.05,
            max_depth=4,
            random_state=42
        )

        model.fit(X_train, y_train)

        preds = model.predict(X_test)
        error = mean_absolute_error(y_test, preds)

        print(f"{etype} - {ecat} MAE:", round(error,2))

        model_name = f"{etype}_{ecat}_model.pkl"
        joblib.dump(model, os.path.join(MODEL_DIR, model_name))

    print("Models trained and saved.")