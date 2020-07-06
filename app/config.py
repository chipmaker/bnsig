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

import os
import time
import pandas as pd
import pytz
from Utils.helpers import date_to_milliseconds, interval_to_seconds, interval_to_milliseconds, read_base_file, tz_from_utc_ms_ts
from Utils.mylogger import *
from datetime import datetime, date, timedelta, timezone
from app.user_config import userConfig

class Config2tf(userConfig):

    def __init__(self, args, cbIF):
        """Constructor for $class$"""
        super().__init__(args, cbIF)
        self.symInMemory = 0
        self.first_flag = 1

        self.timeintervals = {
            '1Min': 60,
            '5Min': 300,
            '15Min': 900,
            '1H': 3600,
            '4h' : 14400,
            '1h': 3600,
            '6h': 21600,
            '1d': 86400,
            '1w': 604800,
        }

        if args.timeframe not in cbIF.exchange.timeframes:
            print('-' * 36, ' ERROR ', '-' * 35)
            print('The requested timeframe ({}) is not available from {}\n'.format(args.timeframe, args.exchange))
            print('Available timeframes are:')
            for key in cbIF.exchange.timeframes.keys():
                print('  - ' + key)
            print('-' * 80)
            quit()

        # Check requested timeframe is available. If not return a helpful error.
        if args.timeframe not in self.timeintervals:
            print('-' * 36, ' ERROR ', '-' * 35)
            print('The requested timeframe ({}) is not available from {}\n'.format(args.timeframe, args.exchange))
            print('Available timeframes are:')
            for key in self.timeintervals.keys():
                print('  - ' + key)
            print('-' * 80)
            quit()

        self.timeframe = self.args.timeframe
        #print('self.trimeframe{}'.format(self.timeframe))
        self.current_interval = interval_to_milliseconds(self.timeframe)
        self.current_date_utc = str(datetime.utcnow())
        self.current_timestamp=date_to_milliseconds(self.current_date_utc)
        #print('cdu{} ct{} ci{}'.format(self.current_date_utc,  self.current_timestamp, self.current_interval))
        self.get_next_timestamp = (self.current_timestamp-(self.current_timestamp % self.current_interval))-self.current_interval*16
        self.get_limit = 16
        self.symbol = 'ETH/USD'

        self.set_data_dirs()

    def get_latest_timestamp(self):
        self.current_date_utc = str(datetime.utcnow())
        self.current_timestamp=date_to_milliseconds(self.current_date_utc)
        final_timestamp_temp = self.current_timestamp
        final_timestamp = (final_timestamp_temp - final_timestamp_temp % self.current_interval)
        return final_timestamp

    @property
    def timeframe(self):
        return self.tframe

    @timeframe.setter
    def timeframe(self, tf):
        if tf not in self.timeintervals:
            print('-' * 36, ' ERROR ', '-' * 35)
            print('The requested timeframe ({}) is not available from {}\n'.format(tf, args.exchange))
            print('Available timeframes are:')
            for key in self.timeintervals.keys():
                print('  - ' + key)
            print('-' * 80)
            quit()
        self.tframe = tf
        self.current_interval = interval_to_milliseconds(tf)
        self.update_interval = interval_to_seconds(tf)

    def set_data_dirs(self):
        #print("{} my time frame is {}".format(self.whoami(), self.timeframe))
        #NOW: self.dumps_folder = '.\data_folder\{}\dumps\{}'.format(self.exchange_str, self.timeframe)
        self.dumps_folder = self.data_folder+'\\'+'{}\dumps\{}'.format(self.cbIFPtr.exchange_str, self.timeframe)
        #print("{} dumps_folder is {} ".format(self.whoami(), self.dumps_folder))
        self.results_folder = self.data_folder+'\\'+'{}\\results\{}'.format(self.cbIFPtr.exchange_str, self.timeframe)
        self.lastRun_data_folder = self.data_folder+'\\'+'{}\last_run\{}'.format(self.cbIFPtr.exchange_str, self.timeframe)
        self.currentRun_data_folder = self.data_folder+'\\'+'{}\current_run\{}'.format(self.cbIFPtr.exchange_str, self.timeframe)
        #print("Exchange = {}".format(self.user_config['exchange']))
        #print("{} my time frame is {}".format(self.whoami(), self.timeframe))

        if os.path.isdir(self.dumps_folder):
            logger.info("dumps_folder exists {}".format(self.dumps_folder))
        else:
            try:
                logger.info("Creating dumps_folder {}".format(self.dumps_folder))
                os.mkdir(self.dumps_folder)
            except OSError as error:
                print(error)

        if os.path.isdir(self.lastRun_data_folder):
            logger.info("lastRun_data_folder exists {}".format(self.lastRun_data_folder))
        else:
            try:
                logger.info("Creating lastRun_data_folder {}".format(self.lastRun_data_folder))
                os.mkdir(self.lastRun_data_folder)
            except OSError as error:
                print(error)

        if os.path.isdir(self.currentRun_data_folder):
            logger.info("currentRun_data_folder exists {}".format(self.currentRun_data_folder))
        else:
            try:
                logger.info("Creating currentRun_data_folder {}".format(self.currentRun_data_folder))
                os.mkdir(self.currentRun_data_folder)
            except OSError as error:
                print(error)
        pass

    def get_args(self):
        return self.args

