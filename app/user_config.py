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

from Utils.helpers import read_base_file
class userConfig(object):

    def __init__(self, args, cbIF):
        """Constructor for $class$"""
        self.args = args
        self.cbIFPtr = cbIF
        # Get our Exchange
        #self.data_folder = '.\data_folder'.format(args.exchange)
        self.data_folder = 'H:\data_folder'.format(args.exchange)
        self.exchange_data_folder = self.data_folder+'\\'+'{}'.format(args.exchange)
        self.dfAllSymbols = read_base_file(self.exchange_data_folder, 'allAssets.csv')
        self.allAssetsList = self.dfAllSymbols['Symbols']

    def whoami(self):
        my_identity = type(self).__name__
        #print('{}'.format(my_identity))
        return my_identity

    def run(self):
        pass

    def mylist(self):
        mylist =('BINANCE:BATBTC', 'BINANCE:BNBBTC', 'BINANCE:KMDBTC', 'BINANCE:NCASHBTC', 'BINANCE:POWRBTC', 'BINANCE:STEEMBTC', 'BINANCE:SUBBTC', 'BINANCE:TNTBTC', 'BINANCE:VENBTC', 'BINANCE:WABIBTC', 'BINANCE:WANBTC', 'BINANCE:WTCBTC', 'BINANCE:XEMBTC')
        return mylist


#        self.print_user_config()
#        return self.user_config
#
#    def print_user_config(self):
#        for k, v in self.user_config.items():
#            print(k, v)
