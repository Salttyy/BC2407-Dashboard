library(data.table)
library(caTools)
library(rpart)
library(rpart.plot)
library(caret)
setwd("C:/Users/amand/OneDrive - Nanyang Technological University/Y2S1_BA/2 BC2406 Analytics 1/Grp projec")
dt_telecomchurn <- fread('telecom_churn.csv')

View(dt_telecomchurn)
summary(dt_telecomchurn ) 

colSums(is.na(dt_telecomchurn)) # to detect NA values or blank space
colSums(is.na(dt_telecomchurn ) | dt_telecomchurn  == "")  

dt_telecomchurn$Churn = factor(dt_telecomchurn$Churn, levels = c(0,1), labels = c("Continued Service","Cancelled Service"))
dt_telecomchurn$DataPlan <- factor(dt_telecomchurn$DataPlan, levels = c(0, 1), labels = c("No Data Plan", "Has Data Plan"))
dt_telecomchurn$ContractRenewal <- factor(dt_telecomchurn$ContractRenewal, levels = c(0, 1), labels = c("No Recent Renewal", "Recent Renewal"))

#Accountweeks
#Boxplot of Accountweeks
ggplot(dt_telecomchurn, aes( y = AccountWeeks, fill = Churn, group = Churn)) +
  geom_boxplot() +
  facet_wrap(~ Churn)+
  labs(title = "Account Weeks vs Churn",y = "Account Weeks")+
  theme(
    axis.title.x = element_blank(),  # Remove x-axis title
    axis.text.x = element_blank(),   # Remove x-axis text
    axis.ticks.x = element_blank())  # Remove x-axis ticks

ggplot(dt_telecomchurn, aes(x = AccountWeeks, fill = as.factor(Churn))) + 
  geom_histogram(binwidth = 5, position = "identity", alpha = 0.5) + 
  labs(title = "Distribution of Account Weeks by Churn", x = "Account Weeks", fill = "Churn") + 
  scale_fill_discrete(labels = c("Continued Service", "Cancelled Service"))


#Contract renewal 
# Calculation of the percentages for ContractRenewal for stacked labels
contractrenewal_prop <- dt_telecomchurn[, .(count = .N), by = .(ContractRenewal, Churn)]
contractrenewal_prop[, percentage := count / sum(count), by = ContractRenewal]

# Stacked bar plot with percentage labels for ContractRenewal
ggplot(contractrenewal_prop, aes(x = ContractRenewal, y = percentage, fill = Churn)) +
  geom_bar(stat = "identity", position = "fill") + 
  geom_text(aes(label = scales::percent(percentage, accuracy = 1)),
            position = position_fill(vjust = 0.5), size = 4) +  # Adds percentage labels
  labs(title = "Churn Rate by Contract Renewal", x = "Contract Renewal", y = "Proportion") +
  scale_y_continuous(labels = scales::percent) +
  theme_minimal()

#dataplan
# Calculation of the percentages for DataPlan for stacked labels
dataplan_prop <- dt_telecomchurn[, .(count = .N), by = .(DataPlan, Churn)]
dataplan_prop[, percentage := count / sum(count), by = DataPlan]

# Stacked bar plot with percentage labels for DataPlan
ggplot(dataplan_prop, aes(x = DataPlan, y = percentage, fill = Churn)) +
  geom_bar(stat = "identity", position = "fill") + 
  geom_text(aes(label = scales::percent(percentage, accuracy = 1)),
            position = position_fill(vjust = 0.5), size = 4) +  # Adds percentage labels
  labs(title = "Churn Rate by Data Plan", x = "Data Plan", y = "Proportion") +
  scale_y_continuous(labels = scales::percent) +
  theme_minimal()


# DataUsage
dt_telecomchurn_filtered <- dt_telecomchurn[DataPlan == 'Has Data Plan']
ggplot(dt_telecomchurn_filtered, aes(y = DataUsage, fill = Churn, group = Churn)) +
  geom_boxplot() +
  facet_wrap(~ Churn) +
  labs(title = "Data Usage vs Churn (Customers with Data Plans)", y = "Data Usage (GB)") +
  theme(
    axis.title.x = element_blank(),  # Remove x-axis title
    axis.text.x = element_blank(),   # Remove x-axis text
    axis.ticks.x = element_blank()   # Remove x-axis ticks
  )


#daymins
#Boxplot of Daymins
ggplot(dt_telecomchurn, aes( y = DayMins, fill = Churn, group = Churn)) +
  geom_boxplot() +
  facet_wrap(~ Churn)+
  labs(title = "DayMins vs Churn",y = "DayMins")+
  theme(
    axis.title.x = element_blank(),  # Remove x-axis title
    axis.text.x = element_blank(),   # Remove x-axis text
    axis.ticks.x = element_blank()   # Remove x-axis ticks
  )
