
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

from datetime import datetime
from Utils.TelegramBot2 import Telegrambot2

class scoreBoard(object):
    """Implementation of perl's autovivification feature."""

    def __init__(self, Config2tf, cbIF):
        """Constructor for $class$"""
        super().__init__()
        self.timeframes = {
            '1Min': '1m',
            '5Min': '5m',
            '15Min': '15m',
            '1H': '1h',
            '1h':'1h',
            '4h':'4h',
            '6h': '6h',
            '1D': '1d',
            '1d': '1d',
            '1w': '1w',
        }
        self.cbIFPtr = cbIF
        self.config2tfPtr = Config2tf
        self.TelegramObj = Telegrambot2()

    def tg_logger(self, bs_dict):

        #mylist_sells = list(set(self.mylist) & set(sell_list))
        mylist_sells = 'DUMMY'

        for strategy_name, results in bs_dict.items():
            buy_list = []
            sell_list = []
            for symbol_str, value in results.items():
                if (value[1] == True):
                    buy_list.append([symbol_str, value[2]])
                elif (value[0] == True):
                    sell_list.append([symbol_str, value[2]])

            #print('buy_list{} sell_list{} lensell = {}'.format(buy_list, sell_list, len(sell_list)))
            #its better to put list length in a variable and use it to compare. Some compiler problem
            buy_list_length = len(buy_list)
            sell_list_length = len(sell_list)
            if((buy_list_length==0) & (sell_list_length==0)):
                #print('nside iffffff buy_list{} sell_list{} lensell = {}'.format(buy_list, sell_list, len(sell_list)))
                continue

            tg_text = str(datetime.utcnow()) + '\nEX:{}   ST:{}\n\n'.format(self.cbIFPtr.exchange_str, strategy_name) + \
                      'BUY_LIST=\n{}\n'.format(str(buy_list)[1:-1]) + \
                      '\n\nSELL_LIST=\n{}\n'.format(str(sell_list)[1:-1]) + \
                      '\n\nMY_SELL_LIST={}'.format(mylist_sells)

            print('{}'.format(tg_text))

            self.TelegramObj.send_telegram_message(tg_text, self.timeframes[self.config2tfPtr.timeframe])

        #for self.symbol in self.config2tfPtr.all_symbols:
        #    if (self.config2tfPtr.return_bs_dict[self.config2tfPtr.symbol_str][1] == True):
        #        buy_list.append(self.config2tfPtr.symbol_out)
        #    elif (self.config2tfPtr.return_bs_dict[self.config2tfPtr.symbol_str][0] == True):
        #        sell_list.append(self.config2tfPtr.symbol_out)

        # logging.info('BUY_LIST={}'.format(Config2tf.buy_list))
        # logging.info('SELL_LIST={}'.format(Config2tf.sell_list))
        # print('BUY_LIST={}'.format(buy_list))
        # print('SELL_LIST={}'.format(sell_list))


        # print('MY_SELL_LIST={}'.format(mylist_sells))

        # self.appendDFToCSV(buy_list, sell_list, mylist_sells, Config2tf)

    def appendDFToCSV(self, buy_list, sell_list, mylist_sells, Config2tf):
        s1 = pd.Series([buy_list, sell_list, mylist_sells])
        df_st_results = pd.DataFrame([s1.values],  columns=["BUY", "SELL", "MY_SELL_LIST"])
        Config2tf.results_filename_only='{}-{}-{}-results.csv'.format(Config2tf.exchange_str, Config2tf.timeframe, Config2tf.strategy_name)
        Config2tf.results_FilePath = Config2tf.results_folder+'\\'+Config2tf.results_filename_only
        appendDFToCSV_void(df_st_results, Config2tf.results_FilePath, sep=",")

    def new_symbols(self, Config2tf):
        new_buy_list=[]
        new_sell_list=[]
        for this_symbol in Config2tf.all_symbols:
            this_symbol_out = 'BINANCE:'+this_symbol.replace("/", "")
            if(Config2tf.return_bs_dict[this_symbol][3]==True):
                new_buy_list.append(this_symbol_out)
            elif(Config2tf.return_bs_dict[this_symbol][2]==True):
                new_sell_list.append(this_symbol_out)

        print('NEW_BUY_LIST={}'.format(new_buy_list))
        print('NEW_SELL_LIST={}'.format(new_sell_list))
        Config2tf.tg_text_append = 'NEW_BUY_LIST=\n{}'.format(str(new_buy_list)[1:-1]) + 'NEW_SELL_LIST=\n{}'.format(str(new_sell_list)[1:-1])
