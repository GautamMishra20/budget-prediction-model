import streamlit as st
import pandas as pd
import joblib
import os
import plotly.graph_objects as go

MODEL_DIR = "models"

st.set_page_config(page_title="AI Finance Assistant", layout="wide")

st.title("🤖 AI Budget Forecast Assistant")
st.caption("Ask financial forecasting questions interactively")

# -------------------------------
# SESSION STATE
# -------------------------------

if "step" not in st.session_state:
    st.session_state.step = 1

if "expense_type" not in st.session_state:
    st.session_state.expense_type = None

if "expense_category" not in st.session_state:
    st.session_state.expense_category = None


# -------------------------------
# MODEL SELECTION
# -------------------------------

def get_models(expense_type, expense_category):

    types = ["Vendor","Reimbursement"] if expense_type == "Both" else [expense_type]

    categories = ["Planned","Unplanned"] if expense_category == "Both" else [expense_category]

    return [(t,c) for t in types for c in categories]


# -------------------------------
# STEP 1
# -------------------------------

if st.session_state.step == 1:

    st.write("### Select Expense Type")

    expense_type = st.selectbox(
        "Expense Type",
        ["Vendor","Reimbursement","Both"]
    )

    if st.button("Next"):

        st.session_state.expense_type = expense_type
        st.session_state.step = 2
        st.rerun()


# -------------------------------
# STEP 2
# -------------------------------

elif st.session_state.step == 2:

    st.write("### Select Expense Category")

    expense_category = st.selectbox(
        "Expense Category",
        ["Planned","Unplanned","Both"]
    )

    if st.button("Next"):

        st.session_state.expense_category = expense_category
        st.session_state.step = 3
        st.rerun()


# -------------------------------
# STEP 3
# -------------------------------

elif st.session_state.step == 3:

    st.write("### Enter Last 4 Months Budget")

    month_1 = st.number_input("Last Month Budget", min_value=0.0)
    month_2 = st.number_input("2 Months Ago", min_value=0.0)
    month_3 = st.number_input("3 Months Ago", min_value=0.0)
    month_4 = st.number_input("4 Months Ago", min_value=0.0)

    if st.button("Generate Forecast"):

        # -------------------------------
        # FEATURE ENGINEERING
        # -------------------------------

        growth_1 = (month_1 - month_2) / month_2
        growth_2 = (month_2 - month_3) / month_3
        growth_3 = (month_3 - month_4) / month_4

        rolling_growth_3 = (growth_1 + growth_2 + growth_3) / 3

        selected_models = get_models(
            st.session_state.expense_type,
            st.session_state.expense_category
        )

        total_growth = 0
        model_count = 0

        for t,c in selected_models:

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

        avg_growth = total_growth / model_count

        next_budget = month_1 * (1 + avg_growth)

        st.markdown("---")

        st.subheader("📊 Forecast Result")

        col1, col2 = st.columns(2)

        col1.metric("Average Growth", f"{avg_growth*100:.2f}%")
        col2.metric("Forecast Budget", f"₹{next_budget:,.2f}")

        # -------------------------------
        # GRAPH
        # -------------------------------

        months = ["M-4","M-3","M-2","M-1","Forecast"]

        values = [month_4,month_3,month_2,month_1,next_budget]

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
            yaxis_title="Budget"
        )

        st.plotly_chart(fig, use_container_width=True)

        # -------------------------------
        # AI INSIGHT
        # -------------------------------

        if avg_growth > 0.08:
            insight = "Budget is rapidly increasing."
        elif avg_growth > 0.03:
            insight = "Budget shows moderate growth."
        else:
            insight = "Budget trend appears stable."

        st.info(f"🧠 AI Insight: {insight}")

        if st.button("Start New Forecast"):

            st.session_state.step = 1
            st.rerun()