#    def make_symbol_data_paths(self):
#        #CurrentRun_path = self.this_dict['data_folder']+'\\last_run_'+
#        #os.mkdir(CurrentRun_path, 0755);
#        #data_folder = '.\data_folder\{}'.format(Config2tf.exchange)
#        self.dump_filename_only = '{}-{}-{}_dump.csv'.format(self.exchange_str, self.symbol_out, self.timeframe)
#        self.dump_filename_path =self.dumps_folder +'\\' +self.dump_filename_only
#        #self.temp_dump_filename_only = '{}-{}-{}_dump_jupyter.csv'.format(self.exchange_str, self.symbol_out, self.timeframe)
#        #self.temp_dump_filename_path =self.dumps_folder +'\\' +self.temp_dump_filename_only
#        self.lastRun_filename_only = '{}-{}-{}-last_run.csv'.format(self.exchange_str, self.symbol_out, self.timeframe)
#        self.lastRun_filename_path = self.lastRun_data_folder +'\\'+ self.lastRun_filename_only
#        self.currentRun_filename_only = '{}-{}-{}-appended.csv'.format(self.exchange_str, self.symbol_out, self.timeframe)
#        self.currentRun_filename_path=self.currentRun_data_folder+'\\'+self.currentRun_filename_only
#        self.currentRunRecent_filename_only = '{}-{}-{}-recent.csv'.format(self.exchange_str, self.symbol_out, self.timeframe)
#        self.currentRunRecent_filename_path=self.currentRun_data_folder+'\\'+self.currentRunRecent_filename_only

    def get_symbols(self):
            # root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            # sys.path.append(root + '/python')
            def print_supported_exchanges():
                print('Supported exchanges:{}', ccxt.exchanges)

            try:
                # load all markets from the exchange
                markets = self.exchange.load_markets()
                # print(markets)
                # # output a list of all market symbols
                # print("{} has {} symbols {}".format(exchange.id, len(exchange.symbols), exchange.symbols))

                print("{} has {} symbols".format(self.exchange_str, len(self.exchange.symbols)))
                tuples = list(ccxt.Exchange.keysort(markets).items())
                # debug
                header = ['SYMBOLS', 'VALUES']
                df = pd.DataFrame(tuples, columns=header)
                df.to_csv(self.symbol_filename_path)
                # header = ['id', 'symbol', 'base', 'quote']
                # df2=pd.DataFrame(columns=header)
                # for(k,v) in tuples:
                #    df2['id'] = v['id']
                #    df2['symbol'] =v['symbol']
                #    df2['base'] = v['base']
                #    df2['quote'] = v['quote']

                # filename = '{}-Symbols-Values.csv'.format(Config2tf.exchange)
                # df2.to_csv(filename)
            except Exception as e:
                # dump('[' + type(e).__name__ + ']', str(e))
                print('[ {} {} ]'.format(type(e).__name__, str(e)))
                print("Usage: check argparse usage ")
                print_supported_exchanges()


    def get_all_symbols(self):
        # Get a list of all active assets.
        active_assets = self.exchange.list_assets(status='active')

        mylist = []
        for asset in active_assets:
            mylist.append(asset.symbol)

        self.allAssetsListPath = self.exchange_data_folder + '\\allAssets.txt'

        with open('allAssets.txt', 'w') as filehandle:
            for listitem in mylist:
                filehandle.write('%s\n' % listitem)

    def read_sym_file(self):
        df = read_base_file(self.exchange_data_folder, self.sym_filename_only)
        #self.exclusions = {"EUR", "GBP", "USDC"}
        self.all_symbols =[x for x in df.SYMBOLS if "EUR" not in x]
        self.all_symbols =[x for x in self.all_symbols if "GBP" not in x]
        self.all_symbols =[x for x in self.all_symbols if "USDC" not in x]
        self.all_symbols =[x for x in self.all_symbols if "/BTC" not in x]
        self.all_symbols =[x for x in self.all_symbols if "/ETH" not in x]
        self.all_symbols =[x for x in self.all_symbols if "/DAI" not in x]
        #print(all_symbols_filtered)
        #all_symbols_exclude1 =[x for x in df.SYMBOLS if "BNB" not in x]
        #self.binance_exclusions={'NANO/BTC', 'NANO/ETH', 'VEN/BTC', 'VEN/ETH', 'VEN/USDT' 'DOCK/ETH', 'POLY/BTC', 'PAX/BTC', 'PAX/ETH', 'USDC/BTC'}
        #self.all_symbols = [e for e in all_symbols_exclude if e not in self.binance_exclusions]
        #self.all_symbols = all_symbols_exclude
        #self.all_symbols = ['ALGO/USD']
        #self.all_symbols = ['ETC/USD']
        #self.all_symbols = ['ADX/BTC']
        #self.csvFilePath= self.currentRun_data_folder+'\\'+ '{}-{}-{}-appended-temp.csv'.format(self.exchange_str, self.symbol_out, self.timeframe)
        #print("{} my time frame is {} {}".format(self.whoami(), self.timeframe, self.symbol_out))

