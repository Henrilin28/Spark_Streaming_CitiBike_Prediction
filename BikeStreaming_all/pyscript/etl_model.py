import pysparkß
import pandas as pd
import numpy as np
import feather
from sklearn import linear_model
from sklearn import cross_validation
from sklearn import preprocessing
from sklearn import metrics
import folium
from folium import plugins
import matplotlib.pyplot as plt
import seaborn as sns
import glob as glob
from datetime import date, timedelta, datetime, time
from sklearn.svm import SVR
from sklearn.metrics import roc_auc_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import TimeSeriesSplit
from sklearn import cross_validation, linear_model
from sklearn.externals import joblib




def mean_absolute_percentage_error(y_true, y_pred):

    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100



file_route = '/Users/Henrilin28/Dropbox/BDA/Citi-Bike-Analysis/data/Citibike/2016*.csv'
all_file= glob.glob(file_route)


def formatted(x):

    df = pd.read_csv(x)
    df.columns = [col.lower().replace(' ','') for col in df.columns.values]
    return df


def roundTime(dt=None, dateDelta=timedelta(minutes=15)):

    roundTo = dateDelta.total_seconds()

    if dt == None : dt = datetime.now()
    seconds = (dt - dt.min).seconds
    # // is a floor division, not a comment on following line:
    rounding = (seconds+roundTo/2) // roundTo * roundTo
    return (dt + timedelta(0,rounding-seconds,-dt.microsecond)).strftime('%Y-%m-%d-%H-%M')

bikedata = pd.concat([formatted(i) for i in all_file])
bikedata['starttime'] = pd.to_datetime(bikedata['starttime'], format="%m/%d/%Y %H:%M:%S",
                                 errors="coerce")
bikedata['stoptime'] = pd.to_datetime(bikedata['stoptime'], format="%m/%d/%Y %H:%M:%S",
                                 errors="coerce")

bikedata = bikedata.dropna(subset=['stoptime', 'starttime'])
bikedata['stopdatehour'] = bikedata.stoptime.apply(roundTime)
bikedata['stopdatehour'] = bikedata.stoptime.apply(lambda x:x.strftime('%Y-%m-%d-%H-%M'))
bikedata['startdatehour'] = bikedata.starttime.apply(lambda x:x.strftime('%Y-%m-%d-%H'))
dfStart = bikedata.groupby(by=['startdatehour','startstationid'])['bikeid'].size().sort_values(ascending=False)
dfEnd = bikedata.groupby(by=['stopdatehour', 'endstationid'])['bikeid'].size().sort_values(ascending=False)
df_12 = pd.merge(dfStart.reset_index(), dfEnd.reset_index(),
         left_on=['startdatehour', 'startstationid'],
                 right_on = ['stopdatehour','endstationid'], how='outer')
df_12 = df_12.dropna()
df_12['net_value'] = df_12.bikeid_x.fillna(0) - df_12.bikeid_y.fillna(0)
df_12 = df_12.drop(['startdatehour','startstationid', "bikeid_x", "bikeid_y"], 1).set_index(['stopdatehour', 'endstationid'])
clean_frame2 = dfEnd_15.reset_index().groupby(['stopdatehour', 'endstationid'])['bikeid'].sum()
target2 = clean_frame2.unstack().fillna(0).shift(2)
target2.columns = [str(int(col))+'_nxt15' for col in target2.columns.values]
features2 = clean_frame2.unstack().fillna(0)
features2.columns = [str(int(col)) for col in features2.columns.values]
final_data2 = features2.join(target2).dropna()
df = pd.read_csv('/Users/Henrilin28/Documents/merge_id.csv')
merged_station = df.columns.values
merged_station = [s.strip()for s in merged_station]
merged_station_pred = [s +'_nxt15' for s in merged_station]
merged_station = merged_station + merged_station_pred
merged = final_data2[merged_station]


splits = TimeSeriesSplit(n_splits=3)
X = merged.iloc[:, :598]
Y = merged.iloc[:, 598:]

splits = TimeSeriesSplit(n_splits=3)

models=[]
score=[]
for train, test in split(X):
    sample_leaf_options = [100,200,500]
    for leaf_size in sample_leaf_options :
        model = RandomForestRegressor(n_estimators= 10, oob_score = True,
                                    n_jobs = 30, random_state =50,
                                    max_features = "auto", min_samples_leaf = leaf_size)
        model.fit(X[train],Y[train])
        score.append(model.score(X[test], Y[test]))
        models.append(model)

final_model = models[np.argmax(score)]





filename = './model/rf_model3.sav'
joblib.dump(model, filename)






