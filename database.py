# Libraries
import websocket, json, pprint, talib, numpy
from binance.enums import *
from datetime import datetime, timedelta
from collections import deque
import pandas as pd
import pandas_ta as ta
import re
from function_principal import*
from functions_support import*
from database import*
from parameters import*



#----------------------------------------------------------------------------------------------------------------
# Falta: conexiones dataset-crear los historios para calcular los EMAS
# database to save hystory transacctions -- WORKING ZONE
backtest_df = pd.DataFrame(columns=['Time', 'Direction', 'Max_val_Pred']) #,'Close','direction','ema10','ema20'
backtest_df_temp= pd.DataFrame(columns=['Time', 'Direction', 'Max_val_Pred']) #,'Close','direction','ema10','ema20'
sql_df = pd.DataFrame()
execute_once = True
temp_execute_once = True
order_direction = ''

