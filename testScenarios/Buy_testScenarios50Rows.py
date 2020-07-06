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

from Strategies.s13_bb_rsi import s13_BB_RSI
from Strategies.s8_amfi import s8_AMFI
from Strategies.s18_MFI import s18_MFI
from Strategies.s200_UO import s200_UO
from Strategies.s300_STOCHRSI import s300_STOCHRSI
from Strategies.sHA import sHA
from Strategies.sOBVEMA import sOBVEMA
from Strategies.s600_AFDM import s600_AFDM
from .testScenario import testScenario

class Buy_testScenarios50Rows(testScenario):
    def __init__(self, Config2tf, params):
       """Constructor for $class$"""
       super().__init__(Config2tf, params)
       self.name = 'Buy_testScenarios50Rows'
       self.set_scenarios()

    def set_scenarios(self):
        s13_BB_RSIObj = s13_BB_RSI()
        s13_BB_RSIObj.strategy_name = self.name+' BB_RSI_BUY_SHOW'
        s13_BB_RSIObj.withinBars = 4
        s13_BB_RSIObj.udShow = 1
        s13_BB_RSIObj.rsiTol = 0
        self.stObjList.append(s13_BB_RSIObj)

        s8_AMFIObj = s8_AMFI()
        s8_AMFIObj.strategy_name = self.name+' AMFI_FLIP_BUY_SHOW'
        s8_AMFIObj.withinBars = 2
        s8_AMFIObj.udShow = 1
        self.stObjList.append(s8_AMFIObj)

        s18_MFIObj = s18_MFI()
        s18_MFIObj.strategy_name = self.name + ' MFI5_BUY_SHOW'
        s18_MFIObj.withinBars = 4
        s18_MFIObj.udShow = 1
        s18_MFIObj.mfiPeriod = 5
        s18_MFIObj.mfiOS = 10
        s18_MFIObj.mfiOB = 90
        self.stObjList.append(s18_MFIObj)

        s18_MFIObj2 = s18_MFI()
        s18_MFIObj2.strategy_name = self.name + ' MFI10_BUY_SHOW'
        s18_MFIObj2.withinBars = 4
        s18_MFIObj2.udShow = 1
        s18_MFIObj2.mfiPeriod = 10
        s18_MFIObj2.mfiOS = 20
        s18_MFIObj2.mfiOB = 80
        self.stObjList.append(s18_MFIObj2)

        s200_UOObj = s200_UO()
        s200_UOObj.strategy_name = self.name+' UO_BUY_SHOW'
        s200_UOObj.withinBars = 12
        s200_UOObj.udShow = 1
        s200_UOObj.uoOS = 25
        s200_UOObj.uoOB = 75
        s200_UOObj.TP1 = 5
        s200_UOObj.TP2 = 10
        s200_UOObj.TP3 = 21
        self.stObjList.append(s200_UOObj)

        s300_STOCHRSIObj = s300_STOCHRSI()
        s300_STOCHRSIObj.strategy_name = self.name + ' STOCHRSI_SHOW'
        s300_STOCHRSIObj.withinBars = 4
        s300_STOCHRSIObj.uoOS = 20
        s300_STOCHRSIObj.uoOB = 80
        self.stObjList.append(s300_STOCHRSIObj)

        sHAObj = sHA()
        sHAObj.strategy_name = self.name+' HA_BUY_SHOW'
        sHAObj.withinBars = 4
        sHAObj.udShow = 1
        self.stObjList.append(sHAObj)

        sOBVEMAOBJ = sOBVEMA()
        sOBVEMAOBJ.strategy_name = self.name + '  OBVEMA_SHOW'
        sOBVEMAOBJ.withinBars = self.withinBars
        self.stObjList.append(sOBVEMAOBJ)

        s600_AFDMObj = s600_AFDM()
        s600_AFDMObj.strategy_name = self.name + ' AFDM_BUY_SHOW'
        s600_AFDMObj.withinBars = 8
        #s600_AFDMObj.udShow = 1
        self.stObjList.append(s600_AFDMObj)

