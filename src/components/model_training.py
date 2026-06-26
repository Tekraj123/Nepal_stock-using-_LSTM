

import os
from src.exception import CustomException
from src.logger import logging
from sklearn.preprocessing import MinMaxScaler

import sys
from src.utils import load_obj
import pandas as pd
import numpy as np

class modelTranning:

    def __init__(self,symbol):
        self.symbol=symbol
    def model_tranning(self,data_path,preprocessor_path):
        try:
            data=pd.read_csv(data_path)
            data=data[['Open', 'High', 'Low', 'Close', 'VWAP','Vol', "Daily_return","SMA_20","EMA_20","RSI_14","MACD"]]
            
            latest_data = data.tail(30) 
            output=latest_data['Close']
            index = data.columns.get_loc('Close')


            logging.info(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,.............................................")
            logging.info(latest_data.shape)
            stock_predicted_price={ }
            preprocessor=load_obj(preprocessor_path)

            preprocessor.fit_transform(data)  
            prerprocessed_data=preprocessor.transform(latest_data)
           

            column_transfer=preprocessor.named_transformers_['colum']  ## columns transformer 
            scaler=column_transfer.named_steps['MinMaxscaler'] #piprline

            # logging(f"tranning on feature : {scaler.n_features_in_}")
    

            for day in range (1,8):
                # logging.info(f"latest_data.shape  {latest_data.shape}       ,       latest_data.columns {latest_data.columns} ")      
                model_path=os.path.join('artifacts',f"{self.symbol}",f"model_{self.symbol}_{day}.pkl")
                model=load_obj(model_path)  
                prerprocessed_data=prerprocessed_data.reshape(1,30,11)
                predicted_value=model.predict(prerprocessed_data) 
                

                no_feature_use_in_scaler=scaler.n_features_in_ 
                # logging(f"tranning on feature : {no_feature_use_in_scaler}")  

                
                n_sample,n_days=predicted_value.shape
                result=np.zeros_like(predicted_value)

                dummy=np.zeros((n_sample,no_feature_use_in_scaler))
                dummy[:,index]=predicted_value
                inversed =scaler.inverse_transform(dummy)
                result=inversed[:,index]
                stock_predicted_price[f'Day {day}']=result                                    



            logging.info(f"Stock price is {stock_predicted_price}")   
            return stock_predicted_price   

        except Exception as e :
            raise CustomException(e,sys)    