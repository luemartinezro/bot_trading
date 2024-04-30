# Libraries
import websocket, json, pprint, talib, numpy
from binance.enums import *
from datetime import datetime, timedelta
from collections import deque
import pandas as pd
import pandas_ta as ta
import re
from functions_support import *
import database 
from parameters import *



# Central code of bot
def on_open(ws):
    """
    Callback function for when the connection is opened.

    Args:
        ws: WebSocket connection object.

    Global Variables Used:
        closes_10 (list): List of closing prices for 10-period.
        closes_20 (list): List of closing prices for 20-period.
        max_value (float): Maximum value.
        RISK (float): Risk factor.
        PROFIT_GAIN (float): Profit gain factor.
    """
    global closes_10, closes_20, max_value, RISK, PROFIT_GAIN
    
    print('opened connection')
    print("[INFO] Risk = {} ProfitGain = {}".format(RISK, PROFIT_GAIN))

def on_close(ws):
    """
    Callback function for when the connection is closed.

    Args:
        ws: WebSocket connection object.
    """
    print('closed connection')

def on_message(ws, message):
    """
    Callback function for when a message is received.

    Args:
        ws: WebSocket connection object.
        message (str): The received message.
    """
    global closes, ema_10, ema_20, temp_ema_10, temp_ema_20, temp_in_position, temp_up_crossed, direction, enter_time, temp_position_close, next_profit_limit, prev_profit_limit, ema_count

    try:
        json_message = json.loads(message)
        candle = json_message['k']
        close = float(candle['c'])
        is_candle_closed = candle['x']

        temp_last_ema_10 = calculates_ema(close, 10, 2, temp_ema_10)
        temp_last_ema_20 = calculates_ema(close, 20, 2, temp_ema_20)
        print("\r", "Price = {}, TEMP_EMA10 = {} TEMP_EMA20 = {}".format(candle['c'], temp_last_ema_10, temp_last_ema_20), end="")

        if is_candle_closed:
            ts = int((candle['T'])/100) + 1
            time = (datetime.now() - interval_offset_time).strftime("%m/%d/%Y %H:%M:%S")
            print("\n", "candle closed at {} in time = {}".format(close, time), end="")
            ema_10.append(temp_last_ema_10)
            ema_20.append(temp_last_ema_20)
            temp_ema_10.append(temp_last_ema_10)
            temp_ema_20.append(temp_last_ema_20)
            print("\n\t CLOSE EMA10 = {}".format(temp_ema_10[-1]))
            print("\t CLOSE EMA20 = {}".format(temp_ema_20[-1]))
            print("\n", "----------------------------------------")

            if temp_last_ema_10 > temp_last_ema_20 and not temp_up_crossed:                        
                if not temp_in_position and ema_count >= ema_ref:
                    direction = 'UP'                    
                    enter_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
                    temp_position_close = close
                    next_profit_limit = temp_position_close * (1 + PROFIT_GAIN)
                    prev_profit_limit = temp_position_close * (1 - RISK)
                    print("\n", "[INFO ENTRY UP] close {} enter_time = {} prev_profit_limit {} next_profit_limit {} ".format(close, enter_time, prev_profit_limit, next_profit_limit ))
                    uncer_count = 0
                    temp_in_position = True
                    temp_up_crossed = True
                    ema_count = 0

            elif temp_last_ema_10 < temp_last_ema_20 and temp_up_crossed:            
                if not temp_in_position and ema_count >= ema_ref:      
                    direction = 'DOWN'
                    enter_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")                    
                    temp_position_close = close 
                    next_profit_limit = temp_position_close * (1 - PROFIT_GAIN) 
                    prev_profit_limit = temp_position_close * (1 + RISK)
                    print("\n", "[INFO ENTRY DOWN] close {} enter_time = {} prev_profit_limit {} next_profit_limit {} ".format(close, enter_time, prev_profit_limit, next_profit_limit ))
                    temp_in_position = True
                    temp_up_crossed = False
                    ema_count = 0

    except Exception as e:
        print(" [ERROR]", e)


                

