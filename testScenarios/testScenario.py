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
from Utils.helpers import read_base_file

class testScenario(object):

    def __init__(self, Config2tf, params):
        """Constructor for $class$"""
        self.config2tfPtr = Config2tf
        #self.name = 'DefaultTestScenario'
        if 'name' not in params:
            self.name = params['sym_filename_only'].replace(".csv", "")
        else:
            self.name = params['name']
        self.read_test_symbols(Config2tf.exchange_data_folder, params['sym_filename_only'])
        if 'withinBars' not in params:
            self.withinBars = 1
        else:
            self.withinBars = params['withinBars']
        self.all_test_symbols = []
        self.stObjList = []

    @property
    def stObjListLength(self):
        return len(self.stObjList)

    def whoami(self):
        print('{}'.format(type(self).__name__))

    def read_test_symbols(self, exchange_data_folder, sym_filename_only):
        self.dfTestSymbols = read_base_file(exchange_data_folder, sym_filename_only)
        self.all_test_symbols = self.dfTestSymbols['Symbols']
        #print("ALL ASSETS = {}".format(self.config2tfPtr.allAssetsList))
        print("#######################################################")
        print("###### Checking if Symbols are actively tradable ######")
        dfAS = self.config2tfPtr.dfAllSymbols
        flag = 0
        for symbol in self.all_test_symbols:
            symbolRegex ="\\b{}\\b".format(symbol)
            resultDF = dfAS[dfAS['Symbols'].str.contains(symbolRegex)]
            resultDFShape = resultDF.shape
            #print('symbolRegex={}, shape={} result=\n {}'.format(symbolRegex, resultDFShape, resultDF))
            if (resultDFShape[0]==1):
                print("#########     Symbol {} exists     ###########".format(symbol))
            else:
                print("######### ++++++++++++++++++++++++ ###########")
                print("######### Symbol {} does not exist ###########".format(symbol))
                print("######### ++++++++++++++++++++++++ ###########")
                flag = 1
        if(flag==1):
            print("######### Quitting. If ur symbol is there, check spelling ##########")
            quit()

        return self.all_test_symbols

    def read_and_check_symbols(self, filename):
        flag = 0
        #with open(filename, 'H:\\data_folder\\ap\\5Min.txt', 'r') as file:
        with open(filename, 'r') as file:
            data = file.read()

        symList = list(filter(None, re.split(r'[\|, ,#,\,\n]+', data)))

        print("#######################################################")
        print("###### Checking if Symbols are actively tradable ######")
        for symbol in symList:
            if (symbol in self.config2tfPtr.allAssetsList):
                print("#########     Symbol {} exists     ###########".format(symbol))
            else:
                print("######### ++++++++++++++++++++++++ ###########")
                print("######### Symbol {} does not exist ###########".format(symbol))
                print("######### ++++++++++++++++++++++++ ###########")
                flag = 1
        if(flag==1):
            print("######### Quitting. check your symbols spelling ##########")
            quit()

        self.all_test_symbols = symList
        return self.all_test_symbols

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

        self.all_test_symbols = symList
        return self.all_test_symbols

