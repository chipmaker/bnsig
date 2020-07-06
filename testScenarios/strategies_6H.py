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

from .strategy import Strategy
#TestScenarios
from testScenarios.Buy_testScenarios50Rows import Buy_testScenarios50Rows
from testScenarios.Buy_testScenarios100Rows import Buy_testScenarios100Rows
from testScenarios.barLB_testScenario import barLB_testScenario

class Strategies_6H(Strategy):
#Feb01 2020: Combined TestScenarios
    def __init__(self, args, cbIF):
        """Constructor for $class$"""
        super().__init__(args, cbIF)
        self.name = 'Strategies_6H'
        self.set_strategies()

    def set_strategies(self):
         TS1Dict = {}
         TS1Dict['sym_filename_only'] = 'allAssets.csv'
         TS1Obj = Buy_testScenarios50Rows(self.Config2tfObj, TS1Dict)
         self.tsObjList.append(TS1Obj)
         ###End of Test Scenario1

         #####Test Scenario2
         TS2Dict = {}
         TS2Dict['sym_filename_only'] = 'allAssets100Rows6H.csv'
         TS2Obj = Buy_testScenarios100Rows(self.Config2tfObj, TS2Dict)
         self.tsObjList.append(TS2Obj)
         ###End of Test Scenario2

         #####Test Scenario9
         TS9Dict = {}
         TS9Dict['sym_filename_only'] = 'allAssets.csv'
         TS9Dict['withinBars'] = 4
         TS9Dict['nBuy'] = 5
         TS9Dict['withinBars'] = 12
         TS9Obj = barLB_testScenario(self.Config2tfObj, TS9Dict)
         self.tsObjList.append(TS9Obj)
         ####End of Test Scenario9

