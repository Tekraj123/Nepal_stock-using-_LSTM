from src.components.data_ingestion import DataIngestion
import os 
from src.logger import logging
import pandas as pd
from src.utils import load_obj
from src.components.model_training import modelTranning
from src.exception import CustomException
import sys

class predictionPipeline:
    def __init__(self,symbol):
        self.symbol=symbol
        self.preprocessor_path = os.path.join('artifacts',f'{self.symbol}','preprocessor.pkl') 
        self.data_path = os.path.join('artifacts', f"{self.symbol}" , f"{self.symbol}_data.csv")

    try:
        def predict (self):
            model_obj=modelTranning(self.symbol)
            predicted_price=model_obj.model_tranning(data_path=self.data_path,preprocessor_path=self.preprocessor_path)
            logging.info(f"the type of the return is {type(predicted_price)}")
            return predicted_price
        
    except Exception as e:
        raise CustomException (e,sys)


        
        
if __name__ == "__main__":
    obj=predictionPipeline("NABIL")
    price=obj.predict()
    logging.info (f"price is {price}")



        






