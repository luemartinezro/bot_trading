# Libraries
import websocket, json, pprint, talib, numpy
from binance.enums import *
from datetime import datetime, timedelta
from collections import deque
import pandas as pd
import pandas_ta as ta
import re


# parameters of the bot
json_message = {}
interval_offset_time = 0
ema_10 = deque(maxlen=2)
ema_20 = deque(maxlen=2)
temp_ema_10 = deque(maxlen=2)
temp_ema_20 = deque(maxlen=2)

max_close_value = None
min_close_value = None
profit_risk_up = 0
profit_risk_down = 0

prev_crossed = False
temp_up_crossed = False
in_position = False
temp_in_position = False

#========================================================================================================================
#-------- RISK & Uncertainty Values ----------
RISK = 0.001 # 0.2% temp_diff
#---------------------------------------------
#-------- PROFIT VARIABLES ----------
PROFIT_GAIN = 0.01 # 0.75%
next_profit_limit = 0
prev_profit_limit = 0
#---------------------------------------------
# Trading parameters  --- working zone
ema_count = 0
ema_ref = 10
EMA10 = 10
EMA20 = 20
close_10_interval = 10
close_20_interval = 20
closes_10 = deque(maxlen=close_10_interval)
closes_20 = deque(maxlen=close_20_interval)

#new_row = {}
direction = "UP"
last_ema10 = []
last_ema20 = []
last_pand_ema10 = []
last_pand_ema20 = []