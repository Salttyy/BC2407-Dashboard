import streamlit as st
import numpy as np
import plotly.express as px
import joblib 
import pandas as pd

st.markdown ("# Our Models")

# reading data
rf = joblib.load("model/random_forest.joblib")
xgb = joblib.load("model/XGBoost.joblib")
mlp = joblib.load("model/MLP.joblib")
log = joblib.load("model/Logistic.joblib")

col1, col2 = st.columns(2)
with col1:
    Acw = st.number_input(
        "Insert number of weeks customer has had active account", value=65, placeholder="Type a number..."
    )

    Dtu = st.number_input(
        "Insert gigabytes of monthly data usage", value=0.29, placeholder="Type a number..."
    )

    CusCall = st.number_input(
        "Insert number of calls into customer service", value=4, placeholder="Type a number..."
    )

    Dmin = st.number_input(
        "Insert average daytime minutes per month", value=129.1, placeholder="Type a number..."
    )
    Renew = st.selectbox(
        "Does the user recently renew the contract?",
        ("Yes","No"),
        index=0,
        placeholder="Select...",
    )

with col2:
    Dcall = st.number_input(
        "Insert average number of daytime calls", value=137, placeholder="Type a number..."
    )

    Bill = st.number_input(
        "Insert average monthly bill", value=44.9, placeholder="Type a number..."
    )

    Ofee = st.number_input(
        "Insert largest overage fee in last 12 months", value=11.43, placeholder="Type a number..."
    )

    Roam = st.number_input(
        "Insert largest average number of roaming minutes", value=12.7, placeholder="Type a number..."
    )
    Dplan = st.selectbox(
        "Does the user has data plan?",
        ("Yes","No"),
        index=1,
        placeholder="Select...",
    )

model = st.selectbox(
        "Select your desire model",
        ("Random Forest","XGBoost", "Multi-layer Perceptron", "Logistic Regression"),
        index=0,
        placeholder="Select your model...",
    )

parameters = {
    'AccountWeeks': [Acw],
    'ContractRenewal': [1 if Renew == "Yes" else 0],
    'DataPlan': [1 if Dplan == "Yes" else 0],
    'DataUsage': [Dtu],
    'CustServCalls': [CusCall],
    'DayMins': [Dmin],
    'DayCalls': [Dcall],
    'MonthlyCharge': [Bill],
    'OverageFee': [Ofee],
    'RoamMins': [Roam]
}
dict = {"Random Forest":rf,"XGBoost":xgb, "Multi-layer Perceptron":mlp, "Logistic Regression":log}
df = pd.DataFrame(parameters)
m = dict[model]
result = m.predict(df)
if(result):
    st.warning('Your customer is likely to canceled our service', icon="⚠️")
else:
    st.success('Your customer will not canceled our service', icon="✅")