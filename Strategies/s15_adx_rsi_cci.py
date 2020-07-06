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

import talib
from Utils.mylogger import *

class s15_ADX_RSI_CCI(object):

    def __init__(self):
        self.strategy_name = 'S15_ADX_RSI_CCI'
        logger.info("Initializing s15_ADX_RSI_CCI")
        """Constructor for $class$"""
        self.withinBars = 1
        self.udShow = 0
        self.cciFilter = True
        self.cciEMALength = 4
        self.cciTOS = -100
        self.cciTOB = 100

    def run(self, df, row):
        logger.info("Initializing s15_ADX_RSI_CCI")
        df = self.ADX_RSI_CCI(df)
        return self.scoreboard(df)

    def ADX_RSI_CCI(self, df):
        rsi30L = 30
        rsi40L = 40
        rsi50L = 50
        rsi60L = 60
        rsi70L = 70

        df['DMP_5'] = talib.PLUS_DI(df['High'].values, df['Low'].values, df['Close'].values, timeperiod=5)
        df['DMN_5'] = talib.MINUS_DI(df['High'].values, df['Low'].values, df['Close'].values, timeperiod=5)
        #df['ADX_5'] = talib.ADX(df['High'].values, df['Low'].values, df['Close'].values, timeperiod=5)

        df['RSI_14'] = talib.RSI(df['Close'], timeperiod=14)

        df['CCI'] = talib.CCI(df['High'], df['Low'], df['Close'], timeperiod=100)
        df['CCIEMA'] = talib.EMA(df['CCI'], timeperiod=self.cciEMALength)

        df['DMP_5SH'] = df['DMP_5'].shift(1)
        df['DMN_5SH'] = df['DMN_5'].shift(1)
        df['RSI_14SH'] = df['RSI_14'].shift(1)
        df['CCIEMASH'] = df['CCIEMA'].shift(1)

        columns = ['RSI_14', 'RSI_14SH']

        def rsi_cond(row, columns):
            rsiBC = ((row['RSI_14SH'] <= rsi30L) & (row['RSI_14'] > rsi30L)) \
                    | ((row['RSI_14SH'] <= rsi40L) & (row['RSI_14'] > rsi40L)) \
                    | ((row['RSI_14SH'] <= rsi50L) & (row['RSI_14'] > rsi50L))
            rsiSC = ((row['RSI_14SH'] >= rsi70L) & (row['RSI_14'] < rsi70L)) \
                    | ((row['RSI_14SH'] >= rsi60L) & (row['RSI_14'] < rsi60L)) \
                    | ((row['RSI_14SH'] >= rsi50L) & (row['RSI_14'] < rsi50L))
            return rsiBC, rsiSC

        df['rsiBC'], df['rsiSC'] = zip(*df.apply(lambda row: rsi_cond(row, columns), axis=1))

        df['rsiBC2'] = df['rsiBC'] | df['rsiBC'].shift(1)
        df['rsiSC2'] = df['rsiSC'] | df['rsiSC'].shift(1)

        columns = ['ADX_5', 'DMP_5', 'DMN_5', 'DMP_5SH', 'DMN_5SH', 'CCI', 'CCIEMA', 'CCIEMASH', 'rsiBC2', 'rsiSC2']

        def adx_rsi_cond(row, columns):
            adxBuy = (row['DMP_5SH'] <= row['DMN_5SH']) & (row['DMP_5'] > row['DMN_5'])
            adxSell = (row['DMP_5SH'] >= row['DMN_5SH']) & (row['DMP_5'] < row['DMN_5'])
            rsiBuy = (row['rsiBC2'])
            rsiSell = (row['rsiSC2'])

            if(self.cciFilter):
                cci_C1 = (row['CCIEMA'] < self.cciTOS) & (row['CCI'] >= row['CCIEMA']) & (row['CCIEMA'] >= row['CCIEMASH'])
                cci_C2 = (row['CCIEMA'] > self.cciTOB) & (row['CCI'] <= row['CCIEMA']) & (row['CCIEMA'] <= row['CCIEMASH'])

            cciBuy = cci_C1 if self.cciFilter else True
            cciSell = cci_C2 if self.cciFilter else True

            buy = (adxBuy & rsiBuy & cciBuy)
            sell = (adxSell & rsiSell & cciSell)
            #buy = (adxBuy & rsiBuy)
            #sell = (adxSell & rsiSell)
            return buy, sell

        df['BUY'], df['SELL'] = zip(*df.apply(lambda row: adx_rsi_cond(row, columns), axis=1))

        return df

    def scoreboard(self, df):
        if(self.udShow==-1):
            df['BUY'] = False
        elif(self.udShow==1):
            df['SELL'] = False

        columns = ['normal_time', 'BUY', 'SELL']
        df2 = df[columns].tail(self.withinBars)
        dfBS = df2[df2['BUY'] | df2['SELL']]
        #print('dfBS={}'.format(dfBS))
        if(dfBS.size == 0):
            sellvar = df['SELL'].iloc[-1]
            buyvar =  df['BUY'].iloc[-1]
            normaltimevar = df['normal_time'].iloc[-1]
        else:
            sellvar = dfBS['SELL'].iloc[-1]
            buyvar =  dfBS['BUY'].iloc[-1]
            normaltimevar = dfBS['normal_time'].iloc[-1]

        #print('udShow={}, sellvar={}, buyvar={}, normalvar={}'.format(self.udShow, sellvar, buyvar, normaltimevar))
        return [sellvar, buyvar, normaltimevar]

#df2 = df.tail(self.withinBars)
#df2['BUY'].any()
#df2['SELL'].any()
#return [df['SELL'].iloc[-1], df['BUY'].iloc[-1], df['normal_time']]
#return [df2['SELL'].any(), df2['BUY'].any(), df['normal_time']]
