import streamlit as st
import pandas as pd
import numpy as np 
import plotly.express as px

st.set_page_config(
    page_title="Dashboard",
    page_icon="🤖",
)

st.markdown(f"# BC2407 Project Dashboard")
df = pd.read_csv("telecom_churn.csv")

st.markdown("### Telecom churn data")
st.dataframe(df)

