import os
from src.exception import CustomException
from src.logger import logging
import sys
import numpy as np
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.metrics import (mean_absolute_error, 
                             root_mean_squared_error,
                              mean_squared_error,
                              mean_absolute_percentage_error,
                              r2_score)
from src.utils import load_obj
from src.utils import save_obj
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import (
    RandomForestRegressor,
)
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM,Dense,Dropout,Input
from sklearn.model_selection import GridSearchCV
from xgboost import XGBRegressor



from sklearn.tree import DecisionTreeClassifier,DecisionTreeRegressor

from sklearn.linear_model import LogisticRegression


class modelEvoulation:
    def __init__ (self,symbol):
        self.symbol=symbol


    def model_evoulation(self,file_path,Train,Test):
        try:
            logging.info(f"in the model Evoulation {Train.shape}")
            close_idx = Train.columns.get_loc('Close')

            preprocessor=load_obj(file_path)
            preprocessor.fit_transform(Train)
            column_transfer=preprocessor.named_transformers_['colum']  ## columns transformer 
            scaler=column_transfer.named_steps['MinMaxscaler'] #piprline
  
            for days in range (1,8):

                x_train,y_train,x_test,y_test=[],[],[],[] 
                preprocessor=load_obj(file_path) 

                train=preprocessor.fit_transform(Train)
                test=preprocessor.transform(Test)


                def window (data,window=30 ,x=[],y=[]):
                    for i in range(len(data)-window-days ):

                        x.append(data[i:i+window,:])  
                        y.append(data[i+window+days,close_idx])   
                    return np.array(x),np.array(y)  

                x_train,y_train=window(train,30, x_train,y_train)   
                logging.info(f"x.shape = {x_train.shape}   y.shape = {y_train.shape}")  

                model=Sequential([    
                    Input(shape=(x_train.shape[1], x_train.shape[2])),  ##Input(shape=(60,18)),
                    LSTM(64,return_sequences = True),
                    Dropout(0.12),
                    LSTM(32,return_sequences=False),
                    Dropout(0.12),
                    Dense(1),
                ])


                model.compile(optimizer='adam',loss='mse')    

                early_stop = EarlyStopping(
                monitor='val_loss',   # metric to watch
                patience=5,           # stop if no improvement for 5 epochs
                restore_best_weights=True # roll back to best weights
                )
                
                model.fit(x_train,y_train,epochs=100,batch_size=32,validation_split=0.1,verbose=1,callbacks=[early_stop])

                x_test,y_test=window(test,30, x_test,y_test) 
                pred_prices=model.predict(x_test)
                model_path=os.path.join('artifacts',f"{self.symbol}",f"model_{self.symbol}_{days}.pkl")       

                save_obj(obj=model,file_path=model_path)    

                dummy_pred = np.zeros((len(pred_prices), scaler.n_features_in_))
                dummy_true = np.zeros((len(y_test), scaler.n_features_in_))

                dummy_pred[:,3] = pred_prices.ravel()
                dummy_true[:,3] = y_test.ravel()

                pred_prices_real = scaler.inverse_transform(dummy_pred)[:,3]
                y_test_real = scaler.inverse_transform(dummy_true)[:,3] 

                mae  = mean_absolute_error(y_test_real,pred_prices_real)
                rmse = np.sqrt(mean_squared_error(y_test_real, pred_prices_real))
                mape = mean_absolute_percentage_error(y_test_real, pred_prices_real) * 100
                r2   = r2_score(y_test_real, pred_prices_real)
                
                actual_dir = (y_test_real[1:] > y_test_real[:-1])
                pred_dir   = (pred_prices_real[1:]  > pred_prices_real[:-1])
                dir_acc    = (actual_dir == pred_dir).mean() * 100

                logging.info(f"{self.symbol} Day {days} | MAE={mae:.2f} | RMSE={rmse:.2f} | "
                f"MAPE={mape:.2f}% | R²={r2:.4f}  |  DirAcc={dir_acc:.1f}%")     



        except Exception as e:
            raise CustomException(e,sys)  
        








"""  Day1 : [28.5, 65, 12, 0, 1012, ..., 18 values]
Day2 : [29.1, 68, 10, 2, 1010, ..., 18 values]
Day3 : [27.8, 70, 15, 5, 1008, ..., 18 values]
...
Day60: [30.2, 62, 11, 0, 1013, ..., 18 values]"""