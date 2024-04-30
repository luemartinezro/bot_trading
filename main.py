# Libraries
import websocket, json, pprint, talib, numpy
from binance.enums import *
from datetime import datetime, timedelta
from collections import deque
import pandas as pd
import pandas_ta as ta
import re
from function_principal import *
from functions_support import *
from  database import *
from parameters import *


if __name__ == "__main__":
    # parameters to modifiy: temporality and cripto 
    print("[COMMENT] DONE.")
    interval = "1m"   # temporality: 1m, 5m, 15m, 30m, 1h
    interval_offset_time = interval_offset(interval)
    ticker = "adausdt"   # cripto 
    SOCKET = "wss://stream.binance.com:9443/ws/" + ticker + "@kline_"+ interval    # socket to catch data

    prev_ema_10 = 30.95
    prev_ema_20 = 30.93
    RISK = 0.001 # 0.2%
    PROFIT_GAIN = 0.01
    print("[INFO] RISK = {} %".format(RISK * 100.0))
    print("[INFO] Profit GAIN = {} %".format(PROFIT_GAIN * 100.0))

    ema_10.append(prev_ema_10)
    ema_20.append(prev_ema_20)
    temp_ema_10.append(prev_ema_10)
    temp_ema_20.append(prev_ema_20)

    ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
    ws.run_forever()


