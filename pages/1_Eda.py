import streamlit as st
import numpy as np
import plotly.express as px
import pandas as pd
import seaborn as sb

df = pd.read_csv("telecom_churn.csv")
numeric_df = pd.read_csv("telecom_churn.csv")
smote_df = pd.read_csv("telecom_churn_smote.csv")

st.markdown ("# Exploratory Data Analysis")
st.markdown("### Summary of Telecom churn data")

st.dataframe(df.describe())

st.markdown("## Overall Statistic")

# preprocess data 

df["Churn"] = df["Churn"].map({0:"Continued Service",1:"Canceled Service"})
df["ContractRenewal"] = df["ContractRenewal"].map({0:"No Recent Renewal",1:"Recent Renewal"})
df["DataPlan"] = df["DataPlan"].map({0:"No Data Plan",1:"Has Data Plan"})

st.markdown("### Distribution of data and Churn")

dis = st.selectbox("Please select desire column",df.columns, index = None)

if(dis):
    fig = px.histogram(df, x=dis, color='Churn') 
    st.plotly_chart(fig)

st.markdown("### Comparison of Numerical Data")

Categorical = ["Churn","ContractRenewal","DataPlan"]

x = st.selectbox("Please select the X axis",df.drop(columns=Categorical).columns, index = None)

y = st.selectbox("Please select the Y axis",df.drop(columns=Categorical).columns, index = None)

categorical = st.selectbox("Please select the Categorical Color", Categorical, index = None)

if(x and y): 
    fig2 = px.scatter(df, x = x, y = y, color = categorical)
    st.plotly_chart(fig2)

st.markdown("### Interesting insight")
st.markdown("#### Percentage of Churn column")

fig3 = px.pie(df,names = "Churn")
st.plotly_chart(fig3)
st.markdown("We can see that there is an imbalance of data between `Churn` and `not Churn`")

cor = numeric_df.corr()
fig_cor = px.imshow(cor,text_auto=True,color_continuous_scale='sunset')
fig_cor.update_layout(height=800, width=1400)
st.plotly_chart(fig_cor)
st.markdown("This is the correlation matrix of all the data. In the next section we will go through a comparison of data that has correlation more than 0.2 or less than -0.2")

st.markdown("#### 1.Churn vs ContractRenewal")
col1, col2 = st.columns(2)

fig_chvcr = px.histogram(df,"ContractRenewal",color = "Churn", opacity= 0.75)
col1.plotly_chart(fig_chvcr)

grouped = df.groupby(["ContractRenewal", "Churn"]).size().reset_index(name="Count")

grouped["Percentage"] = grouped.groupby("ContractRenewal")["Count"].transform(lambda x: 100 * x / x.sum())

fig_chvcr_percent = px.bar(
    grouped, 
    x="ContractRenewal", 
    y="Percentage", 
    color="Churn", 
    text=grouped["Percentage"].round(1).astype(str) + "%",  # Display percentage labels
    opacity = 0.75,
    category_orders={"ContractRenewal": ["Recent Renewal", "No Recent Renewal"],"Churn":["Continued Service","Canceled Service"]}
)

col2.plotly_chart(fig_chvcr_percent)