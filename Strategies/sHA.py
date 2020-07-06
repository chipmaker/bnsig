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

import logging
import pandas as pd


class sHA(object):

    def __init__(self):
        self.strategy_name = 'sHA'
        logging.info("Initializing sHA")
        """Constructor for $class$"""
        self.withinBars = 1
        self.udShow = 0
        self.minbCnt = 1
        self.minsCnt = 1
        self.maxbCnt = 3
        self.maxsCnt = 3

    def run(self, df, row):
        logging.info("Initializing sHA")
        dfHA = self.heikin_ashi(df)
        dfHA = self.sHA1(dfHA)
        # print('{}'.format(dfHA))
        return self.scoreboard(dfHA, row)

    def sHA1(self, dfHA):
        minbCnt = self.minbCnt
        minsCnt = self.minsCnt
        maxbCnt = self.maxbCnt
        maxsCnt = self.maxsCnt

        columns = ['Close', 'Open']

        def ha_cond(row, columns):
            bc = (row['Open'] < row['Close'])
            sc = (row['Open'] > row['Close'])
            return bc, sc

        dfHA['BC'], dfHA['SC'] = zip(*dfHA.apply(lambda row: ha_cond(row, columns), axis=1))

        dfHA['bCnt1'] = dfHA['BC'].groupby((dfHA['BC'] != dfHA['BC'].shift()).cumsum()).cumcount() + 1

        dfHA['sCnt1'] = dfHA['SC'].groupby((dfHA['SC'] != dfHA['SC'].shift()).cumsum()).cumcount() + 1

        columns = ['BC', 'bCnt1', 'SC', 'sCnt1']

        def ha_cond2(row, columns):
            bc = 0 if (row['BC'] == False) else row['bCnt1']
            sc = 0 if (row['SC'] == False) else row['sCnt1']
            return bc, sc

        dfHA['bCnt'], dfHA['sCnt'] = zip(*dfHA.apply(lambda row: ha_cond2(row, columns), axis=1))

        columns = ['bCnt', 'sCnt']
        def ha_cond3(row, columns):
            bc = (row['bCnt'] > minbCnt) & (row['bCnt'] < maxbCnt)
            sc = (row['sCnt'] > minsCnt) & (row['sCnt'] < maxsCnt)
            return bc, sc

        dfHA['BUY'], dfHA['SELL'] = zip(*dfHA.apply(lambda row: ha_cond3(row, columns), axis=1))
        return dfHA

    def scoreboard(self, df, row):
        if (self.udShow == -1):
            df['BUY'] = False
        elif (self.udShow == 1):
            df['SELL'] = False

        columns = ['normal_time', 'BUY', 'SELL', 'bCnt', 'sCnt']
        df2 = df[columns].tail(self.withinBars)
        dfBS = df2[df2['BUY'] | df2['SELL']]
        # print('dfBS={}'.format(dfBS))
        if (dfBS.size == 0):
            sellvar = df['SELL'].iloc[-1]
            buyvar = df['BUY'].iloc[-1]
            normaltimevar = df['normal_time'].iloc[-1]
        else:
            sellvar = dfBS['SELL'].iloc[-1]
            buyvar = dfBS['BUY'].iloc[-1]
            normaltimevar = str(dfBS['normal_time'].iloc[-1]) + '  bCnt=' + str(dfBS['bCnt'].iloc[-1]) + ' sCnt=' + str(
                dfBS['sCnt'].iloc[-1])

        if 'Notes' in row:
            normaltimevar = str(normaltimevar) + '  ' + str(row['Notes'])
        # print('udShow={}, sellvar={}, buyvar={}, normalvar={}'.format(self.udShow, sellvar, buyvar, normaltimevar))
        return [sellvar, buyvar, normaltimevar]

    def heikin_ashi(self, df):
        heikin_ashi_df = pd.DataFrame(index=df.index.values, columns=['Open', 'High', 'Low', 'Close', 'normal_time'])

        heikin_ashi_df['Close'] = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4

        for i in range(len(df)):
            if i == 0:
                heikin_ashi_df.iat[0, 0] = df['Open'].iloc[0]
            else:
                heikin_ashi_df.iat[i, 0] = (heikin_ashi_df.iat[i - 1, 0] + heikin_ashi_df.iat[i - 1, 3]) / 2

        heikin_ashi_df['High'] = heikin_ashi_df.loc[:, ['Open', 'Close']].join(df['High']).max(axis=1)

        heikin_ashi_df['Low'] = heikin_ashi_df.loc[:, ['Open', 'Close']].join(df['Low']).min(axis=1)
        heikin_ashi_df['normal_time'] = df['normal_time'].shift(-1)

        return heikin_ashi_df
