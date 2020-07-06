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

import sys
import ccxt
import multiprocessing
from Utils.mylogger import *
import time
from Utils.helpers import *
class cbIF(object):

    def __init__(self, args):
        """Constructor for $class$"""
        self.args = args
        self.exchange_str=args.exchange
        # Get our Exchange
        try:
            #self.auth_client = cbpro.AuthenticatedClient(key, b64secret, passphrase)
            if(self.exchange_str == 'cb'):
                self.exchange = cbpro.PublicClient()
            elif(self.exchange_str == 'binanceus'):
                try:
                    self.exchange = getattr(ccxt, args.exchange)({
                        #'rateLimit': 3000,
                        'enableRateLimit': True,
                        #'timeout': 10000,
                    })
                except AttributeError:
                    print('-' * 36, ' ERROR ', '-' * 35)
                    print('Exchange "{}" not found. Please check the exchange is supported.'.format(args.exchange))
                    print('-' * 80)
                    quit()
                ##Exchange Symbols Installation Procedure 1
                self.exchange.load_markets()
                self.exchange_rateLimit = self.exchange.rateLimit / 1000
        except AttributeError:
            print('-' * 36, ' ERROR ', '-' * 35)
            print('Exchange "{}" not found. Please check the exchange is supported.'.format(args.exchange))
            print('-' * 80)
            quit()

        self.exchange_rateLimit = 0.4
        self.lock = multiprocessing.Lock()

    def whoami(self):
        my_identity = type(self).__name__
        #print('{}'.format(my_identity))
        return my_identity

    def run(self):
        pass

    def get_historical_dataV2(self, fd):
        """fetchDict will have last_timestamp, latest_timestamp, interval, symbol, exchange
           Get historical OHLCV for a symbol pair
        Args:
            fetchDict will have last_timestamp, latest_timestamp, interval, symbol, exchange
        Returns:
            list: Contains a list of lists which contain timestamp, open, high, low, close, volume.
        """
        self.lock.acquire()
        get_next_timestamp = fd['last_timestamp'] + fd['current_interval']
        since = get_next_timestamp
        start = str(tz_from_utc_ms_ts(get_next_timestamp, pytz.utc))
        end = str(tz_from_utc_ms_ts(fd['latest_timestamp'], pytz.utc))
        ###ISO Format start and end
        #start = str(tz_iso_from_utc_ms_ts(get_next_timestamp, tz_info=pytz.utc))
        #end = str(tz_iso_from_utc_ms_ts(fd['latest_timestamp'], tz_info=pytz.utc))

        after = str(tz_from_utc_ms_ts(fd['last_timestamp']))
        until = str(tz_from_utc_ms_ts(fd['latest_timestamp']))
        granularity = int(fd['current_interval'] / 1000)

        #get_interval_count
        since_lastrec_timestamp = fd['latest_timestamp'] - fd['last_timestamp']
        limit = (since_lastrec_timestamp / fd['current_interval']) - 1

        #logger.info("before fetch_ohlcv {}, timeframe {}, since {}, current {} limit = {}".format(Config2tf.symbol, Config2tf.timeframe, Config2tf.get_next_timestamp, Config2tf.current_timestamp, Config2tf.limit))
        logger.info("Before fetch_ohlcv symbol = {}, timeframe= {}, limit = {}, granularity = {}".format(fd['symbol'], fd['timeframe'], limit, granularity))
        logger.info("since {} end {} after {} until {}".format(start, end, after, until))
        try:
            time.sleep(self.exchange_rateLimit)
            data = self.exchange.fetch_ohlcv(symbol=fd['symbol'], timeframe=fd['timeframe'], since=since)
            header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
            df = pd.DataFrame(data, columns=header)
            # print(df_recent)
            df['normal_time'] = pd.to_datetime(df['Timestamp'], unit='ms')
        except:
            logging.warning("Unexpected error while appending record: {}", sys.exc_info()[0])
            # logger.error("Unexpected error: {}".format(e))
            #break
            raise
            # pass
        finally:
            self.lock.release()
        return df

    def get_symbol_DF(self, fd):
        # Get data
        self.lock.acquire()
        try:
            time.sleep(self.exchange_rateLimit)
            data = self.exchange.fetch_ohlcv(fd['symbol'], fd['timeframe'])
            #############startexp#############
            #df = pd.DataFrame(data)
            #columns = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
            #df.to_csv(Config2tf.temp_dump_filename_path, index=False, header=columns)
            #quit()
            ####################END##############
            #logger.info("After fetch_ohlcv in store_symbol. Symbol={}".format(Config2tf.symbol))
            header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
            df = pd.DataFrame(data, columns=header)
            df['normal_time'] = pd.to_datetime(df['Timestamp'], unit='ms')
            if (df.size == 0):
                print('Inside Store Symbol. DF of {} is empty. Quitting'.format(fd['symbol']))
                quit()
        except:
            # logging.warning("Unexpected error: {}", sys.exc_info()[0])
            logger.warning("Unexpected error: Exchange={}, symbol={}, fd['timeframe']={}".format(fd['exchange_str'], fd['symbol'], fd['timeframe']))
            raise
            # pass
        finally:
            self.lock.release()
        return df
