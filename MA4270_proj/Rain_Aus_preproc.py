import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler
import plotly.express as px
import plotly.io as io
import missingno as msno
import seaborn as sns
from plotly import tools
# load the dataset
raw_df = pd.read_csv('/Users/wangjiangyi/Desktop/weatherAUS.csv')
raw_df.dropna(subset=['RainToday', 'RainTomorrow'], inplace=True)

#draw the label imblance diagram
#raw_df1=raw_df.fillna('None')
#fig=px.histogram(raw_df1,
#             x='Location',
#             color='RainToday',
#             title='Visualization of Label Imbalance',)
#io.write_image(fig, '/Users/wangjiangyi/Desktop/imb.png')

# setting target column
y = raw_df.RainTomorrow
# fill NA
X = raw_df.drop(['RainTomorrow'], axis=1)

# split the time information
year = pd.to_datetime(raw_df.Date).dt.year

#plot the datasets
#df1=pd.read_csv('/Users/wangjiangyi/Desktop/weatherAUS.csv', index_col=['Date'], parse_dates=True)
#sns.countplot(y=df1.index.year)
#plt.show()

#visulize the missing value
#msno.bar(raw_df, labels=True, figsize=(24,7),fontsize=8)
#plt.show()




#visualize some interesting property
#fig=px.histogram(X.fillna('None'), x='Location', title='Location vs. Rainy Days', color='RainToday')

#fig.show()

# split the dataset to three part

train_inputs = X[year < 2015]
val_inputs = X[year == 2015]
test_inputs = X[year > 2015]

train_targets = y[year < 2015]
val_targets = y[year == 2015]
test_targets = y[year > 2015]
print(y)
#split the dataset according to the data type for further fill NA
numeric_cols = X.select_dtypes(include = 'float64').columns.to_list()
cat_cols = X.select_dtypes(include = 'object').columns.to_list()[1:]

# fill NA for numerical type
imputer = SimpleImputer (strategy = 'median')
imputer.fit(X[numeric_cols])
'''
train_inputs=train_inputs.copy()
train_inputs.loc[:, numeric_cols]=imputer.transform(train_inputs[numeric_cols])
val_inputs=val_inputs.copy()
val_inputs[numeric_cols] = imputer.transform(val_inputs[numeric_cols])
test_inputs=test_inputs.copy()
test_inputs[numeric_cols] = imputer.transform(test_inputs[numeric_cols])
'''
#plt.figure(figsize=(15,13))
X[numeric_cols]=X[numeric_cols].copy()
X.loc[:, numeric_cols]=imputer.transform(X[numeric_cols])
#sns.heatmap(X[numeric_cols].corr(), annot=True)

#plt.show()

#as for categorical feature
# fill NA
encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
X2 = X[cat_cols].fillna(method='ffill')
encoder.fit(X2)
#print(X['RainToday'].isna().sum())

encoded_cols = list(encoder.get_feature_names_out(cat_cols))
#print(len(encoded_cols))
'''
train_inputs=train_inputs.copy()
#onehot
train_inputs.loc[:,encoded_cols] = encoder.transform(train_inputs[cat_cols].fillna(method='ffill'))
#print(train_inputs.columns)
val_inputs=val_inputs.copy()
val_inputs.loc[:,encoded_cols] = encoder.transform(val_inputs[cat_cols].fillna(method='ffill'))
test_inputs=test_inputs.copy()
test_inputs.loc[:,encoded_cols] = encoder.transform(test_inputs[cat_cols].fillna(method='ffill'))
'''
X=X.copy()
X.loc[:, encoded_cols]=encoder.transform(X[cat_cols].fillna(method='ffill'))

X=X.copy()
X.loc[:,'RainTomorrow']=y
fig1=px.scatter(X, x='Humidity9am', y='Humidity3pm',
          color='RainTomorrow')

#X.drop(cat_cols+['Temp9am','Temp3pm'],axis=1,inplace=True)


sm=SMOTE(sampling_strategy={0:109586,1:109586})  # should be open
#y_train.index=range(0,97988)
#X_train.index=range(0,97988)
X_sm, y_sm = sm.fit_resample(X[numeric_cols], y) # should be open
X_sm = X_sm.copy()
X_sm.loc[:,'RainTomorrow']=y_sm

fig2=px.scatter(X_sm, x='Humidity9am', y='Humidity3pm',color='RainTomorrow')

fig=tools.make_subplots(rows=2,cols=1)
fig.append_trace()

numeric_cols.pop()
numeric_cols.pop()

'''
#scaler
scaler = MinMaxScaler()
scaler.fit(X[numeric_cols])
X[numeric_cols] = scaler.transform(X[numeric_cols])

X.to_csv('/Users/wangjiangyi/Desktop/pre-processed.csv',index=False,sep=',')


'''

