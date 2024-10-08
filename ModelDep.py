import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import json
import numpy as np
import sys
import os
import joblib
import xgboost as xgb
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
import random
import time


class Model():
    def __init__(self):
        self.wd = os.path.dirname(os.path.abspath(__file__))
        file_list ={'XGBoost Model':'XGBoost.pkl' , 'City Label Encoder':'LECity.pkl', 'County Label Encoder':'LECounty.pkl', 'One Hot Encoder':'oheCT04.pkl'}
        dpnds_path = 'dpnds'
        dpnds_path = os.path.join(self.wd,'dpnds')
        fileMissing = False
        if os.path.isdir(dpnds_path):
            self.files = [f for f in os.listdir(dpnds_path) if os.path.isfile(os.path.join(dpnds_path, f))]
        else:
            print ('Dependencies Folder Not Found')
            sys.exit(-1)

        for i in file_list.keys():
            if file_list[i] in self.files:
                print (i, ': Found')
            else:
                print (i,': Not Found')
                fileMissing =True
        if fileMissing:
            print ('Check Missing Dependencies')
            sys.exit(-1)

    def get_dpnds(self):
        file_list = self.files
        dpnds_path = os.path.join(self.wd,'dpnds')
        for i in  file_list:
            if i == 'XGBoost.pkl':
                modelFile = os.path.join(dpnds_path,i)
            elif i == 'LECity.pkl':
                cityLEFile = os.path.join(dpnds_path,i)
            elif i == 'oheCT04.pkl':
                oheCTFile = os.path.join(dpnds_path,i)
            elif i == 'LECounty.pkl':
                countyLEFile = os.path.join(dpnds_path,i)

        try:
            self.model = joblib.load(modelFile)
        except Exception as e:
            print ('Error Downloading Model: ', e)
            sys.exit(-1)
        try:
            self.cityLE = joblib.load(cityLEFile)
        except Exception as e:
            print ('Error Downloading City Label Encoder: ', e)
            sys.exit(-1)
        try:
            self.oheCT = joblib.load(oheCTFile)
        except Exception as e:
            print ('Error Downloading One Hot Encoder: ', e)
            sys.exit(-1)
        try:
            self.countyLE = joblib.load(countyLEFile)
        except Exception as e:
            print ('Error Downloading City Label Encoder: ', e)
            sys.exit(-1)


    def data_encoding(self, df):
        try:
            df['city'] = self.cityLE.transform(df['city'])
        except:
            df['city'] = 0
        try:
            df['county']= self.countyLE.transform(df['county'])
        except:
            df['county']= 0
            
        #print(df.head(1))
        X = df.iloc[:,:]
        #print (X[:,:])
        X = self.oheCT.transform(X)
        return X

    def predict (self, X):
        price = self.model.predict(X)
        price = float(price[0])
        price = np.expm1(price)
        price = round(price, 2)
        return price


