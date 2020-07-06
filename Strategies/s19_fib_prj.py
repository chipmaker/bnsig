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

import math
from Utils.mylogger import *

class s19_FIB_PRJ(object):

    def __init__(self):
        self.strategy_name = 'S19_FIB_PRJ'
        logger.info("Initializing s19_FIB_PRJ")
        """Constructor for $class$"""
        self.withinBars = 1
        self.udShow = 0
        self.lPrice1 = -1 #-1 trending down, 1 trending up
        self.hPrice = -1 #-1 trending down, 1 trending up
        self.lPrice2 = -1 #-1 trending down, 1 trending up

    def run(self, df, row):
        logger.info("Running s19_FIB_PRJ")
        self.lPrice1 = row['FibLow1']  #contraints[1] #FibHigh
        self.hPrice = row['FibHigh'] #contraints[0] #FibHigh
        self.lPrice2 = row['FibLow2']  #contraints[1] #FibHigh
        if((math.isnan(self.hPrice)) | (math.isnan(self.lPrice1)) | ((self.hPrice < 0) | (self.lPrice1 < 0)|(self.hPrice < self.lPrice1))) :
            print("######### Quitting. check hprice={} and lprice1={}".format(self.hPrice, self.lPrice1))
            quit()

        if(math.isnan(self.lPrice2)) :
            print("######### Quitting. check lprice2={}".format(self.lPrice2))
            quit()

        if((self.udShow == 0)):
            print("######### Quitting. FIB direction must be set. check self.udShow. Value now = {}".format(self.udShow))
            quit()

        df = self.FIB_PRJ(df)
        return self.scoreboard(df)

    def FIB_PRJ(self, df):
        def crossover(myline, src, srcSH):
            return (srcSH <= myline) & (src > myline)

        def crossunder(myline, src, srcSH):
            return (srcSH >= myline) & (src < myline)

        fibdirection = self.udShow
        pricehigh = self.lPrice2 + self.hPrice - self.lPrice1
        pricelow = self.lPrice2

        diff = pricehigh - pricelow

        print("#### check pricehigh={} , pricelow={}, diff={}".format(pricehigh, pricelow, diff))

        diffp236 = diff * 0.236
        diffp382 = diff * 0.382
        diffp50 = diff * 0.5
        diffp618 = diff * 0.618
        diffp786 = diff * 0.786
        diff1p618 = diff * 1.618
        diff2p618 = diff * 2.618
        diff3p618 = diff * 3.618
        diff4p236 = diff * 4.236
        diff6p853 = diff * 6.853
        diff11p089 = diff * 11.089

        # Halfs
        #fibVal_1p618andhalf = (1.618 + (2.618 - 1.618) / 2)
        #fibVal_2p618andhalf = (2.618 + (3.618 - 2.618) / 2)
        #fibVal_4p236andhalf = (4.236 + (6.853 - 4.236) / 2)
        #fibVal_6p853andhalf = (6.853 + (11.089 - 6.853) / 2)
        fibVal_1p618andhalf = 2.118
        fibVal_4p236andhalf = 5.545
        fibVal_6p853andhalf = 8.971

        if (fibdirection == 1):
            fib0 = pricehigh
            fib1 = pricelow
            fib_p236 = fib0 - diffp236
            fib_p382 = fib0 - diffp382
            fib_p50 = fib0 - diffp50
            fib_p618 = fib0 - diffp618
            fib_p786 = fib0 - diffp786
            fib_1p618 = fib0 - diff1p618
            fib_1p618andhalf = fib0 - diff * fibVal_1p618andhalf
            fib_2p618 = fib0 - diff2p618
            #fib_2p618andhalf = fib0 - diff * fibVal_2p618andhalf
            fib_3p618 = fib0 - diff3p618
            fib_4p236 = fib0 - diff4p236
            fib_4p236andhalf = fib0 - diff * fibVal_4p236andhalf
            fib_6p853 = fib0 - diff6p853
            fib_6p853andhalf = fib0 - diff * fibVal_6p853andhalf
            fib_11p089 = fib0 - diff11p089
        elif (fibdirection == -1):
            fib0 = pricelow
            fib1 = pricehigh
            fib_p236 = fib0 + diffp236
            fib_p382 = fib0 + diffp382
            fib_p50 = fib0 + diffp50
            fib_p618 = fib0 + diffp618
            fib_p786 = fib0 + diffp786
            fib_1p618 = fib0 + diff1p618
            fib_1p618andhalf = fib0 + diff * fibVal_1p618andhalf
            fib_2p618 = fib0 + diff2p618
            #fib_2p618andhalf = fib0 + diff * fibVal_2p618andhalf
            fib_3p618 = fib0 + diff3p618
            fib_4p236 = fib0 + diff4p236
            fib_4p236andhalf = fib0 + diff * fibVal_4p236andhalf
            fib_6p853 = fib0 + diff6p853
            fib_6p853andhalf = fib0 + diff * fibVal_6p853andhalf
            fib_11p089 = fib0 + diff11p089

        df['HighSH'] = df['High'].shift(1)
        df['LowSH'] = df['Low'].shift(1)

        columns = ['High', 'HighSH', 'Low', 'LowSH']

        def fib_cond(row, columns):
            cu11p089 = crossunder(fib_11p089, row['High'], row['HighSH'])
            cu6p853andhalf = crossunder(fib_6p853andhalf, row['High'], row['HighSH'])
            cu6p853 = crossunder(fib_6p853, row['High'], row['HighSH'])
            cu4p236andhalf = crossunder(fib_4p236andhalf, row['High'], row['HighSH'])
            cu4p236 = crossunder(fib_4p236, row['High'], row['HighSH'])
            cu3p618 = crossunder(fib_3p618, row['High'], row['HighSH'])
            #cu2p618andhalf = crossunder(fib_2p618andhalf, row['High'], row['HighSH'])
            cu2p618 = crossunder(fib_2p618, row['High'], row['HighSH'])
            cu1p618 = crossunder(fib_1p618, row['High'], row['HighSH'])
            cu1 = crossunder(fib1, row['High'], row['HighSH'])
            cup786 = crossunder(fib_p786, row['High'], row['HighSH'])
            cup618 = crossunder(fib_p618, row['High'], row['HighSH'])
            cup382 = crossunder(fib_p382, row['High'], row['HighSH'])
            cu0 = crossunder(fib0, row['High'], row['HighSH'])

            co11p089 = crossover(fib_11p089, row['Low'], row['LowSH'])
            co6p853andhalf = crossover(fib_6p853andhalf, row['Low'], row['LowSH'])
            co6p853 = crossover(fib_6p853, row['Low'], row['LowSH'])
            co4p236andhalf = crossover(fib_4p236andhalf, row['Low'], row['LowSH'])
            co4p236 = crossover(fib_4p236, row['Low'], row['LowSH'])
            co3p618 = crossover(fib_3p618, row['Low'], row['LowSH'])
            #co2p618andhalf = crossover(fib_2p618andhalf, row['Low'], row['LowSH'])
            co2p618 = crossover(fib_2p618, row['Low'], row['LowSH'])
            co1p618 = crossover(fib_1p618, row['Low'], row['LowSH'])
            co1 = crossover(fib1, row['Low'], row['LowSH'])
            cop786 = crossover(fib_p786, row['Low'], row['LowSH'])
            cop618 = crossover(fib_p618, row['Low'], row['LowSH'])
            cop382 = crossover(fib_p382, row['Low'], row['LowSH'])
            co0 = crossover(fib0, row['Low'], row['LowSH'])

            co11p089Str = 'crossedUP 11p089'
            co6p853andhalfStr = 'crossedUP 6p853andhalf'
            co6p853Str = 'crossedUP 6p853'
            co4p236andhalfStr = 'crossedUP 4p236andhalf'

            cu11p089Str = 'crossedDN 11p089'
            cu6p853andhalfStr = 'crossedDN 6p853andhalf'
            cu6p853Str = 'crossedDN 6p853'
            cu4p236andhalfStr = 'crossedDN 4p236andhalf'

            if (fibdirection == -1):
                cu4p236Str = 'crossedDN 4p236'
                cu3p618Str = 'crossedDN 3p618'
                #cu2p618andhalfStr = 'crossedDN 2p618andhalf'
                cu2p618Str = 'crossedDN 2p618'
                cu1p618Str = 'crossedDN 1p618'
                cu0Str = 'crossedDN 0'
                cu1Str = 'crossedDN 100'
                cup786Str = 'crossedDN 0p786'
                cup618Str = 'crossedDN 0p618'
                cup382Str = 'crossedDN 0p382'

                mystringT =\
                           cu4p236Str if cu4p236 else \
                           cu3p618Str if cu3p618 else \
                           cu2p618Str if cu2p618 else \
                           cu1p618Str if cu1p618 else \
                           cup786Str if cup786 else \
                           cup618Str if cup618 else \
                           cup382Str if cup382 else \
                           cu1Str if cu1 else \
                           cu0Str if cu0 else 'dumb'
            elif (fibdirection == 1):
                co4p236Str = 'crossedUP 4p236'
                co3p618Str = 'crossedUP 3p618'
                #co2p618andhalfStr = 'crossedUP 2p618andhalf'
                co2p618Str = 'crossedUP 2p618'
                co1p618Str = 'crossedUP 1p618'
                co1Str = 'crossedUP 100'
                cop786Str = 'crossedUP 0p786'
                cop618Str = 'crossedUP 0p618'
                cop382Str = 'crossedUP 0p382'
                co0Str = 'crossedUP 0'

                mystringT =\
                           co4p236Str if co4p236 else \
                           co3p618Str if co3p618 else \
                           co2p618Str if co2p618 else \
                           co1p618Str if co1p618 else \
                           co1Str if co1 else \
                           cop786Str if cop786 else \
                           cop618Str if cop618 else \
                           cop382Str if cop382 else \
                           co0Str if co0 else 'dumb'

            mystring = co11p089Str if (co11p089) else \
                       co6p853andhalfStr if (co6p853andhalf) else \
                       co6p853Str if (co6p853) else \
                       co4p236andhalfStr if (co4p236andhalf) else \
                       cu11p089Str if (cu11p089) else \
                       cu6p853andhalfStr if (cu6p853andhalf) else \
                       cu6p853Str if (cu6p853) else \
                       cu4p236andhalfStr if (cu4p236andhalf) else \
                       mystringT

            sell = (fibdirection == -1) & \
                   ((co11p089 | co6p853andhalf | co6p853 | cu11p089 | cu6p853andhalf | cu6p853) | \
                    (co4p236andhalf | cu4p236andhalf) | \
                    (cu4p236 | cu3p618 | cu2p618 | cu1p618 | cu1 |cup786 | cup618 | cup382 |cu0))
            buy = (fibdirection == 1) & \
                  ((co11p089 | co6p853andhalf | co6p853 | cu11p089 | cu6p853andhalf | cu6p853) | \
                   (cu4p236andhalf | co4p236andhalf) | \
                   (co4p236 | co3p618 | co2p618 | co1p618 | co1 | cop786 |  cop618 | cop382 |co0))

            return buy, sell, mystring

        df['BUY'], df['SELL'], df['mystring'] = zip(*df.apply(lambda row: fib_cond(row, columns), axis=1))

        return df

    def scoreboard(self, df):
        if(self.udShow==-1):
            df['BUY'] = False
        elif(self.udShow==1):
            df['SELL'] = False

        columns = ['normal_time', 'BUY', 'SELL', 'mystring']

        #print("#### check pricehigh={} , pricelow={}, diff={}, fib_p786={}, cup786={}, mystr={}, sell={}".format( pricehigh, pricelow, diff, fib_p786, cup786, mystring, sell))
        df2 = df[columns].tail(self.withinBars)
        dfBS = df2[df2['BUY'] | df2['SELL']]
        #print('withinBars={}, dfBS={}'.format(self.withinBars, dfBS))
        if(dfBS.size == 0):
            sellvar = df['SELL'].iloc[-1]
            buyvar =  df['BUY'].iloc[-1]
            normaltimevar = df['normal_time'].iloc[-1]
        else:
            sellvar = dfBS['SELL'].iloc[-1]
            buyvar =  dfBS['BUY'].iloc[-1]
            normaltimevar = str(dfBS['normal_time'].iloc[-1])+'  '+dfBS['mystring'].iloc[-1]

        #print('udShow={}, sellvar={}, buyvar={}, normalvar={}'.format(self.udShow, sellvar, buyvar, normaltimevar))
        return [sellvar, buyvar, normaltimevar]

#df2 = df.tail(self.withinBars)
#df2['BUY'].any()
#df2['SELL'].any()
#return [df['SELL'].iloc[-1], df['BUY'].iloc[-1], df['normal_time']]
#return [df2['SELL'].any(), df2['BUY'].any(), df['normal_time']]
