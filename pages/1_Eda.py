import streamlit as st
import numpy as np
import plotly.express as px
import pandas as pd
# import seaborn as sb

df = pd.read_csv("telecom_churn.csv")
numeric_df = pd.read_csv("telecom_churn.csv")
smote_df = pd.read_csv("telecom_churn_smote.csv")

st.markdown ("# Exploratory Data Analysis")
st.markdown("### Summary of Telecom churn data")

st.dataframe(df.describe())

st.markdown("## Overall Statistic")

# preprocess data 

df["Churn"] = df["Churn"].map({0:"Did not Churn",1:"Churn"})
df["ContractRenewal"] = df["ContractRenewal"].map({0:"Did Not Renew Contract",1:"Renewed Contract"})
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


fig_chvcr = px.histogram(df,"ContractRenewal",color = "Churn", opacity= 0.75)

grouped = df.groupby(["ContractRenewal", "Churn"]).size().reset_index(name="Count")

grouped["Percentage"] = grouped.groupby("ContractRenewal")["Count"].transform(lambda x: 100 * x / x.sum())

fig_chvcr_percent = px.bar(
    grouped, 
    x="ContractRenewal", 
    y="Percentage", 
    color="Churn", 
    text=grouped["Percentage"].round(1).astype(str) + "%",  # Display percentage labels
    opacity = 0.75,
    category_orders={"ContractRenewal": ["Renewed Contract", "Did Not Renew Contract"],"Churn":["Did not Churn","Churn"]}
)

c1 = st.selectbox("Please select desire graph",("Normal","Percentage"), index = 0,key="1")
st.plotly_chart(fig_chvcr if c1 == "Normal" else fig_chvcr_percent)

st.markdown("After switching from count to percentage, we observe that customers who recently renewed their contracts are less likely to terminate the service compared to those who did not renew. This suggests that contract renewal may be driven by customer trust and satisfaction with our company. Customers who choose to renew likely have a positive experience or see value in continuing the service, whereas those who do not renew may already be considering termination.")

st.markdown("#### 2.Churn vs CustServCall")

fig_chvcustcall = px.histogram(df,"CustServCalls",color = "Churn",opacity = 0.75)

grouped2 = df.groupby(["CustServCalls", "Churn"]).size().reset_index(name="Count")

grouped2["Percentage"] = grouped2.groupby("CustServCalls")["Count"].transform(lambda x: 100 * x / x.sum())

fig_chvcustcall_percent = px.bar(
    grouped2, 
    x="CustServCalls", 
    y="Percentage", 
    color="Churn", 
    text=grouped2["Percentage"].round(1).astype(str) + "%",  # Display percentage labels
    opacity = 0.75,
    category_orders={"Churn":["Did not Churn","Churn"]}
)

c2 = st.selectbox("Please select desire graph",("Normal","Percentage"), index = 0, key="2")
st.plotly_chart(fig_chvcustcall if c2 == "Normal" else fig_chvcustcall_percent)

st.markdown("Similar to `Contract Renewal`, an increase in `Customer Service Calls` (CustServCalls) is associated with a higher likelihood of service cancellation. However, this relationship may also suggest that customers who eventually cancel the service are more likely to have contacted customer support multiple times before making their decision. At the same time, the higher **likelihood of cancellation** might also be linked to a **lower proportion** of customers making frequent service calls, meaning that while dissatisfied customers tend to call more, the overall number of such customers remains relatively small. ")

st.markdown("#### 3. Churn vs DayMin")

fig_fix = px.histogram(df,"DayMins",color = "Churn",opacity = 0.75)

st.plotly_chart(fig_fix)

st.markdown("Based on the graph, we observe that the distribution of `DayMins` for customers with **Continued Service** follows a nearly normal distribution. In contrast, the distribution for customers with **Canceled Service** appears bimodal, suggesting two distinct usage patterns. Statistically, there is no **direct correlation** between these two distributions, meaning that the difference in shape is not necessarily indicative of a direct relationship between Churn and Non-Churn. Instead, the observed correlation may stem from an imbalance in the dataset or underlying factors influencing churn behavior.")

st.markdown("#### 4.Churn vs DayUsage")

fig_chvdm = px.histogram(df,"DataUsage",color = "DataPlan",opacity = 0.75)

st.plotly_chart(fig_chvdm)

st.markdown("From the graph, we observe that customers **without a data plan** mostly use between 0 and 0.5 units of data, whereas those **with a data plan** tend to use significantly more, typically between 1 and 5 units. Additionally, the distribution appears to be separated into two distinct components, which may indicate a strong dependency between Data Plan and Data Usage. This separation could lead to **multicollinearity** in predictive models, as the presence of a data plan almost directly determines the range of data usage, making these two variables highly correlated.")
 
st.markdown("#### 5.Monthly Charge vs Data Usage (Data Plan)")
st.markdown("Since `Dataplan` and `DataUsage` has high correlation and should similar result, we decided analyze `DataUsage` and seperate data using `DataPlan`")

fig_mcvsdu = px.scatter(df,y = "DataUsage",x = "MonthlyCharge", color = "DataPlan", opacity = 0.75)

st.plotly_chart(fig_mcvsdu)

st.markdown("As illustrated in the graph, the data is separated into two clusters based on the `Data Plan.`\nFor customers **without a data plan**, data usage remains low regardless of an increase in monthly charges. This suggests that monthly charges account for other telecom features beyond data usage, such as call or SMS plans.\n On the other hand, for customers **with a data plan**, data usage increases as monthly charges rise, implying that higher monthly charges may correspond to more extensive data plans. This distinction highlights a key relationship between data plans and pricing structure, reinforcing that monthly charges influence data usage differently depending on the presence of a data plan")

st.markdown("#### 6.Monthly Charge vs DayMins")

fig_mcvdm = px.scatter(df,y = "DayMins",x = "MonthlyCharge",color = "DataPlan", opacity = 0.75)

st.plotly_chart(fig_mcvdm)

st.markdown("According to the graph, the data can divide into two clusters between **with data plan** and **without data plan**. These two data have the same increasing trend, however, the one that include data plan has a higher charge that might cause from the additional data.")

st.markdown("## Data Imbalanced")

st.markdown("### SMOTE (Synthetic Minority Over-Sampling Technique)")

st.markdown("We address the issue of class imbalance using SMOTE (Synthetic Minority Over-Sampling Technique) to generate synthetic samples for the minority class based on `Churn`. SMOTE enhances the dataset by selecting a minority class instance, identifying its k-nearest neighbors, and creating synthetic points along the line connecting them. This approach helps improve model performance by preventing bias toward the majority class. We choose **oversampling** over undersampling because the minority class **contains too few data points** for effective training. Undersampling would remove valuable information from the majority class, potentially leading to loss of critical patterns and suboptimal model performance. By using SMOTE, we maintain the dataset’s diversity while ensuring balanced class representation.")

df_smote = pd.read_csv("telecom_churn_smote.csv")

fig_pie = px.pie(df_smote,names = "Churn", opacity=0.8)

st.plotly_chart(fig_pie)

st.markdown("We can see that the different between data before and after **SMOTE** is a number of data points that increase from 3333 to 5700 data points. With this adjustment, the percentage of people who canceled the service and people who retained the service is come closer to 50%. Additionally, the correlation of the dataset is the same as a result from **SMOTE** which generated a data based on k-nearest neighbors.")

