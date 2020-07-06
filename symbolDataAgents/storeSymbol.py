#   ///////////////////////////////////////////////////////////////////////
#   Author: KAL GANDIKOTA
#  #
#   Kal’s bnsig is a Python program to interface with binanceus exchange
#   pull the data and analyze the data through Technical Analysis Algorithms
#   Copyright (C) NOV 2019 KAL GANDIKOTA
#  #
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#  #
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#  #
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  #
#   Please Kindly Donate for my Daily Expenses and Greater Works Than These
#  #
#   BTC Wallet: 1NeDC1GvpFa49DFLuT1v28ohFjqtoWXNQ5
#   ETH Wallet: 0x35e557F39A998e7d35dD27c6720C3553e1c65053
#   NEO Wallet: AUdiNJDW7boeUyYYNhX86p2T8eWwuELSGr
#   SteemID: chipmaker
#   https://www.twitter.com/chipmaker_tweet
#   https://steemit.com/@chipmaker
#   https://www.tradingview.com/u/KalGandikota/
#   ///////////////////////////////////////////////////////////////////////

import shutil
import pandas as pd
import glob, os
import logging
import time
import sys
import pandas_market_calendars as mcal
import asyncio
from Utils.helpers import *
from Utils.mylogger import *

class storeSymbol(object):
    def whoami(self):
        print('{}'.format(type(self).__name__))

    def __init__(self):
        """Constructor for $class$"""
        #print('Inside SYMBOL_DATA CONSTRUCTOR{}'.format(type(self).__name__))

    @property
    def symbol(self):
        return self.symbol_str

    @symbol.setter
    def symbol(self, sym):
        self.symbol_str = sym
        self.symbol_out = sym.replace("/", "")

    @property
    def timeframe(self):
        return self.tframe

    @timeframe.setter
    def timeframe(self, tf):
        self.tframe = tf
        self.current_interval = interval_to_milliseconds(tf)
        self.update_interval = interval_to_seconds(tf)

    def run(self, fd):
        #self.store_symbol(fd)
        pass

    def store_symbol(self, fd):
        #print ("Inside Store Symbol {}".format(Config2tf.exchange))
        # Check if the symbol is available on the Exchange
        #if Config2tf.symbol not in self.exchange.symbols:
        #    print('-' * 36, ' ERROR ', '-' * 35)
        #    print('The requested symbol ({}) is not available from {}\n'.format(Config2tf.symbol, Config2tf.exchange_str))
        #    print('Available symbols are:')
        #    for key in Config2tf.exchange.symbols:
        #        print('  - ' + key)
        #    print('-' * 80)
        #    quit()

        # Get data
        exchange_rateLimit = fd['exchange_rateLimit']
        exchange = fd['exchange']
        exchangeStr = fd['exchangeStr']
        symbol = fd['symbol']
        timeframe = fd['timeframe']
        dump_filename_path = fd['dump_filename_path']
        try:
            time.sleep(exchange_rateLimit)
            barset = exchange.get_barset(symbol, timeframe, limit=300)
            mylist = []
            for bar in barset[symbol]:
                mydict = {}
                mydict['Timestamp'] = date_to_milliseconds(str(bar.t))
                mydict['Open'] = bar.o
                mydict['High'] = bar.h
                mydict['Low'] = bar.l
                mydict['Close'] = bar.c
                mydict['Volume'] = bar.v
                mydict['normal_time'] = tz_from_utc_ms_ts(mydict['Timestamp'])
                mylist.append(mydict)

            #############startexp#############
            #df = pd.DataFrame(data)
            #columns = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
            #df.to_csv(Config2tf.temp_dump_filename_path, index=False, header=columns)
            #quit()
            ####################END##############
            #logger.info("After fetch_ohlcv in store_symbol. Symbol={}".format(Config2tf.symbol))
            df = pd.DataFrame(mylist)
            if (df.size== 0):
                print('Inside Store Symbol. DF of {} is empty. Quitting'.format(symbol))
                quit()
            else:
                df.to_csv(dump_filename_path, index=False)
            return df
        except:
            #logging.warning("Unexpected error: {}", sys.exc_info()[0])
            logger.warning("Unexpected error: Exchange={}, symbol={}".format(exchangeStr, symbol))
            raise
            #pass

    def get_historical_dataV2(self, fd):
        """fetchDict will have last_timestamp, latest_timestamp, interval, symbol, exchange
           Get historical OHLCV for a symbol pair
        Args:
            fetchDict will have last_timestamp, latest_timestamp, interval, symbol, exchange
        Returns:
            list: Contains a list of lists which contain timestamp, open, high, low, close, volume.
        """
        get_next_timestamp = fd['last_timestamp'] + fd['current_interval']
        start = str(tz_from_utc_ms_ts(get_next_timestamp))
        end = str(tz_from_utc_ms_ts(fd['latest_timestamp']))
        after = str(tz_from_utc_ms_ts(fd['last_timestamp']))
        until = str(tz_from_utc_ms_ts(fd['latest_timestamp']))

        #get_interval_count
        since_lastrec_timestamp = fd['latest_timestamp'] - fd['last_timestamp']
        limit = (since_lastrec_timestamp / fd['current_interval']) - 1

        #logger.info("before fetch_ohlcv {}, timeframe {}, since {}, current {} limit = {}".format(Config2tf.symbol, Config2tf.timeframe, Config2tf.get_next_timestamp, Config2tf.current_timestamp, Config2tf.limit))
        logger.info("Before fetch_ohlcv symbol = {}, timeframe= {}, limit = {}".format(fd['symbol'], fd['timeframe'], limit))
        logger.info("since {} end {} after {} until {}".format(start, end, after, until))
        try:
            #historical_data = fetchDict['exchange'].fetch_ohlcv(symbol=fetchDict['symbol'], timeframe=fetchDict['timeframe'], since=fetchDict['since'], limit=fetchDict['limit'])
            barset = fd['exchange'].get_barset(fd['symbol'], fd['timeframe'], start=start, end=end)
            mylist = []
            for bar in barset[fd['symbol']]:
                mydict = {}
                mydict['Timestamp'] = date_to_milliseconds(str(bar.t))
                mydict['Open'] = bar.o
                mydict['High'] = bar.h
                mydict['Low'] = bar.l
                mydict['Close'] = bar.c
                mydict['Volume'] = bar.v
                mydict['normal_time'] = tz_from_utc_ms_ts(mydict['Timestamp'])
                mylist.append(mydict)
        except:
            logging.warning("Unexpected error while appending record: {}", sys.exc_info()[0])
            # logger.error("Unexpected error: {}".format(e))
            #break
            raise
            # pass

        return mylist

    def get_historical_data(self, fetchDict):
        """Get historical OHLCV for a symbol pair
        Decorators:
            retry
        Args:
            market_pair (str): Contains the symbol pair to operate on i.e. BURST/BTC
            exchange (str): Contains the exchange to fetch the historical data from.
            time_unit (str): A string specifying the ccxt time unit i.e. 5m or 1d.
            start_date (int, optional): Timestamp in milliseconds.
            max_periods (int, optional): Defaults to 100. Maximum number of time periods
              back to fetch data for.
        Returns:
            list: Contains a list of lists which contain timestamp, open, high, low, close, volume.
        """
        #logger.info("before fetch_ohlcv {}, timeframe {}, since {}, current {} limit = {}".format(Config2tf.symbol, Config2tf.timeframe, Config2tf.get_next_timestamp, Config2tf.current_timestamp, Config2tf.limit))
        logger.info("before fetch_ohlcv symbol = {}, timeframe= {}, since {} limit = {}".format(fetchDict['symbol'], fetchDict['timeframe'], fetchDict['since'], fetchDict['limit']))
        logger.info("after {} until {}".format(fetchDict['after'], fetchDict['until']))
        logger.info("end {} ".format(fetchDict['end']))
        try:
            #historical_data = fetchDict['exchange'].fetch_ohlcv(symbol=fetchDict['symbol'], timeframe=fetchDict['timeframe'], since=fetchDict['since'], limit=fetchDict['limit'])
            barset = fetchDict['exchange'].get_barset(fetchDict['symbol'], fetchDict['timeframe'], start=fetchDict['since'], end=fetchDict['end'])
            mylist = []
            for bar in barset[fetchDict['symbol']]:
                mydict = {}
                mydict['Timestamp'] = date_to_milliseconds(str(bar.t))
                mydict['Open'] = bar.o
                mydict['High'] = bar.h
                mydict['Low'] = bar.l
                mydict['Close'] = bar.c
                mydict['Volume'] = bar.v
                mydict['normal_time'] = tz_from_utc_ms_ts(mydict['Timestamp'])
                mylist.append(mydict)
        except:
            logging.warning("Unexpected error while appending record: {}", sys.exc_info()[0])
            # logger.error("Unexpected error: {}".format(e))
            #break
            raise
            # pass

        return mylist

#    def readSymbolsCSV(self, filename):
#        df = read_base_file(exchange_folder, symbol_file_name)
#        with open(filename, 'r') as file:
#            data = file.read()
#        symList = list(filter(None, re.split(r'[\|, ,#,\,\n]+', data)))
#        return symList

