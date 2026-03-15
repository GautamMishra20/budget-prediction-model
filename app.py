import streamlit as st
import pandas as pd
import joblib
import os
import plotly.graph_objects as go
from src.config import MODEL_DIR

st.set_page_config(page_title="Enterprise Budget BI Dashboard", layout="wide")

# ------------------------------------------------
# MODEL SELECTION LOGIC
# ------------------------------------------------
def get_models(expense_type, expense_category):
    types = ["Vendor", "Reimbursement"] if expense_type == "Both" else [expense_type]
    categories = ["Planned", "Unplanned"] if expense_category == "Both" else [expense_category]
    return [(t, c) for t in types for c in categories]

# ------------------------------------------------
# CSS
# ------------------------------------------------
st.markdown("""
<style>
.main { background-color: #f4f6f9; }

.kpi-card {
    padding: 25px;
    border-radius: 14px;
    background: white;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    margin-bottom: 15px;
}

.kpi-title { font-size: 14px; color: #6b7280; }
.kpi-value { font-size: 28px; font-weight: 700; margin-top: 5px; color: #111827; }

div.stButton > button {
    background: linear-gradient(90deg, #111827, #374151);
    color: white;
    border-radius: 8px;
    height: 3em;
    width: 100%;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# HEADER
# ------------------------------------------------
st.title("📊 Budget Forecast Dashboard")
st.caption("Enterprise Financial Analytics")
st.markdown("---")

# ------------------------------------------------
# SIDEBAR INPUTS
# ------------------------------------------------
st.sidebar.header("Filters")

expense_type = st.sidebar.selectbox(
    "Expense Type",
    ["Vendor", "Reimbursement", "Both"]
)

expense_category = st.sidebar.selectbox(
    "Expense Category",
    ["Planned", "Unplanned", "Both"]
)

st.sidebar.markdown("### Last 4 Months Budget")

month_1 = st.sidebar.number_input("Last Month Budget", min_value=0.0)
month_2 = st.sidebar.number_input("2 Months Ago", min_value=0.0)
month_3 = st.sidebar.number_input("3 Months Ago", min_value=0.0)
month_4 = st.sidebar.number_input("4 Months Ago", min_value=0.0)

generate = st.sidebar.button("Generate Forecast")

# ------------------------------------------------
# MAIN DASHBOARD
# ------------------------------------------------
if generate:

    if 0 in [month_1, month_2, month_3, month_4]:
        st.warning("Please enter all 4 months budget values.")
    else:

        # ------------------------------------------------
        # FEATURE ENGINEERING
        # ------------------------------------------------
        growth_1 = (month_1 - month_2) / month_2
        growth_2 = (month_2 - month_3) / month_3
        growth_3 = (month_3 - month_4) / month_4

        rolling_growth_3 = (growth_1 + growth_2 + growth_3) / 3

        selected_models = get_models(expense_type, expense_category)

        total_growth = 0
        model_count = 0
        export_rows = []

        # ------------------------------------------------
        # MODEL PREDICTIONS (HIDDEN FROM UI)
        # ------------------------------------------------
        for t, c in selected_models:

            model_name = f"{t}_{c}_model.pkl"
            model_path = os.path.join(MODEL_DIR, model_name)

            if not os.path.exists(model_path):
                continue

            model = joblib.load(model_path)

            input_data = pd.DataFrame([{
                "growth_lag_1": growth_1,
                "growth_lag_3": growth_3,
                "rolling_growth_3": rolling_growth_3
            }])

            predicted_growth = model.predict(input_data)[0]

            total_growth += predicted_growth
            model_count += 1

            export_rows.append({
                "Expense Type": t,
                "Expense Category": c,
                "Predicted Growth (%)": round(predicted_growth * 100, 2)
            })

        # ------------------------------------------------
        # FINAL FORECAST
        # ------------------------------------------------
        avg_growth = total_growth / model_count
        next_budget = month_1 * (1 + avg_growth)

        st.subheader("Final Forecast")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Average Predicted Growth", f"{avg_growth*100:.2f}%")

        with col2:
            st.metric("Forecast Budget (₹)", f"₹ {next_budget:,.2f}")

        # ------------------------------------------------
        # TREND CHART
        # ------------------------------------------------
        months = ["M-4", "M-3", "M-2", "M-1", "Forecast"]
        values = [month_4, month_3, month_2, month_1, next_budget]

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=months,
            y=values,
            mode="lines+markers",
            line=dict(width=4)
        ))

        fig.update_layout(
            template="plotly_white",
            height=450,
            xaxis_title="Timeline",
            yaxis_title="Budget (₹)"
        )

        st.plotly_chart(fig, use_container_width=True)

        # ------------------------------------------------
        # EXPORT CSV
        # ------------------------------------------------
        export_df = pd.DataFrame(export_rows)

        export_df.loc[len(export_df)] = [
            "Combined",
            "All Selected",
            round(avg_growth * 100, 2)
        ]

        csv = export_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Forecast as CSV",
            data=csv,
            file_name="budget_forecast.csv",
            mime="text/csv"
        )

else:
    st.info("Select filters and enter budget to generate forecast.")