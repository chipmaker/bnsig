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
import traceback
import pandas as pd
import glob, os
import logging
import time
from Utils.helpers import *
from Utils.mylogger import *

class Symbol_data(object):
    def whoami(self, def_name):
        #print('I am = {}'.format(type(self).__name__))
        if def_name == None:
            (filename,line_number,function_name,text)=traceback.extract_stack()[-2]
            self.def_name = text[:text.find('=')].strip()
        else:
            self.def_name = def_name
        return self.def_name

    def __init__(self, Config2tf, cbIF, def_name=None):
        """Constructor for $class$"""
        #print('####Inside SYMBOL_DATA CONSTRUCTOR = {}'.format(type(self).__name__))
        #print('Inside SYMBOL_DATA CONSTRUCTOR = {}'.format(self.whoami()))
        if def_name == None:
            (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
            def_name = text[:text.find('=')].strip()
        self.name = def_name
        print('Inside SYMBOL_DATA CONSTRUCTOR = {}'.format(self.name))
        self.config2tfPtr = Config2tf
        self.cbIFPtr = cbIF
        self.exchange = cbIF.exchange
        self.exchange_str = cbIF.exchange_str
        self.timeframe = Config2tf.timeframe

        self.data_folder = Config2tf.data_folder
        self.dumps_folder = Config2tf.dumps_folder
        self.lastRun_data_folder = Config2tf.lastRun_data_folder
        self.currentRun_data_folder = Config2tf.currentRun_data_folder

        self.symbol = 'BTC-USD'
        self.symData = {}
        self.fetchDict ={ 'exchange'  : cbIF.exchange,
                          'exchange_str': cbIF.exchange_str,
                          'timeframe' : Config2tf.timeframe,
                          'since'     : Config2tf.get_next_timestamp,
                          'limit'     :  Config2tf.get_limit,
                          'symbol'    : self.symbol}

    @property
    def timeframe(self):
        return self.tframe

    @timeframe.setter
    def timeframe(self, tf):
        self.tframe = tf
        self.current_interval = interval_to_milliseconds(tf)
        self.update_interval = interval_to_seconds(tf)

    @property
    def symbol(self):
        return self.symbol_str

    @symbol.setter
    def symbol(self, sym):
        self.symbol_str = sym
        self.symbol_out = sym.replace("/", "")

    def make_symbol_data_paths(self):
        #CurrentRun_path = self.this_dict['data_folder']+'\\last_run_'+
        #os.mkdir(CurrentRun_path, 0755);

        self.dump_filename_only = '{}-{}-{}_dump.csv'.format(self.exchange_str, self.symbol_out, self.timeframe)
        self.dump_filename_path =self.dumps_folder +'\\' +self.dump_filename_only
        #self.temp_dump_filename_only = '{}-{}-{}_dump_jupyter.csv'.format(self.exchange_str, self.symbol_out, self.timeframe)
        #self.temp_dump_filename_path =self.dumps_folder +'\\' +self.temp_dump_filename_only
        self.lastRun_filename_only = '{}-{}-{}-last_run.csv'.format(self.exchange_str, self.symbol_out, self.timeframe)
        self.lastRun_filename_path = self.lastRun_data_folder +'\\'+ self.lastRun_filename_only
        self.currentRun_filename_only = '{}-{}-{}-appended.csv'.format(self.exchange_str, self.symbol_out, self.timeframe)
        self.currentRun_filename_path=self.currentRun_data_folder+'\\'+self.currentRun_filename_only
        self.currentRunRecent_filename_only = '{}-{}-{}-recent.csv'.format(self.exchange_str, self.symbol_out, self.timeframe)
        self.currentRunRecent_filename_path=self.currentRun_data_folder+'\\'+self.currentRunRecent_filename_only

    def get_exchange_tickers(Config2tf):
        # Get our Exchange from init
        d = self.exchange.fetch_tickers()
        df = pd.DataFrame(data=d)
        filename = '{}.csv'.format(Config2tf.exchange_str)
        df.to_csv(filename)

    def read_record_wchks2(self):
        if os.path.isfile(self.currentRun_filename_path):
            logger.info("read_record_wchks: CurrentRun File exists {}".format(self.currentRun_filename_path))
            df_current = read_base_file(self.currentRun_data_folder, self.currentRun_filename_only)
            cr_last_timestamp = int(df_current['Timestamp'].iloc[-1])
            #current_date = str(datetime.now())
            #print("last_TimeStamp={} current_timestamp={} current_interval={} diff={}".format(last_timestamp, self.current_timestamp, self.current_interval, (self.current_timestamp-last_timestamp)))
            logging.info("current run last_TimeStamp={} current_timestamp={} current_interval={} diff={}".format(cr_last_timestamp, self.config2tfPtr.current_timestamp, self.current_interval, (self.config2tfPtr.current_timestamp-cr_last_timestamp)))
            latest_timestamp = self.config2tfPtr.get_latest_timestamp()
            since_lastrec_timestamp = (latest_timestamp - cr_last_timestamp)
            if(since_lastrec_timestamp < self.current_interval):
                logger.info("APPENDED RECORD IS LATEST {}".format(self.currentRun_filename_path))
                return df_current
            elif(since_lastrec_timestamp > self.current_interval*299):   ##Is current run older than 32 records
                logger.info("OLD CURRENT RECORDS: TRYING TO MOVE APPENDED DATA FILES AND UPDATE LAST RUNS for {}".format(self.currentRun_filename_path))
                currentRun_data_folder_backup=self.get_currentRun_data_backup_folder_path('old_current_records')
                os.makedirs(currentRun_data_folder_backup, exist_ok=True)
                cr_dst_file_path = os.path.join(currentRun_data_folder_backup, self.currentRun_filename_only)
                if os.path.exists(cr_dst_file_path):
                    #os.remove(dst_file_path)
                    logger.info("BACKUP ALREADY EXISTS! {} . Overwriting the file ".format(cr_dst_file_path))
                elif os.path.exists(self.currentRun_filename_path):
                    shutil.move(self.currentRun_filename_path, cr_dst_file_path)
                    #shutil.move(self.currentRun_filename_path, self.lastRun_filename_path)
                    #os.remove(self.currentRunRecent_filename_path)
                return self.append_lastRun_record()
            else:
                #logger.info("CALLING append_lastRun_record to update file .{}".format(self.currentRun_filename_path))
                return self.append_lastRun_record()
        else:
            #logger.info("CALLING append_lastRun_record to update file {} to create {}".format(self.lastRun_filename_path, self.currentRun_filename_path))
            #logger.info("CALLING append_lastRun_record State")
            return self.append_lastRun_record()

    def append_lastRun_record(self):
        if os.path.isfile(self.lastRun_filename_path):
            df_lastRun = read_base_file(self.lastRun_data_folder, self.lastRun_filename_only)
            dropped_lastRun_timestamp = int(df_lastRun['Timestamp'].iloc[-1])
            df_lastRun.drop(df_lastRun.last_valid_index(), axis=0, inplace=True)
            lastRun_last_timestamp = int(df_lastRun['Timestamp'].iloc[-1])
            latest_timestamp = self.config2tfPtr.get_latest_timestamp()
            since_lastrec_timestamp = (latest_timestamp - lastRun_last_timestamp)
            if(since_lastrec_timestamp == 0):
                logger.info("LASTRUN_RECORD IS LATEST {}".format(self.lastRun_filename_path))
                shutil.copyfile(self.lastRun_filename_path, self.currentRun_filename_path)
                return df_lastRun
            elif(since_lastrec_timestamp > self.current_interval*299):    ##Is last run older than 128 records
                #logger.info("LAST RUN FILE TOO OLD.MOVING CURRENT DATA FILES{} into last_run folder backup and naming as last run file".format(self.currentRun_filename_path))
                logger.info("LAST RUN FILE TOO OLD.MOVING it to backup and going to DUMP state".format(self.lastRun_filename_path))
                lastRun_data_backup_folder= self.get_lastRun_data_backup_folder_path()
                os.makedirs(lastRun_data_backup_folder, exist_ok=True)
                lastRun_data_backup_file_path = os.path.join(lastRun_data_backup_folder, self.lastRun_filename_only)
                if os.path.exists(lastRun_data_backup_file_path):
                    #os.remove(dst_file_path)
                    logger.info("BACKUP FILE ALREADY EXISTS!{} Overwriting file".format(lastRun_data_backup_file_path))
                else:
                    shutil.move(self.lastRun_filename_path, lastRun_data_backup_file_path)
                    #shutil.move(self.currentRun_filename_path, self.lastRun_filename_path)
                    #os.remove(self.currentRunRecent_filename_path)
                return self.append_dump_record()
            else:
                #data = self.exchange.fetch_ohlcv(self.symbol, self.timeframe, since=self.get_next_timestamp)
                # data = self.exchange.fetch_ohlcv(self.symbol, self.timeframe, since=self.get_next_timestamp)
                self.fetchDict['symbol'] = self.symbol
                self.fetchDict['timeframe'] = self.timeframe
                self.fetchDict['current_interval'] = self.current_interval
                self.fetchDict['last_timestamp'] = lastRun_last_timestamp
                self.fetchDict['latest_timestamp'] = latest_timestamp
                self.fetchDict['since'] = dropped_lastRun_timestamp
                df_recent= self.cbIFPtr.get_historical_dataV2(self.fetchDict)
                self.df_current = pd.concat([df_lastRun, df_recent], ignore_index=True, sort=False, axis=0)

                self.df_current.to_csv(self.lastRun_filename_path, index=False)
                shutil.copyfile(self.lastRun_filename_path, self.currentRun_filename_path)
                return self.df_current
        else:
            return self.append_dump_record()

    def append_dump_record(self):
        if os.path.isfile(self.dump_filename_path):
            df_dump = read_base_file(self.dumps_folder, self.dump_filename_only)
            if (df_dump.empty):
                logger.info("######### QUITTING: Reason: Data Frame Empty {}".format(self.dump_filename_path))
                quit()

            dropped_dump_timestamp = int(df_dump['Timestamp'].iloc[-1])
            df_dump.drop(df_dump.last_valid_index(), axis=0, inplace=True)
            dump_last_timestamp = int(df_dump['Timestamp'].iloc[-1])
            latest_timestamp = self.config2tfPtr.get_latest_timestamp()
            since_lastrec_timestamp = (latest_timestamp - dump_last_timestamp)
            if(since_lastrec_timestamp == 0):
                logger.info("DUMP_RECORD IS LATEST {}".format(self.dump_filename_path))
                shutil.copyfile(self.dump_filename_path, self.lastRun_filename_path)
                shutil.copyfile(self.dump_filename_path, self.currentRun_filename_path)
                return df_dump
            elif(since_lastrec_timestamp > self.current_interval*299):    ##Is last run older than 128 records
                #logger.info("LAST RUN FILE TOO OLD.MOVING CURRENT DATA FILES{} into last_run folder backup and naming as last run file".format(self.currentRun_filename_path))
                logger.info("DUMP FILE TOO OLD.MOVING it to backup and going to DUMP state".format(self.dump_filename_path))
                dump_data_backup_folder= self.get_dump_data_backup_folder_path()
                os.makedirs(dump_data_backup_folder, exist_ok=True)
                dump_data_backup_file_path = os.path.join(dump_data_backup_folder, self.dump_filename_only)
                if os.path.exists(dump_data_backup_file_path):
                    #os.remove(dst_file_path)
                    logger.info("### BACKUP FILE ALREADY EXISTS!{} Quitting ###".format(dump_data_backup_file_path))
                    logger.info("### TBD. Symbolwise backup with timestamps ###")
                    #df_dump_fbackup = read_base_file(self.dump_data_backup_folder, self.dump_filename_only)
                    quit()
                else:
                    shutil.move(self.dump_filename_path, dump_data_backup_file_path)
                    #shutil.move(self.currentRun_filename_path, self.lastRun_filename_path)
                    #os.remove(self.currentRunRecent_filename_path)
                    logger.info("PULLING NEW DUMP FILE{}".format(self.dump_filename_path))

                    self.fetchDict['symbol'] = self.symbol
                    self.fetchDict['timeframe'] = self.timeframe
                    self.fetchDict['limit'] = 300
                    self.df_latest_fromExchange = self.cbIFPtr.get_symbol_DF(self.fetchDict)
                    self.df_latest_fromExchange.to_csv(self.dump_filename_path, index=False)
                    shutil.copyfile(self.dump_filename_path, self.lastRun_filename_path)
                    shutil.copyfile(self.dump_filename_path, self.currentRun_filename_path)
                    return self.df_latest_fromExchange
            else:
                # data = self.exchange.fetch_ohlcv(self.symbol, self.timeframe, since=self.get_next_timestamp)
                # data = self.exchange.fetch_ohlcv(self.symbol, self.timeframe, since=self.get_next_timestamp)
                self.fetchDict['symbol'] = self.symbol
                self.fetchDict['timeframe'] = self.timeframe
                self.fetchDict['current_interval'] = self.current_interval
                self.fetchDict['last_timestamp'] = dump_last_timestamp
                self.fetchDict['since'] = dropped_dump_timestamp
                self.fetchDict['latest_timestamp'] = latest_timestamp
                df_recent = self.cbIFPtr.get_historical_dataV2(self.fetchDict)
                self.df_current = pd.concat([df_dump, df_recent], ignore_index=True, sort=False, axis=0)
                self.df_current.to_csv(self.dump_filename_path, index=False)
                shutil.copyfile(self.dump_filename_path, self.lastRun_filename_path)
                shutil.copyfile(self.dump_filename_path, self.currentRun_filename_path)
                return self.df_current
        else:
            logger.info("DUMP_FILE DOES NOT EXIST.{}".format(self.dump_filename_path))
            logger.info("PULLING NEW DUMP FILE{}".format(self.dump_filename_path))

            self.fetchDict['symbol'] = self.symbol
            self.fetchDict['timeframe'] = self.timeframe
            self.df_latest_fromExchange = self.cbIFPtr.get_symbol_DF(self.fetchDict)
            self.df_latest_fromExchange.to_csv(self.dump_filename_path, index=False)
            shutil.copyfile(self.dump_filename_path, self.lastRun_filename_path)
            shutil.copyfile(self.dump_filename_path, self.currentRun_filename_path)
            return self.df_latest_fromExchange

    def run(self, sym):
        self.symbol = sym
        self.make_symbol_data_paths()

        if(self.config2tfPtr.first_flag == 1):
            if (self.config2tfPtr.symInMemory == 1):
                self.symData[self.symbol] = self.read_record_wchks2()
                return self.symData[self.symbol]
            else:
                return self.read_record_wchks2()
        elif(self.config2tfPtr.first_flag == 0):
            if(self.config2tfPtr.symInMemory == 1):
                logger.info("read_record_wchks, LOOP: Pulling {} Data from memory".format(self.symbol))
                df_current = self.symData[self.symbol]
            else:
                logger.info("read_record_wchks, LOOP: CurrentRun File exists {}".format(self.currentRun_filename_path))
                df_current = read_base_file(self.currentRun_data_folder, self.currentRun_filename_only)
            df_current.drop(df_current.last_valid_index(), axis=0, inplace=True)
            cr_last_timestamp = int(df_current['Timestamp'].iloc[-1])
            #logging.info("current run last_TimeStamp={} current_timestamp={} current_interval={} diff={}".format(cr_last_timestamp, Config2tf.current_timestamp, Config2tf.current_interval, (Config2tf.current_timestamp-cr_last_timestamp)))
            latest_timestamp = self.config2tfPtr.get_latest_timestamp()
            since_lastrec_timestamp = (latest_timestamp - cr_last_timestamp)
            if(since_lastrec_timestamp < self.current_interval):
                logger.info("APPENDED RECORD IS LATEST {}".format(self.currentRun_filename_path))
                return df_current
            else:
                if ((df_current.shape[0]) > 600):
                    logger.info("Current Run file too large. Chop the first 300 old records from {}".format(self.currentRun_filename_path))
                    df_current = df_current.iloc[300:]
                # data = Config2tf.exchange.fetch_ohlcv(self.symbol, Config2tf.timeframe, since=Config2tf.get_next_timestamp)
                self.fetchDict['symbol'] = self.symbol
                self.fetchDict['timeframe'] = self.timeframe
                self.fetchDict['current_interval'] = self.current_interval
                self.fetchDict['last_timestamp'] =cr_last_timestamp
                self.fetchDict['latest_timestamp'] = latest_timestamp

                df_recent = self.cbIFPtr.get_historical_dataV2(self.fetchDict)
                #print(df_recent)
                #quit()
                # df_recent.to_csv(Config2tf.currentRunRecent_filename_path)
                df_current = pd.concat([df_current, df_recent], ignore_index=True, sort=False, axis=0)
                if (self.config2tfPtr.symInMemory == 1):
                    self.symData[self.symbol] = df_current
                else:
                    df_current.to_csv(self.currentRun_filename_path, index=False)
                return df_current

    def get_lastRun_data_backup_folder_path(self):
        lastRun_data_folder_backup_path = self.lastRun_data_folder + '_' + str(time.strftime('%Y%m%d%H'))
        return lastRun_data_folder_backup_path

    def get_dump_data_backup_folder_path(self):
        dump_data_folder_backup_path = self.dumps_folder + '_' + str(time.strftime('%Y%m%d%H'))
        return dump_data_folder_backup_path

    def get_currentRun_data_backup_folder_path(self, name=''):
        currentRun_data_folder_backup_path = self.currentRun_data_folder + '_'+name+'_'+str(time.strftime('%Y%m%d%H'))
        return currentRun_data_folder_backup_path

