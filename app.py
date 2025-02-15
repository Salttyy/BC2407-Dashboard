import streamlit as st
import pandas as pd
import numpy as np 
import plotly.express as px

st.markdown(f"# BC2407 Project Dashboard")
df = pd.read_csv("telecom_churn.csv")

st.markdown("### Telecom churn data")
st.dataframe(df)

st.markdown ("### Exploratory Data Analysis")

color = px.colors.qualitative.Dark24

df["Churn"] = df["Churn"].astype(str);

fig1 = px.box(df, 
              y="AccountWeeks", 
              color="Churn", 
              facet_col="Churn",
              title="Account Weeks vs Churn",
              color_discrete_sequence=color)

fig1.update_xaxes(title_text="")  # Remove x-axis title
fig1.update_xaxes(showticklabels=False)  # Remove x-axis text
fig1.update_xaxes(showgrid=False)  # Remove x-axis ticks

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