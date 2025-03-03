import streamlit as st
import numpy as np
import plotly.express as px
import pandas as pd
import seaborn as sb

df = pd.read_csv("telecom_churn.csv")

st.markdown ("# Exploratory Data Analysis")
st.markdown("### Summary of Telecom churn data")

st.dataframe(df.describe())

st.markdown("## Overall Statistic")




