#==============================================================================================================
# Libraries
import websocket, json, pprint, talib, numpy
from binance.enums import *
from datetime import datetime, timedelta
from collections import deque
import pandas as pd
import pandas_ta as ta
import re


### Functions
def interval_offset(interval):
    """
    Computes the offset based on the provided interval.

    Args:
        interval (str): The time interval in the format of '[number][unit]', e.g., '1m' for 1 minute.

    Returns:
        pd.DateOffset: A Pandas DateOffset object representing the offset.
    """
    regex = "(\d+)(\w+)"
    match = re.search(regex, interval) 
    if match[2] == "m":
        return pd.DateOffset(minutes=int(match[1]))
    else:
        return pd.DateOffset(minutes=0)

def calculates_ema(close, period, smoothing, ema_list):
    """
    Calculate Exponential Moving Average.

    Args:
        close (float): Current closing price.
        period (int): EMA period.
        smoothing (int): Smoothing factor.
        ema_list (list): List of previous EMA values.

    Returns:
        float: Calculated EMA.
    """
    # Implementation of EMA calculation
    return ema_list[-1] * (1 - smoothing / (1 + period)) + close * (smoothing / (1 + period))


def ret_ema(prev_closes, period, lib='TA'):    
    """
    Computes Exponential Moving Average (EMA) based on the given closing prices and library.

    Args:
        prev_closes (list): List of previous closing prices.
        period (int): Period for EMA calculation.
        lib (str): Library to use for EMA calculation ('TA' or 'PANDAS').

    Returns:
        float: Last EMA value.
    """
    np_closes = np.array(prev_closes)    
    if lib == 'TA':
        ema = talib.EMA(np_closes, period)
    elif lib =='PANDAS':
        holder = pd.DataFrame(np_closes, columns=['close'])
        ema = ta.ema(holder['close'], length=period)    
    last_ema = ema.iloc[-1]
    return last_ema

def time_select(interval, ema10, ema20):
    """
    Selects time based on the provided intervals and EMA values.

    Args:
        interval (str): The time interval ('1m', '5m', '15m', '30m', '1h').
        ema10 (float): EMA value for 10-period.
        ema20 (float): EMA value for 20-period.

    Returns:
        tuple: A tuple containing the time strings for EMA10 and EMA20.
    """
    now = datetime.now()
    now_time = now.strftime("%d-%m-%Y %H:%M")
    categories_ema10 = {
        '1m': timedelta(minutes=ema10*1),
        '5m': timedelta(minutes=ema10*5),
        '15m': timedelta(minutes=ema10*15),
        '30m': timedelta(minutes=ema10*30),
        '1h': timedelta(hours=ema10)    
    }
    categories_ema20 = {
        '1m': timedelta(minutes=ema20*1),
        '5m': timedelta(minutes=ema20*5),
        '15m': timedelta(minutes=ema20*15),
        '30m': timedelta(minutes=ema20*30),
        '1h': timedelta(hours=ema20)    
    }
    EMA10_time = now - categories_ema10[interval]
    EMA20_time = now - categories_ema20[interval]
    EMA10_time_str = EMA10_time.strftime("%m-%d-%Y %H:%M")
    EMA20_time_str = EMA20_time.strftime("%m-%d-%Y %H:%M")
    return EMA10_time_str, EMA20_time_str

def execute_func(M10, M20, execute_once=False, prev_crossed=None):
    """
    Executes a function based on certain conditions.

    Args:
        M10 (float): EMA10 value.
        M20 (float): EMA20 value.
        execute_once (bool): Flag to execute only once (default False).
        prev_crossed (bool): Previous crossed value.

    Returns:
        bool: Updated prev_crossed value.
    """
    if execute_once:            
        print("\n", "oka")
        print("\n", "Define Direction", end="")
        if M20 > M20:
            prev_crossed = True
            print("\n", "Downtrend")                 
            execute_once = False
        elif M20 < M20:
            prev_crossed = False
            print("\n", "Uptrend")                 
            execute_once = False
    return prev_crossed
    
def order(side, quantity, symbol, order_type='ORDER_TYPE_MARKET'):
    """
    Places an order.

    Args:
        side (str): Side of the order ('BUY' or 'SELL').
        quantity (float): Quantity of the asset.
        symbol (str): Symbol of the asset.
        order_type (str): Type of order (default 'ORDER_TYPE_MARKET').

    Returns:
        bool: True if order is successfully sent, False otherwise.
    """
    try:
        print("sending order")
        print(order)
    except Exception as e:
        print("an exception occurred - {}".format(e))
        return False

    return True

def backtest(enter_date, enter_price, exit_date, exit_price, direction='Test', pred_max_value=-1, ticks=-1, ticker='', temp=False, operation_type='Test'):    
    """
    Conducts backtesting.

    Args:
        enter_date (str): Enter date.
        enter_price (float): Enter price.
        exit_date (str): Exit date.
        exit_price (float): Exit price.
        direction (str): Direction ('U' for uptrend, 'D' for downtrend, 'Test' for testing) (default 'Test').
        pred_max_value (float): Predicted maximum value.
        ticks (int): Number of ticks.
        ticker (str): Ticker symbol.
        temp (bool): Flag for temporary backtesting.
        operation_type (str): Type of operation (default 'Test').
    """
    global backtest_df, max_value, backtest_df_temp, sql_df, new_row
    
    current_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    profit = 0
    if direction == 'UP':
        profit = (exit_price / enter_price) - 1
    elif direction == 'DOWN':
        profit = 1 - (exit_price / enter_price)
    else:
        profit = -1       
    new_row = {'EnterDate': enter_date,
               'ExitDate': exit_date,
               'EnterPrice': enter_price,               
               'ExitPrice': exit_price, 
               'Direction': direction,
               'Profit': profit,
               'MaxValue': pred_max_value, 
               'Ticks': ticks,
               'Ticker': ticker,
               'OperationType': operation_type,
               'CurrentTime': current_time
              }    
    if temp:        
        print("\n SAVED at direction {}".format(direction))
        df = pd.DataFrame(new_row, index=[''])
        backtest_df_temp= backtest_df_temp.append(new_row, ignore_index=True)
        print("\r", "[DATA] Insert Succesfull", end="")
    else:
        backtest_df= backtest_df.append(new_row, ignore_index=True)    