ggplot(dt_telecomchurn, aes(x = DayMins, fill = as.factor(Churn))) + 
  geom_histogram(binwidth = 5, position = "identity", alpha = 0.5) + 
  labs(title = "Distribution of Day Minutes by Churn", x = "Day Minutes", fill = "Churn") + 
  scale_fill_discrete(labels = c("Continued Service", "Cancelled Service"))

#daycalls
#DayCalls
# Box Plot of Day Calls by Churn
ggplot(dt_telecomchurn, aes( y = DayCalls, fill = Churn, group = Churn)) +
  geom_boxplot() +
  facet_wrap(~ Churn)+
  labs(title = "Day Calls vs Churn",y = "Day Calls")+
  theme(
    axis.title.x = element_blank(),  # Remove x-axis title
    axis.text.x = element_blank(),   # Remove x-axis text
    axis.ticks.x = element_blank()   # Remove x-axis ticks
  )


# Histogram - Churn by Day Calls
ggplot(dt_telecomchurn, aes(x = DayCalls, fill = as.factor(Churn))) + 
  geom_histogram(binwidth = 5, position = "identity", alpha = 0.5) + 
  labs(title = "Distribution of Day Calls by Churn", x = "Day Calls", fill = "Churn") + 
  scale_fill_discrete(labels = c("Continued Service", "Cancelled Service"))


# Roam minutes 
#Boxplot of Roaming Minutes
ggplot(dt_telecomchurn, aes( y = RoamMins, fill = Churn, group = Churn)) +
  geom_boxplot() +
  facet_wrap(~ Churn)+
  labs(title = "Roam Mins vs Churn",y = "Roam Mins")+
  theme(
    axis.title.x = element_blank(),  # Remove x-axis title
    axis.text.x = element_blank(),   # Remove x-axis text
    axis.ticks.x = element_blank()   # Remove x-axis ticks
  )

#monthly charge
#Boxplot of Monthly Charge
ggplot(dt_telecomchurn, aes( y = MonthlyCharge, fill = Churn, group = Churn)) +
  geom_boxplot() +
  facet_wrap(~ Churn)+
  labs(title = "MonthlyCharge vs Churn",y = "MonthlyCharge")+
  theme(
    axis.title.x = element_blank(),  # Remove x-axis title
    axis.text.x = element_blank(),   # Remove x-axis text
    axis.ticks.x = element_blank()   # Remove x-axis ticks
  )
#histogram 
ggplot(dt_telecomchurn, aes(x = MonthlyCharge, fill = as.factor(Churn))) + 
  geom_histogram(binwidth = 5, position = "identity", alpha = 0.5) + 
  labs(title = "Distribution of Monthly Charge by Churn", x = "Monthly Charge", fill = "Churn") + 
  scale_fill_discrete(labels = c("Continued Service", "Cancelled Service"))


#overagefee
# Overage Fee
#Boxplot of Overage Fee
ggplot(dt_telecomchurn, aes( y = OverageFee, fill = Churn, group = Churn)) +
  geom_boxplot() +
  facet_wrap(~ Churn)+
  labs(title = "OverageFee vs Churn",y = "Overage Fee")+
  theme(
    axis.title.x = element_blank(),  # Remove x-axis title
    axis.text.x = element_blank(),   # Remove x-axis text
    axis.ticks.x = element_blank()   # Remove x-axis ticks
  )


# Histogram - Churn by Overage Fee
ggplot(dt_telecomchurn, aes(x = OverageFee, fill = as.factor(Churn))) + 
  geom_histogram(binwidth = 5, position = "identity", alpha = 0.5) + 
  labs(title = "Distribution of Overage Fee by Churn", x = "Overage Fee", fill = "Churn") + 
  scale_fill_discrete(labels = c("Continued Service", "Cancelled Service"))

#custservcall 
#Boxplot of CustServCalls
ggplot(dt_telecomchurn, aes( y = CustServCalls, fill = Churn, group = Churn)) +
  geom_boxplot() +
  facet_wrap(~ Churn)+
  labs(title = "CustServCalls vs Churn",y = "CustServCalls")+
  theme(
    axis.title.x = element_blank(),  # Remove x-axis title
    axis.text.x = element_blank(),   # Remove x-axis text
    axis.ticks.x = element_blank()   # Remove x-axis ticks
  )

# CustServCalls 
# Stacked Bar plot for churn rate by CustServCalls 
ggplot(dt_telecomchurn, aes(x = as.factor(CustServCalls), fill = as.factor(Churn))) + 
  geom_bar(position = "fill") + 
  labs(title = "Proportion of Churn by Customer Service Calls", 
       x = "Customer Service Calls", 
       y = "Proportion", 
       fill = "Churn") +
  scale_fill_discrete(labels = c("Continued Service", "Cancelled Service")) +
  theme_minimal()
