# The dataset comes from Kaggle, which is about the Rain Prediction in India
# (Binary classifcation) Problem
# Use Random Forest, Logistic Regression, Adaboost, GBDT, XGBOOST
from imblearn.over_sampling import SMOTE
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.feature_selection import RFE
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import recall_score, confusion_matrix, roc_auc_score
import pickle

# Step 1): set the path of dataset
filename1 = "/Users/wangjiangyi/Desktop/data/forecast_data.csv"
filename2 = "/Users/wangjiangyi/Desktop/data/location_data.csv"

# Step 2): load the dataset and data pre-processing
weather_data = pd.read_csv(filename1)
location_data = pd.read_csv(filename2)

#print(weather_data.shape)
#print(weather_data.head())
#print(location_data.shape)
#print(location_data.head())

# Notice that there are some REDUNDANT columns like TEMP_C & TEMP_F
redundant_col = ['time', 'temp_f', 'wind_kph', 'pressure_in', 'precip_in', 'feelslike_f', 'windchill_f', 'heatindex_f', 'dewpoint_f', 'chance_of_rain', 'will_it_snow', 'chance_of_snow', 'vis_miles', 'gust_kph']
weather_data.drop(redundant_col, axis=1, inplace=True)
#print(weather_data.shape)
#print(location_data.shape)

# transform the categorical label into number (later we will use one-hot code)
categorical_cols = ['condition', 'wind_dir', 'state', 'city']
for col in categorical_cols:
    le = LabelEncoder()
    weather_data[col] = le.fit_transform(weather_data[col])



# Step 3): split the dataset for training samples and labels
# NOTICE y is SERIES
y = weather_data['will_it_rain']
X = weather_data.drop('will_it_rain', axis=1)

y_list = pd.Series.to_list(y)

# Centralization
scaler = StandardScaler()
X_scaler = scaler.fit_transform(X)
X_central = pd.DataFrame(X_scaler, columns=X.columns)




# Step 4): Training
# Split the data into training and testing set
X_train, X_test, y_train, y_test = train_test_split(X_central, y_list, test_size=0.1, random_state=6)

#over-sample
#X_train, y_train = SMOTE().fit_resample(X_train_down, y_train_down)
print(X_train.shape)
gbdt = GradientBoostingClassifier(loss='exponential', learning_rate=1, n_estimators=1, subsample=1
                                  , min_samples_split=2, min_samples_leaf=2, max_depth=1
                                  , init=None, random_state=None, max_features=None
                                  , verbose=0, max_leaf_nodes=None, warm_start=False
                                  )
gbdt1 = GradientBoostingClassifier()
ada = AdaBoostClassifier()
lr = LogisticRegression(penalty='none', max_iter=2000)
dt_stump=DecisionTreeClassifier(max_depth=100,min_samples_leaf=5)

dt_stump.fit(X_train, y_train)

test_pred = dt_stump.predict(X_test)
train_pred = dt_stump.predict(X_train)



print("testing accuracy is: ", dt_stump.score(X_test,y_test))
print("training accuracy is: ", dt_stump.score(X_train,y_train))
print(X_train)

#print(test_pred, y_test)
