import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score


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

# Loop over each alpha value and evaluate the performance using cross-validation
for val in alphas:
    reg = Ridge(alpha=val)
    scores = cross_val_score(reg, X_train, y_train, cv=5)
    cv_scores.append(np.mean(scores))

# Find the best alpha value
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