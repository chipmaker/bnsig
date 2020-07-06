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

import requests
import urllib
import logging

class Telegrambot2(object):
    def whoami(self):
        logging.info('{}'.format(type(self).__name__))

    def __init__(self):
        """Constructor for $class$"""
        self.load_tg_params()
        #logging.info("Telegrambot2 Instantiated.{} %s", self.whoami())
        #print("Telegrambot2 Instantiated.")

        # Make your own telegram tokens by searching google. It is a simple task

    def load_tg_params(self):
        self.tg_TOKEN_1d = '486645677:AdhhhtjullgdwrgksjgktisvmajAhljo25U'
        self.tg_TOKEN_6h = ':'
        self.tg_TOKEN_4h = ':'
        self.tg_TOKEN_1h = ':'
        self.tg_TOKEN_15m = '8575746746:SSSfggjhekk366HBDDDKJHBCKJIHOLJSHF'
        self.tg_TOKEN_5m = ':'
        self.tg_chat_id = '5675845948'
        self.tg_URL_1d = "https://api.telegram.org/bot{}/".format(self.tg_TOKEN_1d)
        self.tg_URL_6h = "https://api.telegram.org/bot{}/".format(self.tg_TOKEN_6h)
        self.tg_URL_4h = "https://api.telegram.org/bot{}/".format(self.tg_TOKEN_4h)
        self.tg_URL_1h = "https://api.telegram.org/bot{}/".format(self.tg_TOKEN_1h)
        self.tg_URL_15m = "https://api.telegram.org/bot{}/".format(self.tg_TOKEN_15m)
        self.tg_URL_5m = "https://api.telegram.org/bot{}/".format(self.tg_TOKEN_5m)

    def send_telegram_message(self, bs_msg, timeframe):

        text = urllib.parse.quote_plus(bs_msg)

        if(timeframe=='1w'):
            url_1w = self.tg_URL_1w + "sendMessage?text={}&chat_id={}".format(bs_msg, self.tg_chat_id)
            response = requests.get(url_1w)
        elif(timeframe=='1d'):
            url_1d = self.tg_URL_1d + "sendMessage?text={}&chat_id={}".format(bs_msg, self.tg_chat_id)
            response = requests.get(url_1d)
        elif (timeframe == '6h'):
            url_6h = self.tg_URL_6h + "sendMessage?text={}&chat_id={}".format(bs_msg, self.tg_chat_id)
            response = requests.get(url_6h)
        elif(timeframe=='4h'):
            url_4h = self.tg_URL_4h + "sendMessage?text={}&chat_id={}".format(bs_msg, self.tg_chat_id)
            response = requests.get(url_4h)
        elif(timeframe=='1h'):
            url_1h = self.tg_URL_1h + "sendMessage?text={}&chat_id={}".format(bs_msg, self.tg_chat_id)
            response = requests.get(url_1h)
        elif(timeframe=='15m'):
            url_15m = self.tg_URL_15m + "sendMessage?text={}&chat_id={}".format(bs_msg, self.tg_chat_id)
            response = requests.get(url_15m)
        elif(timeframe=='5m'):
            #print('INside TelegramBot2: timeframe={}'.format(timeframe))
            url_5m = self.tg_URL_5m + "sendMessage?text={}&chat_id={}".format(bs_msg, self.tg_chat_id)
            response = requests.get(url_5m)
        else:
            logging.error("####Check timeframes####")
            quit(0)

        content = response.content.decode("utf8")
