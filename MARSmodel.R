# MARS Modelling 

setwd("C:/Users/lueyz/OneDrive/Documents/Study matters/Y2S2/BC2407 ANALYTICS II/BC2407 Group Project")

# 1. Install the relevant packages

library(earth)        # for MARS package. 
library(data.table)   # for .csv reading
library(caret)        # for grid search and TTS
library(MLmetrics)    # for performance metrics evaluation

# 2. Load the data 

df <- fread("telecom_churn_smote.csv")
View(df)
summary(df)
str(df)
df$Churn <- factor(df$Churn, levels = c(0,1), labels = c('Did_Not_Churn', 'Churned'))
df$ContractRenewal <- factor(df$ContractRenewal, levels = c(0,1), labels = c('Did_Not_Renew', 'Renewed'))
df$DataPlan <- factor(df$DataPlan, levels = c(0,1), labels = c('No_Data_Plan', 'Has_Data_Plan'))

# 3. 70/30 Train-Test Split

set.seed(123)
index <- createDataPartition(df$Churn, p = 0.7, list = F)

train <- df[index, ]
test <- df[-index, ]

summary(train)
summary(test)

# 4. Train the MARS Model

mars1 <- earth(
  Churn ~ ., 
  data = train,
  glm = list(family = binomial),
  degree = 1
)

summary(mars1)

# 5. Predict

predict1 <- predict(mars1, newdata = test, type = 'response')
threshold <- 0.5
predicted_class <- ifelse(predict1 > threshold,'Churned', 'Did_Not_Churn')
predicted_class <- factor(predicted_class, 
                          levels = levels(test$Churn))

#5.1 Generate the confusion matrix

confusion_results <- confusionMatrix(
  data = predicted_class,       # Predicted classes
  reference = test$Churn,       # True classes
  positive = "Churned"          # Define the "positive" class (event of interest)
)

# Print detailed results
print(confusion_results)

# ===============================================================================================================================================================================
# Confusion Matrix and Statistics
# 
# Reference
# Prediction      Did_Not_Churn Churned
# Did_Not_Churn           716     108
# Churned                 139     747
# 
# Accuracy : 0.8556         
# 95% CI : (0.838, 0.8719)
# No Information Rate : 0.5            
# P-Value [Acc > NIR] : < 2e-16        
# 
# Kappa : 0.7111         
# 
# Mcnemar's Test P-Value : 0.05628        
#                                          
#             Sensitivity : 0.8737         
#             Specificity : 0.8374         
#          Pos Pred Value : 0.8431         
#          Neg Pred Value : 0.8689         
#              Prevalence : 0.5000         
#          Detection Rate : 0.4368         
#    Detection Prevalence : 0.5181         
#       Balanced Accuracy : 0.8556  * F1 Score (Area of Concern)       
#                                          
#        'Positive' Class : Churned  
# ===============================================================================================================================================================================


# 5.1 : Model Performance Metrics

# Accuracy =  85.6%
# Precision = 84.3%
# F1-score = 85.6%

# 6.1 Optimize model parameters to maximize F1 score
# 6.1.1 Define a function for the computation of F1 score

customSummary <- function(data, lev = NULL, model = NULL) {
  # `data` contains observed (`obs`) and predicted (`pred`) classes
  # `lev` holds the factor levels (e.g., "Did_Not_Churn", "Churned")
  
  # Calculate F1-score, precision, and recall
  f1 <- F1_Score(
    y_true = data$obs,          # Observed class labels
    y_pred = data$pred,         # Predicted class labels
    positive = lev[2]           # "Churned" is the positive class
  )
  
  precision <- Precision(
    y_true = data$obs,
    y_pred = data$pred,
    positive = lev[2]
  )
  
  recall <- Recall(
    y_true = data$obs,
    y_pred = data$pred,
    positive = lev[2]
  )
  
  # Return metrics
  c(F1 = f1, Precision = precision, Recall = recall)
}

# 6.1.2 Defining Model Tuning Terms

ctrl <- trainControl(
  method = "cv",           # 10-fold cross-validation
  number = 10,
  classProbs = TRUE,       # Generate class probabilities
  summaryFunction = customSummary,  # Use the custom F1 function
  savePredictions = "final"
)

tuneGrid <- expand.grid(
  degree = 1:3,           # Tests interaction depth (1-3) to find the optimal degree
  nprune = seq(5, 50, by = 5)  # Tests pruning levels from 5-50 in steps of 5 to find the optimal nprune. 
)

# 6.2 Hyperparameter tuning 

tuned_m1 <- train(
  Churn ~ ., 
  data = train,
  method = "earth",
  tuneGrid = tuneGrid,
  trControl = ctrl,
  metric = "F1",          # Optimize for F1-score
  maximize = TRUE         # Higher F1 is better
)

print(tuned_m1)  # The final values used for the model were nprune = 15 and degree = 3.

# 6.3 Predict using the tuned model

# Get predicted probabilities for the "Churned" class
predict_probs <- predict(tuned_m1, newdata = test, type = "prob")$Churned

# Apply threshold to classify
threshold <- 0.5
predicted_class <- ifelse(predict_probs > threshold, "Churned", "Did_Not_Churn")

# Ensure factor levels match the true labels
predicted_class <- factor(predicted_class, levels = levels(test$Churn))

# 6.4 Generate confusion matrix
confusion_results <- confusionMatrix(
  data = predicted_class, 
  reference = test$Churn,
  positive = "Churned"
)
print(confusion_results)

#========================================================================================================================================================

# Confusion Matrix and Statistics
# 
# Reference
# Prediction      Did_Not_Churn Churned
# Did_Not_Churn           739     102
# Churned                 116     753
# 
# Accuracy : 0.8725         
# 95% CI : (0.8558, 0.888)
# No Information Rate : 0.5            
# P-Value [Acc > NIR] : <2e-16         
# 
# Kappa : 0.745          
# 
# Mcnemar's Test P-Value : 0.3786         
#                                          
#             Sensitivity : 0.8807         
#             Specificity : 0.8643         
#          Pos Pred Value : 0.8665         
#          Neg Pred Value : 0.8787         
#              Prevalence : 0.5000         
#          Detection Rate : 0.4404         
#    Detection Prevalence : 0.5082         
#       Balanced Accuracy : 0.8725         *F1 Score (Area of Concern)
#                                          
#        'Positive' Class : Churned  

# After tuning the model, key performance metrics like accuracy, sensitivity, specificity and most importantly, F1 Score, increased.


























