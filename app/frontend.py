import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/predict"
st.set_page_config(
    page_title="Credit Risk Predictor",
    page_icon="💳",
    layout="centered"
)

st.title("💳 Credit Risk Predictor")
st.write("Enter the applicant details to predict the probability of serious credit delinquency.")

with st.form("credit_form"):
    st.subheader("Applicant Details")
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input(
            "Age",
            min_value=18,
            max_value=110,
            value=35,
            step=1
        )
        
        monthly_income = st.number_input(
            "Monthly Income",
            min_value=0.0,
            value=5000.0,
            step=100.0,
            help="Enter monthly income in USD ($)"
        )

        income_unknown = st.checkbox(
            "Monthly income is unknown"
        )

        debt_ratio = st.number_input(
            "Debt Ratio",
            min_value=0.0,
            value=0.3,
            step=0.01,
            help="Ratio of monthly debt payments to gross monthly income"
        )

        revolving_utilization = st.number_input(
            "Revolving Utilization",
            min_value=0.0,
            value=0.3,
            step=0.01
        )

        number_of_dependents = st.number_input(
            "Number of Dependents",
            min_value=0,
            value=0,
            step=1
        )

        dependents_unknown = st.checkbox(
            "Number of dependents is unknown"
        )

    with col2:

        open_credit_lines = st.number_input(
            "Open Credit Lines and Loans",
            min_value=0,
            value=5,
            step=1
        )

        real_estate_loans = st.number_input(
            "Real Estate Loans or Lines",
            min_value=0,
            value=1,
            step=1
        )

        past_due_30_59 = st.number_input(
            "Times 30-59 Days Past Due",
            min_value=0,
            value=0,
            step=1
        )

        past_due_60_89 = st.number_input(
            "Times 60-89 Days Past Due",
            min_value=0,
            value=0,
            step=1
        )

        past_due_90 = st.number_input(
            "Times 90+ Days Late",
            min_value=0,
            value=0,
            step=1
        )

    submitted = st.form_submit_button("Predict Risk",use_container_width=True)

if submitted:
    payload = { "RevolvingUtilizationOfUnsecuredLines":revolving_utilization,
        "age":age,
        "NumberOfTime30-59DaysPastDueNotWorse":past_due_30_59,
        "DebtRatio":debt_ratio,
        "MonthlyIncome":None if income_unknown else monthly_income,
        "NumberOfOpenCreditLinesAndLoans":open_credit_lines,
        "NumberOfTimes90DaysLate":past_due_90,
        "NumberRealEstateLoansOrLines":real_estate_loans,
        "NumberOfTime60-89DaysPastDueNotWorse":past_due_60_89,
        "NumberOfDependents":None if dependents_unknown else number_of_dependents
    }
    try:
        with st.spinner("Predicting risk..."):
            response = requests.post(API_URL,json=payload)
            
        response.raise_for_status()
        result = response.json()
        probability = result["default_probability"]
        prediction = result["prediction"]
        risk = result["risk_category"]
        st.subheader("Prediction Result")
        st.metric("Default Probability",f"{probability:.1%}")
        st.write(f"**Risk Category:** {risk}")
        st.progress(min(probability, 1.0))

        if prediction == 1:
            st.warning("⚠️ The applicant is predicted to be at higher risk of serious delinquency.")
        else:
            st.success("✅ The applicant is predicted to be at lower risk of serious delinquency.")

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the FastAPI server, Please start the API first.")
    except requests.exceptions.HTTPError:st.error(f"API Error: {response.text}")
    except Exception as e:
        st.error(f"Something went wrong: {e}")