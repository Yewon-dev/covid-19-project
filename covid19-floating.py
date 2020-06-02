# -*- coding: utf-8 -*-
"""
Created on Tue May 26 22:03:45 2020

@author: user
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1월 ~ 5월 유동인구 구하기
# 일별 지하철 승차 승객
print(os.getcwd())
path = "dataset/"

floating_01 = pd.read_csv(path + 'CARD_SUBWAY_MONTH_202001.csv', encoding = 'cp949')
floating_02 = pd.read_csv(path + 'CARD_SUBWAY_MONTH_202002.csv')
floating_03 = pd.read_csv(path + 'CARD_SUBWAY_MONTH_202003.csv')
floating_04 = pd.read_csv(path + 'CARD_SUBWAY_MONTH_202004.csv')

subway_01 = floating_01.groupby('사용일자')['승차총승객수'].sum()
subway_02 = floating_02.groupby('사용일자')['승차총승객수'].sum()
subway_03 = floating_03.groupby('사용일자')['승차총승객수'].sum()
subway_04 = floating_04.groupby('사용일자')['승차총승객수'].sum()



# 자료 합치기
seoul_floating = pd.concat([subway_01, subway_02, subway_03, subway_04]).reset_index()

# 그래프로 나타내기

seoul_floating['사용일자'] = seoul_floating['사용일자'].apply(lambda x: pd.to_datetime(str(x),format='%Y%m%d'))

plt.rc('font', family ='Malgun Gothic')
plt.figure(figsize=(20,5))
plt.title('1월부터 4월까지 일별 지하철 이용 승객수')
plt.plot_date(seoul_floating['사용일자'], seoul_floating['승차총승객수'], fmt='c*-', label='승차 총 승객수')
plt.xticks(seoul_floating['사용일자'][0::5])
plt.gcf().autofmt_xdate()

plt.plot([seoul_floating['사용일자'][seoul_floating[seoul_floating['사용일자']=='2020-03-22'].index[0]],
          seoul_floating['사용일자'][seoul_floating[seoul_floating['사용일자']=='2020-03-22'].index[0]]],[0,9000000],lw=5, c='r', label='사회적 거리두기')
plt.plot([seoul_floating['사용일자'][seoul_floating[seoul_floating['사용일자']=='2020-01-20'].index[0]],
          seoul_floating['사용일자'][seoul_floating[seoul_floating['사용일자']=='2020-01-20'].index[0]]],[0,9000000],lw=5, c='y', label='국내 첫 확진자')
plt.plot([seoul_floating['사용일자'][seoul_floating[seoul_floating['사용일자']=='2020-02-18'].index[0]],
          seoul_floating['사용일자'][seoul_floating[seoul_floating['사용일자']=='2020-02-18'].index[0]]],[0,9000000],lw=5, c='g', label='신천지 확진자 발생')
#plt.plot([seoul_floating['사용일자'][seoul_floating[seoul_floating['사용일자']=='2020-05-06'].index[0]],
#          seoul_floating['사용일자'][seoul_floating[seoul_floating['사용일자']=='2020-05-06'].index[0]]],[0,9000000],lw=5, c='r', label='이태원 클럽 확진자 양성 판정')
#plt.bar(seoul_floating[seoul_floating['사용일자']=='2020-04-05 00:00:00'], height=[0,9000000], width=0.8, c='o', label='사회적 거리두기 연장')
#plt.bar(seoul_floating[seoul_floating['사용일자']=='2020-04-20 00:00:00'], height=[0,9000000], width=0.8, c='r', label='생활속 거리두기')
plt.legend()
plt.show()

# 주별 평균 이용 고객 수
'''
seoul_week = []
for row in seoul_floating:
    for i in row:
        seoul_week[i] = seoul_floating[i::7].sum()
'''