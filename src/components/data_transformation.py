import os
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import sys
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from src.logger import logging
from sklearn.pipeline import Pipeline
from src.exception import CustomException
from src.utils import save_obj


class DataTransformationConfig:
    def __init__(self,symbol):
        self.symbol=symbol
        self.preprocessor_path = os.path.join('artifacts',f'{self.symbol}','preprocessor.pkl') 

class dataTransformation:
         
        def __init__ (self,symbol):
            self.symbol=symbol
            self.preprocessor_path=DataTransformationConfig(symbol)  

         
        def data_transforamtion(self,train_path,test_path):
             try:
               logging.info("entered into the data_transformation")
 
 
               train = pd.read_csv(train_path)
               logging.info(f"the shape of the trained data is {train.shape}") 
               test = pd.read_csv(test_path) 
               logging.info(f"the shape of the test data is {test.shape}")
 
               logging.info("Train Test data read from their path")

               # for day in range(1, 8):
               #      train[f'Target_Day{day}'] = train['Close'].shift(-day)
               #      test[f'Target_Day{day}'] = train['Close'].shift(-day)
                      

               columns= ['Open', 'High', 'Low', 'Close', 'VWAP','Vol', "Daily_return","SMA_20","EMA_20","RSI_14","MACD"]


               pipeline=Pipeline(
                    steps=[
                         ('imputer',SimpleImputer(strategy='median')),
                         ('MinMaxscaler',MinMaxScaler())  
                    ]
               )
 
               logging.info("make the pipeline")

               preprocessor_obj=ColumnTransformer([
                    ('colum',pipeline,columns)
               ])
  
               logging.info("make the conumn transfer ")
  
               save_obj(
                    obj=preprocessor_obj,
                    file_path=self.preprocessor_path.preprocessor_path
               )
  
               logging.info(f"preprocessor for {self.symbol} is saved")

               logging.info(f'....................{preprocessor_obj.transformers}')

               # train_arr=preprocessor_obj.fit_transform(train)

               # logging.info("preprocessed train")
          
               # test_arr=preprocessor_obj.transform(test)

               # logging.info("preprocessed train")

               # logging.info('test arr shape ',test_arr.shape) 

               return (
                    self.preprocessor_path.preprocessor_path,
                    train,
                    test,
               )  
             
             except Exception as e :
                  raise CustomException (e,sys)
          







"""
Your pipeline structure nesting path

Your scaler is nested 3 levels deep — ColumnTransformer -> pipeline -> MinMaxscaler

[preprocessor_obj] (ColumnTransformer) -> ['colum'] (transformer name) -> [pipeline] (Pipeline object) -> ['MinMaxscaler'] (your step name) -> [MinMaxScaler()] (actual scaler)"""



"""
# Step 1: get the pipeline from ColumnTransformer
# 'colum' is the name you gave in ColumnTransformer([('colum', pipeline, columns)])

col_pipeline = preprocessor_obj.named_transformers_['colum']

# Step 2: get the scaler from the pipeline
# 'MinMaxscaler' is the name you gave in Pipeline steps

scaler = col_pipeline.named_steps['MinMaxscaler']

print(type(scaler))           # MinMaxScaler
print(scaler.n_features_in_)  # number of columns you trained on
print(scaler.feature_names_in_) # column names (if trained on DataFrame)


"""











