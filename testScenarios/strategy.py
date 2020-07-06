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

import re
import multiprocessing
import time
from symbolDataAgents.symbol_data import Symbol_data
from app.scoreBoard import scoreBoard
from app.config import Config2tf
from datetime import datetime
from Utils.helpers import date_to_milliseconds

class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""

    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

class Strategy(multiprocessing.Process):

    def __init__(self, args, cbIF):
        """Constructor for $class$"""
        multiprocessing.Process.__init__(self)
        #threading.Thread.__init__(self, daemon=daemon)
        #super().__init__()
        self.Config2tfObj = Config2tf(args, cbIF)
        self.symbolDataObj=Symbol_data(self.Config2tfObj, cbIF)
        self.scoreBoardObj = scoreBoard(self.Config2tfObj, cbIF)
        self.tsObjList = []
        self.return_bs_dict = AutoVivification()

    def whoami(self):
        print('{}'.format(type(self).__name__))

    def run(self):
        while True:
            self.run_strategies()
            self.scoreBoardObj.tg_logger(self.return_bs_dict)
            if self.Config2tfObj.first_flag:
                time_remaining = self.Config2tfObj.update_interval - (time.time() % self.Config2tfObj.update_interval) + 32
                print("##### First Flag: Taking rest: Sleeping for {} seconds #####".format(time_remaining))
                time.sleep(time_remaining)
                self.Config2tfObj.first_flag=0
            else:
                print("##### Taking rest: Sleeping  for {} seconds #####".format(self.Config2tfObj.update_interval))
                time.sleep(self.Config2tfObj.update_interval)

#    def get_id(self):
#
#        # returns id of the respective thread
#        if hasattr(self, '_thread_id'):
#            return self._thread_id
#        for id, thread in threading._active.items():
#            if thread is self:
#                return id
#
#    def raise_exception(self):
#        thread_id = self.get_id()
#        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
#                                                         ctypes.py_object(SystemExit))
#        if res > 1:
#            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
#            print('Exception raise failure')

    def run_strategies(self):
         #return_bs_dict = {}
         ##current timestamp in utc

         self.current_date_utc = str(datetime.utcnow())
         self.Config2tfObj.current_timestamp=date_to_milliseconds(self.current_date_utc)

         for tsObj in self.tsObjList:
             for index, row in tsObj.dfTestSymbols.iterrows():
                 symbol = row['Symbols']
                 df_current = self.symbolDataObj.run(symbol)
                 for stObj in tsObj.stObjList:
                     df_temp = df_current.copy(deep=True) if (tsObj.stObjListLength > 1) else df_current
                     self.return_bs_dict[stObj.strategy_name][symbol] = stObj.run(df_temp, row)

         #print('{}'.format(return_bs_dict))

    def readSymbolList(self, filename):
         with open(filename, 'r') as file:
             data = file.read()
         symList = list(filter(None, re.split(r'[\|, ,#,\,\n]+', data)))
         return symList

    def check_symbols(self, tsSymList, allAssetsList) :
         flag = 0
         print("#######################################################")
         print("###### Checking if Symbols are actively tradable ######")
         for symbol in tsSymList:
             if (symbol in allAssetsList):
                 print("#########     Symbol {} exists     ###########".format(symbol))
             else:
                 print("######### ++++++++++++++++++++++++ ###########")
                 print("######### Symbol {} does not exist ###########".format(symbol))
                 print("######### ++++++++++++++++++++++++ ###########")
                 flag = 1
         if(flag==1):
             print("######### Quitting. check your symbols spelling ##########")
             quit()
         else:
             return True

    def read_symbols(self, filename, allAssets_filename):
         flag = 0
         #with open(filename, 'H:\\data_folder\\ap\\5Min.txt', 'r') as file:
         with open(filename, 'r') as file:
             data = file.read()

         symList = list(filter(None, re.split(r'[\|, ,#,\,\n]+', data)))

         with open(allAssets_filename, 'r') as file:
             allAssets = file.read()

         print("#######################################################")
         print("###### Checking if Symbols are actively tradable ######")
         for symbol in symList:
             if (symbol in allAssets):
                 print("#########     Symbol {} exists     ###########".format(symbol))
             else:
                 print("######### ++++++++++++++++++++++++ ###########")
                 print("######### Symbol {} does not exist ###########".format(symbol))
                 print("######### ++++++++++++++++++++++++ ###########")
                 flag = 1
         if(flag==1):
             print("######### Quitting. check your symbols spelling ##########")
             quit()
         return symList

