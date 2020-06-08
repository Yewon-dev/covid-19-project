# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 00:47:59 2020

@author: user
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

from datetime import date, timedelta

## 누적 확진자 구하기
# lightcoral orange gold yellowgren mediumturquoise plum

print(os.getcwd())
path = 'desktop/covid-19-project/dataset/'

case = pd.read_csv(path+ 'Case02.csv')
accum = pd.read_csv(path+'Time02.csv')
info = pd.read_csv(path+'PatientInfo02.csv')
shincheon = pd.read_csv(path + 'shincheon.csv')
diff = pd.read_csv(path + 'daily_diff.csv')

accum.head()


floating_01 = pd.read_csv(path + 'CARD_SUBWAY_MONTH_202001.csv', encoding = 'cp949')
floating_02 = pd.read_csv(path + 'CARD_SUBWAY_MONTH_202002.csv')
floating_03 = pd.read_csv(path + 'CARD_SUBWAY_MONTH_202003.csv')
floating_04 = pd.read_csv(path + 'CARD_SUBWAY_MONTH_202004.csv')

subway_01 = floating_01.groupby('사용일자')['승차총승객수'].sum()
subway_02 = floating_02.groupby('사용일자')['승차총승객수'].sum()
subway_03 = floating_03.groupby('사용일자')['승차총승객수'].sum()
subway_04 = floating_04.groupby('사용일자')['승차총승객수'].sum()

#lightcoral orange gold

# 자료 합치기
seoul_floating = pd.concat([subway_01, subway_02, subway_03, subway_04]).reset_index()

## 첫 확진자부터 5월31일까지 그래프

plt.rc('font', family ='Malgun Gothic')
plt.figure(figsize=(15,5))
plt.title('1월부터 5월까지 누적확진자 수')
plt.plot(accum['date'], accum['confirmed'], color='lightcoral', label='누적 확진자 수')

## 신천지 누적

plt.plot(accum['date'], shincheon['accum_num'], color = 'orange', label = '신천지 확진자 수')

## 신천지 누적 빼기
pure_confirm = list(accum['confirmed'] - shincheon['accum_num'])
plt.plot(accum['date'],pure_confirm, color = 'yellowgreen', label = '신천지 제외 확진자 수')


plt.plot([accum['date'][accum[accum['date']=='2020-03-22'].index[0]],
          accum['date'][accum[accum['date']=='2020-03-22'].index[0]]],[0,15000],color='orange',marker='^', label='사회적 거리두기')
plt.plot([accum['date'][accum[accum['date']=='2020-01-20'].index[0]],
          accum['date'][accum[accum['date']=='2020-01-20'].index[0]]],[0,15000],color='gold',marker='^', label='국내 첫 확진자')
plt.plot([accum['date'][accum[accum['date']=='2020-02-18'].index[0]],
          accum['date'][accum[accum['date']=='2020-02-18'].index[0]]],[0,15000],color='yellowgreen',marker='^', label='신천지 확진자 발생')

plt.plot(diff['Date'],diff['Confirmed'],color='gold',label = '전체 일별 확진자 수')

plt.xticks(accum['date'][0::5])
plt.gcf().autofmt_xdate()
plt.legend()
plt.show()

## 일별 확진자 수 그래프
plt.figure(figsize=(15,5))
plt.title('일별 확진자 수')

plt.plot(diff['Date'],diff['Confirmed'],color='gold',label = '전체 일별 확진자 수')

## 신천지 제외한 일별 확진자 수
pure_daily = list(diff['Confirmed'] - shincheon['num'])
plt.plot(diff['Date'], pure_daily, color='mediumturquoise', label = '신천지 제외 일별 확진자 수')

plt.xticks(diff['Date'][0::10])
plt.gcf().autofmt_xdate()
plt.legend()
plt.show()



### 신천지 patient_id 얻기

shin = list(info.patient_id[info.infection_case=='Shincheonji Church'])
##jupyter notebook 확인


# =============================================================================
# LogisticRegression 이용하여 예측
# =============================================================================

import pandas as pd 

data = pd.read_csv(path + 'Time02.csv') 
tc = data['confirmed']
tt = data['test']
y = []
tt_increase = []

for i in range(1, len(tt)):
    current_epi = ((tc[i] - tc[i-1])/(tt[i]-tt[i-1]))*100
    tt_increase.append(tt[i]-tt[i-1])
    y.append(current_epi)

data['date']
y

X = []
for i in range(1, len(y)+1):
    X.append([i])


# 사회적 거리두기 시행
di = 62
restrictions_x = [di,di,di,di,di,di]
restrictions_y = [0,10,20,30,40,50]

# 사회적 거리두기 시행 후 일주일
de = di + 7
effects_x = [de,de,de,de,de,de]
effects_y = [0,10,20,30,40,50]
de

import matplotlib.pyplot as plt

plt.rc('font', family ='Malgun Gothic')
plt.figure(figsize=(10,5))
plt.scatter(X, y,  color='black')
plt.plot(restrictions_x,restrictions_y, color='red', linewidth=2, label='사회적 거리두기 시행')
plt.plot(effects_x,effects_y, color='green', linewidth=2, label='사회적 거리두기 시행 7일 후')
plt.grid()
plt.xlabel('Days')
plt.xlim(41,100)
plt.ylim(0,20)
plt.xticks([40,50,60,70,80,90,100,110,120,130],
           data['date'][41::10])

plt.gcf().autofmt_xdate()
plt.legend()
plt.show()

import numpy as np
from sklearn import linear_model

# 3월 이후 데이터
X = X[de:]
y = y[de:]

print(X)
# Linear Regression
linear_regr = linear_model.LinearRegression()

# Train the model using the training sets
linear_regr.fit(X, y)

# 정확도
score = linear_regr.score(X,y)
print("score :",score)

from sklearn.metrics import max_error
import math

y_pred = linear_regr.predict(X)
error = max_error(y, y_pred)
error

X_test = []

gp = 50

for i in range(de, de + gp):
    X_test.append([i])

y_pred_linear = linear_regr.predict(X_test)

y_pred_max = []
y_pred_min = []

for i in range(0, len(y_pred_linear)):
    y_pred_max.append(y_pred_linear[i] + error)
    y_pred_min.append(y_pred_linear[i] - error)
    
from datetime import datetime
from datetime import timedelta  

data_eff = datetime.strptime(data['date'][de], '%Y-%m-%d')

# date previsione
date_prev = []
x_ticks = []
step = 5
data_curr = data_eff
x_current = de
n = int(gp/step)
for i in range(0, n):
    date_prev.append(str(data_curr.day) + "/" + str(data_curr.month))
    x_ticks.append(x_current)
    data_curr = data_curr + timedelta(days=step)
    x_current = x_current + step


plt.grid()
plt.scatter(X, y,  color='black')

plt.plot(X_test, y_pred_linear, color='green', linewidth=2, label='예측 값')
plt.plot(X_test, y_pred_max, color='red', linewidth=1, linestyle='dashed', label='최대 오류 값')
plt.plot(X_test, y_pred_min, color='red', linewidth=1, linestyle='dashed')

plt.xlabel('Days')
plt.xlim(de,de+gp)

plt.xticks(x_ticks, date_prev)
plt.yscale("log")

plt.savefig("prediction.png")
plt.gcf().autofmt_xdate()
plt.legend()
plt.show()