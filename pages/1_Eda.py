import streamlit as st
import numpy as np
import plotly.express as px
import pandas as pd

df = pd.read_csv("telecom_churn.csv")

st.markdown ("## Exploratory Data Analysis")
st.markdown("### Summary of Telecom churn data")

st.dataframe(df.describe())

color = px.colors.qualitative.Dark24    

df["Churn"] = df["Churn"].astype(str);

fig1 = px.box(df, 
              y="AccountWeeks", 
              color="Churn", 
              facet_col="Churn",
              title="Account Weeks vs Churn",
              color_discrete_sequence=color)

fig1.update_xaxes(title_text="")  
fig1.update_xaxes(showticklabels=False) 
fig1.update_xaxes(showgrid=False)  

st.plotly_chart(fig1)

fig2 = px.histogram(df, 
                    x="AccountWeeks", 
                    color="Churn", 
                    opacity=0.5, 
                    barmode="overlay",
                    title="Distribution of Account Weeks by Churn",
                    labels={"Churn": "Churn Status"},
                    color_discrete_sequence=color)


st.plotly_chart(fig2)