import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "corporate_expense_data.csv")

DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "finance_dataset_modified_432_rows.csv")

MODEL_DIR = os.path.join(BASE_DIR, "models")

GROUP_COLUMNS = ["expense_type", "expense_category"]

FEATURE_COLUMNS = [
    "growth_lag_1",
    "growth_lag_3",
    "rolling_growth_3"
]

TARGET_COLUMN = "growth_rate"
