# -*- coding: utf-8 -*-
"""
Created on Thu Feb 09 13:48:55 2017

@author: Administrator
"""

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import random
import sys
from sklearn.preprocessing import PolynomialFeatures
sys.path.append('../tools')
from tools import *

random.seed(1)

weekA = pd.read_csv('../train/weekABCD/weekA.csv'); weekA.index=weekA.shop_id
weekB = pd.read_csv('../train/weekABCD/weekB.csv'); weekB.index=weekB.shop_id
weekC = pd.read_csv('../train/weekABCD/weekC.csv'); weekC.index=weekC.shop_id
weekD = pd.read_csv('../train/weekABCD/weekD.csv'); weekD.index=weekD.shop_id

poly = PolynomialFeatures(3,interaction_only=True)

train_x = (pd.merge(weekA,weekB,on='shop_id')).drop('shop_id',axis=1)       #train = weekA + weekB
train_sum = train_x.sum(axis=1)
train_mean = train_x.mean(axis=1)
train_weekend = ['2016-09-24 00:00:00','2016-09-25 00:00:00','2016-10-15 00:00:00','2016-10-16 00:00:00']
train_ratio_wk = (train_x[train_weekend]).sum(axis=1)/(train_sum.replace(0,1))
train_open_ratio_wkA = every_shop_open_ratio(start_day=447,end_day=453)
train_open_ratio_wkB = every_shop_open_ratio(start_day=468,end_day=474)
train_open_ratio = (train_open_ratio_wkA.open_ratio + train_open_ratio_wkB.open_ratio)/2

train_x = transfrom_Arr_DF(poly.fit_transform(train_x)) #将其中的日期生成多项式
train_x['sumABCD'] = train_sum    #加入总数
train_x['meanABCD'] = train_mean     #加入平均数
train_x['ratio_wk'] = train_ratio_wk  #周末占总量的比例
train_x['open_ratio_ABCD'] = train_open_ratio.values    #加入开业比例

train_y = weekD.drop('shop_id',axis=1)

#-----------------------------------------------------------------------------------------------------------------------------------------------------
test_x = (pd.merge(weekB,weekC,on='shop_id')).drop('shop_id',axis=1)    #test = weekC + weekD
test_sum = test_x.sum(axis=1)
test_mean = test_x.mean(axis=1)
test_weekend = ['2016-10-15 00:00:00','2016-10-15 00:00:00','2016-10-22 00:00:00','2016-10-23 00:00:00']
test_ratio_wk = (test_x[test_weekend]).sum(axis=1)/(test_sum.replace(0,1))
test_open_ratio = every_shop_open_ratio(start_day=468,end_day=481)

test_x = transfrom_Arr_DF(poly.fit_transform(test_x))
test_x['sumABCD'] = test_sum
test_x['meanABCD'] = test_mean
test_x['ratio_wk'] = test_ratio_wk
test_x['open_ratio_ABCD'] = test_open_ratio.open_ratio

test_y = weekD.drop('shop_id',axis=1)


RF = RandomForestRegressor(n_estimators=500,random_state=1,n_jobs=-1,min_samples_split=2,min_samples_leaf=2,max_depth=25)
RF.fit(train_x,train_y)
pre = (RF.predict(test_x)).round()
score =calculate_score(pre,test_y.values)
print score