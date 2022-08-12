import time
import pandas as pd
from sklearn import  metrics
import numpy as np
from sklearn.metrics import confusion_matrix
from imblearn.over_sampling import SMOTE
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import zero_one_loss
import xgboost as xgb
from sklearn.ensemble import AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
import seaborn as sn
import matplotlib.pyplot as plt
from xgboost.sklearn import XGBClassifier
from sklearn.model_selection import GridSearchCV
import warnings


def tun_parameters(train_x, train_y):
    xgb1 = XGBClassifier(learning_rate=0.2, n_estimators=350, max_depth=5, min_child_weight=1, gamma=0, subsample=0.8,
                         colsample_bytree=0.8, objective='binary:logistic', scale_pos_weight=1, seed=27)
    modelfit(xgb1, train_x, train_y)


def modelfit(alg, X, y, useTrainCV=True, cv_folds=5, early_stopping_rounds=50):
    if useTrainCV:
        xgb_param = alg.get_xgb_params()
        xgtrain = xgb.DMatrix(X, label=y)
        cvresult = xgb.cv(xgb_param, xgtrain, num_boost_round=alg.get_params()['n_estimators'], nfold=cv_folds,
                          metrics='auc', early_stopping_rounds=early_stopping_rounds)
        alg.set_params(n_estimators=cvresult.shape[0])

    # Fit the algorithm on the data
    alg.fit(X, y, eval_metric='auc')

    # Predict training set:
    dtrain_predictions = alg.predict(X)
    dtrain_predprob = alg.predict_proba(X)[:, 1]

    # Print model report:
    print("\nModel Report")
    print("Accuracy : %.4g" % metrics.accuracy_score(y, dtrain_predictions))
    print("AUC Score (Train): %f" % metrics.roc_auc_score(y, dtrain_predprob))

    feat_imp = pd.Series(alg.get_booster().get_fscore()).sort_values(ascending=False)
    feat_imp.plot(kind='bar', title='Feature Importances')
    plt.ylabel('Feature Importance Score')
    plt.show()
    print('n_estimators=', cvresult.shape[0])



def plot_matrix(cm,title_name):
    ax = sn.heatmap(cm,annot=True,fmt='g',xticklabels=['non-rainy', 'rainy'],yticklabels=['non-rainy', 'rainy'])
    ax.set_title(title_name)
    ax.set_xlabel('ground truth')
    ax.set_ylabel('predict')
#warnings.filterwarnings("ignore")  # ignore warning

# load the pre-processed dataset
raw_df= pd.read_csv('/Users/wangjiangyi/Desktop/pre-processed.csv')
temp_y= pd.read_csv('/Users/wangjiangyi/Desktop/weatherAUS.csv')
temp_y.dropna(subset=['RainToday', 'RainTomorrow'], inplace=True)

y = temp_y.RainTomorrow
X = raw_df

# there are 109586 0-class, 31201 1-class in total

# split for training and testing sets
year1 = pd.to_datetime(X.Date).dt.year
year2 = pd.to_datetime(temp_y.Date).dt.year
X.drop(['Date'],axis=1,inplace=True)

X_train = X[year1 < 2015]
X_test = X[year1 >= 2015]

y_train = y[year2 < 2015]
y_test = y[year2 >= 2015]

#there are 76190 0-class, 21798 1-class in training set




#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
# Model training part
# training set: X_train, y_train <=======> X_train_sm, y_train_sm
# testing set: X_test, y_test

lr = LogisticRegression(C=.2, max_iter=5000) # C=.2 vs C=100
ada = AdaBoostClassifier(base_estimator=DecisionTreeClassifier(max_depth=9, min_samples_split=300, min_samples_leaf=3), learning_rate=0.7, n_estimators=400)
gbdt = GradientBoostingClassifier(learning_rate=0.35, loss= 'deviance', max_depth=10, min_samples_leaf=10, min_samples_split= 300, n_estimators= 30, subsample= 0.9)
xgbst = XGBClassifier(learning_rate =0.2, n_estimators=350, max_depth=10,
min_child_weight=2, gamma=0, subsample=0.8,colsample_bytree=0.8,
 objective= 'binary:logistic', nthread=8,scale_pos_weight=1, seed=21)


'''
# Logistic Regression
models = {
    'LogisticRegression': {
        'model': LogisticRegression(max_iter=5000),
        'params': {
            'C': [.2, .5, 1, 2, 5, 10, 15, 20, 50, 100]
        }
    }
}
scores = []

for model_name, mp in models.items():
    gridsearch = GridSearchCV(mp['model'], mp['params'], cv=5, return_train_score=False, scoring = 'accuracy')
    grid_result = gridsearch.fit(X_train, y_train)
    scores.append({
        'model': model_name,
        'best_score': gridsearch.best_score_,
        'best_params': gridsearch.best_params_
    })

    means = grid_result.cv_results_['mean_test_score']
    params = grid_result.cv_results_['params']
    for mean, param in zip(means, params):
        print("%f  with:   %r" % (mean, param))

print(scores)
'''
'''
lr.fit(X_train, y_train)
lr_pred=lr.predict(X_test)
print(confusion_matrix(lr_pred, y_test))
print(lr.score(X_test, y_test))
'''

