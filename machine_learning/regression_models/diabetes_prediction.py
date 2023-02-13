import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score



#this will print out a helpful error message, based on the (not so few) error messages I encountered while implementing this code.
try:
    # Loading the data into a pandas df
    data = pd.read_csv("diabetes.csv")
except FileNotFoundError:
    print("The file 'diabetes.csv' was not found. Please ensure that it exists and is in the correct directory.")
    exit()
except pd.errors.ParserError:
    print("The file 'diabetes.csv' could not be loaded into a DataFrame. Please ensure that it is a proper CSV file.")
    exit()

try:
    X = data.drop("Outcome", axis=1)
    y = data["Outcome"]
except KeyError:
    print("The column specified in the script above was not found in the 'diabetes.csv' file. Please ensure that it exists in the file.")
    exit()

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Initialize a list to store the cross-validation scores
cv_scores = []

# Define a range of alpha values to test
alphas = np.logspace(-5, 5, 50)

# Loop over each alpha value and evaluate the performance using the cross-validation function
for val in alphas:
    reg = Ridge(alpha=val)
    scores = cross_val_score(reg, X_train, y_train, cv=5)
    cv_scores.append(np.mean(scores))

# Finding the best alpha value so we may avoid an overfitting issue
best_alpha = alphas[np.argmax(cv_scores)]

# Train the final model with the best alpha value
reg = Ridge(alpha=best_alpha)
reg.fit(X_train, y_train)

# Use the trained model to make predictions on the test data
y_pred = reg.predict(X_test)

# Evaluate the performance of the model using mean squared error
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# Evaluate the performance of the model using R-squared
r2 = r2_score(y_test, y_pred)
print("R-squared:", r2)

# Evaluate the performance of the model using cross-validation
cv_score = np.mean(cross_val_score(reg, X, y, cv=5))
print("Cross-Validation Score:", cv_score)



#INTERPRETING THE RESULTS OF THIS MODEL:

"""
The Mean Squared Error (MSE) is a measure of the average difference between the predicted values and the true values. 
In this case, the MSE of 0.17 indicates that the average difference between the predicted and true values is about 0.17. 
A lower MSE value is generally better, as it indicates that the model is making accurate predictions. 


The R-squared value is a measure of how well the regression line fits the data. 
It takes values between 0 and 1, where a higher value indicates a better fit. 
In our case, the R-squared value of 0.25 indicates that the model explains about 25% of the variance in the target variable. 
This is relatively low, and might indicate that the features in the data are not strong predictors of the target variable.


The cross-validation score represents the average performance of the model on the different folds of the data used in cross-validation. 
In this case, the cross-validation score of 0.27 indicates that, on average, the model is able to explain about 27% of the variance in 
the target variable. 
This score is similar to the R-squared value, and suggests that the model is not performing well in terms of explaining the target variable.


Overall, these results suggest that the linear regression model is not making accurate predictions *insert sad face* and 
that the features in the data may not be strong predictors of the target variable. 
Improving the model's performance may require additional feature adjustments or a different ML algorithm altogether.
"""


#OTHER INSIGHTS / COMMENTS:
"""
Evidently, the capitalization of X and lowercase y is a common convention in machine learning and reflects
the mathematical notation for input variables and output variables. 
In a machine learning problem, the input variables are often represented by a matrix X (with one row for each sample and one column for each feature), 
while the output variable is a vector y (with one entry for each sample).

So, in the code, X_train represents the training data for the input variables, while y_train represents the corresponding 
training data for the target variable. During model training, the algorithm uses the X_train and y_train arrays to 
learn the relationships between the input variables and the target variable, and these learned relationships are then used to 
make predictions on new, unseen data
"""
