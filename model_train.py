# IMPORT LIBRARIES
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score

from sklearn.ensemble import RandomForestRegressor

import joblib
import re

# LOAD DATA
data = pd.read_csv("House_Rent_Dataset.csv")
data.head()

# BASIC CLEANING
data = data.dropna()

# Remove useless columns
data = data.drop(["Posted On", "Area Locality", "Point of Contact"], axis=1)

# FLOOR CLEANING
def extract_floor(x):
    try:
        if "Ground" in x:
            return 0
        elif "Upper" in x:
            return 1
        elif "Lower" in x:
            return -1
        else:
            return int(re.findall(r'\d+', x)[0])
    except:
        return np.nan

data["Floor"] = data["Floor"].apply(extract_floor)

data["Floor"] = data["Floor"].fillna(data["Floor"].median())
data["Floor"] = data["Floor"].astype(int)

# # REMOVE OUTLIERS
data = data[data["Rent"] < 100000]

# ENCODING(maping)
le = LabelEncoder()

data["Area Type"] = le.fit_transform(data["Area Type"])
data["City"] = le.fit_transform(data["City"])
data["Furnishing Status"] = le.fit_transform(data["Furnishing Status"])
data["Tenant Preferred"] = le.fit_transform(data["Tenant Preferred"])

# remove weak features
data = data.drop(["Area Type", "Tenant Preferred"], axis=1)

# LOG TRANSFORM TARGET
y = np.log1p(data["Rent"])
X = data.drop("Rent", axis=1)

# TRAIN TEST SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)

# MODEL (OPTIMIZED)
model = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    min_samples_split=10,
    min_samples_leaf=5,
    random_state=42
)

model.fit(X_train, y_train)

# MODEL (OPTIMIZED)
model = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    min_samples_split=10,
    min_samples_leaf=5,
    random_state=42
)

model.fit(X_train, y_train)


# PREDICTION
y_pred = model.predict(X_test)

# Convert back from log
y_test_actual = np.expm1(y_test)
y_pred_actual = np.expm1(y_pred)


# EVALUATION
rmse = np.sqrt(mean_squared_error(y_test_actual, y_pred_actual))
r2 = r2_score(y_test_actual, y_pred_actual)

print("RMSE:", rmse)
print("R2 Score:", r2)

# EVALUATION
rmse = np.sqrt(mean_squared_error(y_test_actual, y_pred_actual))
r2 = r2_score(y_test_actual, y_pred_actual)

print("RMSE:", rmse)
print("R2 Score:", r2)

# GRAPH 1 (ACTUAL vs PREDICTED)
plt.figure()
plt.scatter(y_test_actual, y_pred_actual)
plt.xlabel("Actual Rent")
plt.ylabel("Predicted Rent")
plt.title("Actual vs Predicted Rent")
plt.show()

# GRAPH 1 (ACTUAL vs PREDICTED)
plt.figure()
plt.scatter(y_test_actual, y_pred_actual)
plt.xlabel("Actual Rent")
plt.ylabel("Predicted Rent")
plt.title("Actual vs Predicted Rent")
plt.show()

# FEATURE IMPORTANCE
importances = model.feature_importances_
features = X.columns

plt.figure()
plt.barh(features, importances)
plt.title("Feature Importance")
plt.show()

#SAVE MODEL
joblib.dump(model, "house_rent_rf_model.pkl")
print("Model Saved Successfully")


'''
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

# STEP 0: City mapping FIX (original CSV se)
data_original = pd.read_csv("House_Rent_Dataset.csv")

le_city = LabelEncoder()
le_city.fit(data_original["City"])

print("City Mapping:", dict(enumerate(le_city.classes_)))


# STEP 1: show test data
i = int(input("\nEnter index to view data (0 to {}): ".format(len(X_test)-1)))

print("\nSelected Data (from CSV):")
print(X_test.iloc[i])

actual = np.expm1(y_test.iloc[i])
print("Actual Rent (CSV):", round(actual))

# show correct city name
city_code = int(X_test.iloc[i]["City"])
print("City Name:", le_city.classes_[city_code])


# STEP 2: manual input
print("\nEnter same values manually:")

input_data = []
for col in X_test.columns:
    val = float(input(f"{col}: "))
    input_data.append(val)

input_array = np.array(input_data).reshape(1, -1)


# STEP 3: prediction
pred = np.expm1(model.predict(input_array))[0]


# STEP 4: result
print("\nRESULT")
print("Actual Rent:", round(actual))
print("Predicted Rent:", round(pred))
print("Difference:", round(abs(actual - pred)))
print("Accuracy %:", round(100 - (abs(actual - pred)/actual)*100, 2))

'''