#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
# Adaboost
'''
models = {
    'AdaBoostClassifier': {
        'model': AdaBoostClassifier(base_estimator=DecisionTreeClassifier(max_depth=6, min_samples_split=400, min_samples_leaf=4)),
        'params': {
            "learning_rate": [0.3, 1],
            "n_estimators": [50,150,400],
        }
    }}
scores_gradboost = []

for model_name, mp in models.items():
    gridsearch = GridSearchCV(mp['model'], mp['params'], cv=5, return_train_score=False, scoring='recall')
    grid_result=gridsearch.fit(X_train, y_train)
    scores_gradboost.append({
        'model': model_name,
        'best_score': grid_result.best_score_,
        'best_params': grid_result.best_params_
    })
    means = grid_result.cv_results_['mean_test_score']
    params = grid_result.cv_results_['params']
    std = grid_result.cv_results_['std_test_score']
    for std, mean, param in zip(std, means, params):
        print("%f  %f  with:   %r" % (std, mean, param))

print(scores_gradboost)


ada.fit(X_train, y_train)
ada_pred=ada.predict(X_test)
print(confusion_matrix(ada_pred, y_test))
print(ada.score(X_test, y_test))

'''
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
# GBDT
'''
models = {
    'GradientBoostingClassifier': {
        'model': GradientBoostingClassifier(),
        'params': {
            "loss": ["deviance"],
            "learning_rate": [0.35],
            "min_samples_split": [150, 300],
            "min_samples_leaf": [5, 10],
            "max_depth": [4, 8, 10],
            "subsample": [.9],
            "n_estimators": [30]
        }
    }}
scores_gradboost = []

for model_name, mp in models.items():
    grid_gbdt = GridSearchCV(mp['model'], mp['params'], cv=5, return_train_score=False, scoring='recall')
    grid_gbdt.fit(X_train, y_train)
    scores_gradboost.append({
        'model': model_name,
        'best_score': grid_gbdt.best_score_,
        'best_params': grid_gbdt.best_params_
    })
    means = grid_gbdt.cv_results_['mean_test_score']
    params = grid_gbdt.cv_results_['params']
    std = grid_gbdt.cv_results_['std_test_score']
    for std, mean, param in zip(std, means, params):
        print("%f  %f  with:   %r" % (std, mean, param))
print(scores_gradboost)
'''
'''
gbdt.fit(X_train, y_train)
gbdt_pred=gbdt.predict(X_test)
print(confusion_matrix(gbdt_pred, y_test))
print(gbdt.score(X_test, y_test))
'''

#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
# XGBoost
'''
models = {
    'XGBClassifier': {
        'model': XGBClassifier(objective= 'binary:logistic'),
        'params': {
            'max_depth': [5],
            "min_child_weight": [1],
            "subsample": [.8],
            'n_estimators': [50],
            'scale_pos_weight' : [1],
            'leanning_rate' : [1000]
        }
    }}
scores_xgb = []

for model_name, mp in models.items():
    grid_xgb = GridSearchCV(mp['model'], mp['params'], cv=5, return_train_score=False, scoring='recall')
    grid_xgb.fit(X_train, y_train)
    scores_xgb.append({
        'model': model_name,
        'best_score': grid_xgb.best_score_,
        'best_params': grid_xgb.best_params_
    })
    means = grid_xgb.cv_results_['mean_test_score']
    params = grid_xgb.cv_results_['params']
    std = grid_xgb.cv_results_['std_test_score']
    for std, mean, param in zip(std, means, params):
        print("%f  %f  with:   %r" % (std, mean, param))
print(scores_xgb)
'''
'''
xgbst.fit(X_train, y_train)
xgb_pred=xgbst.predict(X_test)
print(confusion_matrix(xgb_pred, y_test))
print(xgbst.score(X_test, y_test))
'''
# step 1
#tun_parameters(X_train, y_train)
# step 2
'''
param_test1 = {
  'max_depth':[6,10],
    'min_child_weight': [1,2,3]
}
gsearch1 = GridSearchCV(estimator = XGBClassifier(learning_rate =0.2, n_estimators=350, max_depth=5,
min_child_weight=1, gamma=0, subsample=0.8,colsample_bytree=0.8,
 objective= 'binary:logistic', nthread=8,scale_pos_weight=1, seed=27),
 param_grid = param_test1,scoring='recall',n_jobs=-1, cv=5 )
gsearch1.fit(X_train,y_train)
print(gsearch1.best_score_, gsearch1.best_params_,     gsearch1.best_score_)
means = gsearch1.cv_results_['mean_test_score']
params = gsearch1.cv_results_['params']
std = gsearch1.cv_results_['std_test_score']
for std, mean, param in zip(std, means, params):
    print("%f  %f  with:   %r" % (std, mean, param))
'''
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------

sm=SMOTE(sampling_strategy={0:76190,1:76190})  # should be open
#y_train.index=range(0,97988)
#X_train.index=range(0,97988)
X_train_sm, y_train_sm = sm.fit_resample(X_train, y_train) # should be open



xgbst.fit(X_train_sm, y_train_sm)
xgb_pred=xgbst.predict(X_test)
print(confusion_matrix(xgb_pred, y_test))
print(xgbst.score(X_test, y_test))



plot_matrix(xgbst.score(X_test, y_test),"XGBoost_SMOTE")
plt.show()
