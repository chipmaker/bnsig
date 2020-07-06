'''
Author: KAL GANDIKOTA
'''
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

import argparse
import sys

from app.cbIF import cbIF
from testScenarios.strategies import Strategies
from testScenarios.strategies_1W import Strategies_1W
from testScenarios.strategies_1D import Strategies_1D
from testScenarios.strategies_6H import Strategies_6H
from testScenarios.strategies_4h import Strategies_4h
from testScenarios.strategies_1H import Strategies_1H
from testScenarios.strategies_30m import Strategies_30m
from testScenarios.strategies_15Min import Strategies_15Min
from testScenarios.strategies_5Min import Strategies_5Min
from testScenarios.strategies_1m import Strategies_1m

def parse_args():
    parser = argparse.ArgumentParser(description='Checker')
    parser.add_argument('-s','--symbol',
                        type=str,
                        help='The Symbol of the Instrument To Download')

    parser.add_argument('-e','--exchange',
                        type=str,
                        required=True,
                        help='The exchange to download from')

    parser.add_argument('-t','--timeframe',
                        type=str,
                        default='1d',
                        choices=['1Min', '5Min', '15Min', '1H', '1h', '4h', '6h', '1d', '1w'],
                        help='The timeframe to download')

    parser.add_argument('-since','--since',
                        type=str,
                        help='The Start Time')

    parser.add_argument('--debug',
                            action ='store_true',
                            help=('Print Sizer Debugs'))

    parser.add_argument('-lastRun_data_folder',
                        type=str
                        )

    return parser.parse_args()

def main():
    """Initializes the application
    """
    #name = __name__
    #print('Main={}'.format(name))

    # Get our arguments
    args=parse_args()

    cbIFObj = cbIF(args)

    if(args.timeframe=='15Min'):
        strategiesObj =Strategies_15Min(args, cbIFObj)
    elif (args.timeframe == '1w'):
        strategiesObj = Strategies_1W(args, cbIFObj)
    elif(args.timeframe=='1d'):
        strategiesObj =Strategies_1D(args, cbIFObj)
    elif(args.timeframe=='4h'):
        strategiesObj =Strategies_4h(args, cbIFObj)
    elif (args.timeframe == '6h'):
        strategiesObj = Strategies_6H(args, cbIFObj)
    elif((args.timeframe=='1H')|(args.timeframe=='1h')):
        strategiesObj =Strategies_1H(args, cbIFObj)
    elif(args.timeframe=='30'):
        strategiesObj =Strategies_30m()
    elif (args.timeframe == '5Min'):
        strategiesObj = Strategies_5Min(args, cbIFObj)
        #args.timeframe = '15Min'
        #print("main: 15M timeframe= {}".format(args.timeframe))
        #Strategies_15MinObj = Strategies_15Min(args, cbIFObj)
    elif (args.timeframe == '1Min'):
        strategiesObj = Strategies_1m(args, cbIFObj)
    else:
        strategiesObj =Strategies()

    strategiesObj.run()
    #strategiesObj.join()
    #Strategies_15MinObj.start()

if __name__ == "__main__":
      #signal.signal(signal.SIGINT, handler)
      try:
          main()
      except KeyboardInterrupt:
          sys.exit(0)

