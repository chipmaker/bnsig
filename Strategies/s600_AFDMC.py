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
#import logging
from Utils.mylogger import *

class s600_AFDM(object):

    def __init__(self):
        self.strategy_name = 'S600_AFDM'
        logger.info("Initializing s600_AFDM")
        """Constructor for $class$"""
        self.withinBars = 1
        self.udShow = 0
        self.cciFilter = True
        self.cciEMALength = 8
        self.cciTOS = -100
        self.cciTOB = 100

    def run(self, df, row):
        logger.info("Initializing s600_AFDM")
        df = self.AFDM(df)
        return self.scoreboard(df)

    def AFDM(self, df):
        df['DMP_5'] = talib.PLUS_DI(df['High'].values, df['Low'].values, df['Close'].values, timeperiod=5)
        df['DMN_5'] = talib.MINUS_DI(df['High'].values, df['Low'].values, df['Close'].values, timeperiod=5)

        df['DMP_5SH'] = df['DMP_5'].shift(1)
        df['DMN_5SH'] = df['DMN_5'].shift(1)

        columns = ['DMP_5', 'DMN_5', 'DMP_5SH', 'DMN_5SH']

        def dCond(row, columns):
            dBuy = (row['DMP_5SH'] <= row['DMN_5SH']) & (row['DMP_5'] > row['DMN_5'])
            dSell = (row['DMP_5SH'] >= row['DMN_5SH']) & (row['DMP_5'] < row['DMN_5'])
            return dBuy, dSell

        df['dBC'], df['dSC'] = zip(*df.apply(lambda row: dCond(row, columns), axis=1))

        fp = 6  # 12
        sp = 13  # 26
        signalp = 5  # 9

        df['macdLine'], df['macdSignal'], df['histLine'] = talib.MACD(df['Close'].values, fastperiod=fp, slowperiod=sp,
                                                                      signalperiod=signalp)
        df['histLineSH'] = df['histLine'].shift(1)

        columns = ['macdLine', 'histLine', 'histLineSH']

        def mCond(row, columns):
            mBuy = (row['histLine'] > 0) & (row['histLineSH'] <= 0)
            mSell = (row['histLine'] < 0) & (row['histLineSH'] >= 0)
            return mBuy, mSell

        df['mBC'], df['mSC'] = zip(*df.apply(lambda row: mCond(row, columns), axis=1))

        cciTOS = -100
        cciTOB = 100
        cciEMALength = 8
        cciLength = 100

        df['CCI'] = talib.CCI(df['High'], df['Low'], df['Close'], timeperiod=cciLength)
        df['CCIEMA'] = talib.EMA(df['CCI'], timeperiod=cciEMALength)
        df['CCIEMASH'] = df['CCIEMA'].shift(1)

        columns = ['CCI', 'CCIEMA', 'CCIEMASH']

        def cCond(row, columns):
            cBuy = (row['CCIEMA'] < cciTOS) & (row['CCI'] >= row['CCIEMA']) & (row['CCIEMA'] >= row['CCIEMASH'])
            cSell = (row['CCIEMA'] > cciTOB) & (row['CCI'] <= row['CCIEMA']) & (row['CCIEMA'] <= row['CCIEMASH'])
            return cBuy, cSell

        df['cBC'], df['cSC'] = zip(*df.apply(lambda row: cCond(row, columns), axis=1))

        df['ARDN'], df['ARUP'] = self.AROON(df, periods=10)
        df['AR5DN'], df['AR5UP'] = self.AROON(df, periods=5)

        df['AR10BUY'] = ((df['ARUP'] > df['ARDN']) & (df['ARUP'] > 85)) & \
                        ((df['ARUP'].shift(1) < 5) | (df['ARUP'].shift(2) < 5))
        df['AR10SELL'] = ((df['ARDN'] > df['ARUP']) & (df['ARDN'] > 85)) & \
                         ((df['ARDN'].shift(1) < 5) | (df['ARDN'].shift(2) < 5))

        df['AR5BUY'] = ((df['AR5UP'] > df['AR5DN']) & (df['AR5UP'] > 85)) & \
                       ((df['AR5UP'].shift(1) < 5) | (df['AR5UP'].shift(2) < 5))
        df['AR5SELL'] = ((df['AR5DN'] > df['AR5UP']) & (df['AR5DN'] > 85)) & \
                        ((df['AR5DN'].shift(1) < 5) | (df['AR5DN'].shift(2) < 5))

        df['aBC'] = df['AR10BUY'] | df['AR5BUY']
        df['aSC'] = df['AR10SELL'] | df['AR5SELL']

        columns = ['aBC', 'aSC', 'dBC', 'dSC', 'mBC', 'mSC']

        def admCond(row, columns):
            buy = row['aBC'] & row['dBC'] & row['mBC']
            sell = row['aSC'] & row['dSC'] & row['mSC']
            return buy, sell

        df['BUY'], df['SELL'] = zip(*df.apply(lambda row: admCond(row, columns), axis=1))

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

        return [sellvar, buyvar, normaltimevar]

    def AROON(self, df, periods = 25):
        # Returns a dataframe read from filepath with aroon indicator put in columns from col_name
        # col_name - 2 element list, where the first element is the name for aroon up column,
        # and the second is the name for aroon down column
        # Aroon Up = ( N - Nhc) / N * 100
        # Aroon Down = ( N - Nlc) / N * 100
        # where N - periods provided by the function,
        # Nhc, Nlc - periods since N-period high and periods since N-period low respectively
        aroon_up = df['High'].rolling(periods+1).apply(lambda x: x.argmax(), raw=True) / periods * 100
        aroon_down = df['Low'].rolling(periods+1).apply(lambda x: x.argmin(), raw=True) / periods * 100
        return [aroon_down, aroon_up]

