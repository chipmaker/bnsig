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

from Strategies.s11_arcci_flip import s11_ArCCI_FLIP
from Strategies.s15_adx_rsi_cci import s15_ADX_RSI_CCI
from Strategies.s17_crsi import s17_CRSI
from Strategies.sCCI import sCCI
from Strategies.sEMA import sEMA

from .testScenario import testScenario

class Buy_testScenarios100Rows(testScenario):
    def __init__(self, Config2tf, params):
       """Constructor for $class$"""
       super().__init__(Config2tf, params)
       self.name = 'Buy_testScenarios100Rows  '
       self.set_scenarios()

    def set_scenarios(self):
        s11_ArCCI_FLIPObj = s11_ArCCI_FLIP()
        s11_ArCCI_FLIPObj.strategy_name = self.name+' ArCCI_FLIP_BUY_SHOW'
        s11_ArCCI_FLIPObj.withinBars = 2
        s11_ArCCI_FLIPObj.udShow = 1
        self.stObjList.append(s11_ArCCI_FLIPObj)

        s15_ADX_RSI_CCIObj = s15_ADX_RSI_CCI()
        s15_ADX_RSI_CCIObj.strategy_name = self.name+' ADX_RSI_CCI_BUY_SHOW'
        s15_ADX_RSI_CCIObj.withinBars = 4
        s15_ADX_RSI_CCIObj.udShow = 1
        s15_ADX_RSI_CCIObj.cciFilter = True
        s15_ADX_RSI_CCIObj.cciEMALength = 4
        s15_ADX_RSI_CCIObj.cciTOS = 0
        s15_ADX_RSI_CCIObj.cciTOB = 0
        self.stObjList.append(s15_ADX_RSI_CCIObj)

        s17_CRSIObj = s17_CRSI()
        s17_CRSIObj.strategy_name = self.name+' CRSI_SHOW'
        s17_CRSIObj.withinBars = 3
        #s17_CRSIObj.udShow = 1
        self.stObjList.append(s17_CRSIObj)

        sCCIOBJ = sCCI()
        sCCIOBJ.strategy_name = self.name + '  CCI_SHOW'
        sCCIOBJ.withinBars = 4
        sCCIOBJ.cciEMALength = 8
        sCCIOBJ.cciLength = 100
        sCCIOBJ.cciTOS = -100
        sCCIOBJ.cciTOB = 100
        self.stObjList.append(sCCIOBJ)

        sEMAOBJ = sEMA()
        sEMAOBJ.strategy_name = self.name + '  EMA_SHOW'
        sEMAOBJ.withinBars = 4
        self.stObjList.append(sEMAOBJ)
