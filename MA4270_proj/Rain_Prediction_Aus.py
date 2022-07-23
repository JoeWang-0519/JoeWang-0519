import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import zero_one_loss
from sklearn.ensemble import AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
import time
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
import plotly.express as px

raw_df = pd.read_csv('/Users/wangjiangyi/Desktop/weatherAUS.csv')
#setting target column
y = raw_df.RainTomorrow


y=y.fillna(method='ffill')
print(y.isna().sum())

#removing targets from predictors

X = raw_df.drop(['RainTomorrow'], axis=1)
year = pd.to_datetime(raw_df.Date).dt.year
#print(X.isna().sum())
#print(X)


#imputer1 = SimpleImputer (strategy = 'median')
#imputer1.fit(y)
#y=y.copy()
#y=imputer1.transform(y)



train_inputs = X[year < 2015]
val_inputs = X[year == 2015]
test_inputs = X[year > 2015]

train_targets = y[year < 2015]
val_targets = y[year == 2015]
test_targets = y[year > 2015]

numeric_cols = train_inputs.select_dtypes(include = 'float64').columns.to_list()
cat_cols = train_inputs.select_dtypes(include = 'object').columns.to_list()[1:]

#create an imputer
imputer = SimpleImputer (strategy = 'median')

#fit the imputer in data
imputer.fit(X[numeric_cols])

print(numeric_cols)
train_inputs=train_inputs.copy()
train_inputs.loc[:, numeric_cols]=imputer.transform(train_inputs[numeric_cols])
val_inputs=val_inputs.copy()
val_inputs[numeric_cols] = imputer.transform(val_inputs[numeric_cols])
test_inputs=test_inputs.copy()
test_inputs[numeric_cols] = imputer.transform(test_inputs[numeric_cols])





scaler = MinMaxScaler()
scaler.fit(X[numeric_cols])
train_inputs[numeric_cols] = scaler.transform(train_inputs[numeric_cols])
val_inputs[numeric_cols] = scaler.transform(val_inputs[numeric_cols])
test_inputs[numeric_cols] = scaler.transform(test_inputs[numeric_cols])


# fill NA
encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
X2 = X[cat_cols].fillna(method='ffill')
encoder.fit(X2)
print(X['RainToday'].isna().sum())

encoded_cols = list(encoder.get_feature_names_out(cat_cols))

train_inputs=train_inputs.copy()
# 直接把categorical全都one-hot了
train_inputs.loc[:,encoded_cols] = encoder.transform(train_inputs[cat_cols].fillna(method='ffill'))
print(train_inputs.columns)
val_inputs=val_inputs.copy()
val_inputs.loc[:,encoded_cols] = encoder.transform(val_inputs[cat_cols].fillna(method='ffill'))
test_inputs=test_inputs.copy()
test_inputs.loc[:,encoded_cols] = encoder.transform(test_inputs[cat_cols].fillna(method='ffill'))

#

T=train_inputs[numeric_cols+encoded_cols]
T2=train_targets



model = LogisticRegression(solver ='liblinear', C=15, fit_intercept= False)
model.fit(train_inputs[numeric_cols + encoded_cols], train_targets)
'''
X_train = train_inputs[numeric_cols + encoded_cols]
X_val = val_inputs[numeric_cols + encoded_cols]
X_test = test_inputs[numeric_cols + encoded_cols]
print(model.score(train_inputs[numeric_cols + encoded_cols], train_targets))
print(model.score(X_test, test_targets))


gbdt = GradientBoostingClassifier(loss='exponential', learning_rate=1, n_estimators=1, subsample=1
                                  , min_samples_split=2, min_samples_leaf=2, max_depth=1
                                  , init=None, random_state=None, max_features=None
                                  , verbose=0, max_leaf_nodes=None, warm_start=False
                                  )
#gbdt.fit(X_train,train_targets)
#print(gbdt.score(X_train, train_targets))
#print(gbdt.score(X_test, test_targets))

dt_stump=DecisionTreeClassifier(max_depth=1,min_samples_leaf=1)
dt_stump.fit(X_train, train_targets)
print(dt_stump.score(X_train, train_targets))
print(dt_stump.score(X_test, test_targets))

'''