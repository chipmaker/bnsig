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

import dateparser
import pytz
from datetime import datetime
import pandas as pd
import os

def tz_from_utc_ms_ts(utc_ms_ts, tz_info=pytz.timezone('America/Los_Angeles')):
    """Given millisecond utc timestamp and a timezone return dateime

    :param utc_ms_ts: Unix UTC timestamp in milliseconds
    :param tz_info: timezone info
    :return: timezone aware datetime
    """
    # convert from time stamp to datetime
    utc_datetime = datetime.utcfromtimestamp(utc_ms_ts / 1000.)

    # set the timezone to UTC, and then convert to desired timezone
    return utc_datetime.replace(tzinfo=pytz.timezone('UTC')).astimezone(tz_info)

def tz_iso_from_utc_ms_ts(utc_ms_ts, tz_info=pytz.timezone('America/Los_Angeles')):
    """Given millisecond utc timestamp and a timezone return dateime

    :param utc_ms_ts: Unix UTC timestamp in milliseconds
    :param tz_info: timezone info
    :return: timezone aware datetime
    """
    # convert from time stamp to datetime
    utc_datetime = datetime.utcfromtimestamp(utc_ms_ts / 1000.)
    # set the timezone to UTC, and then convert to desired timezone
    tz_utc_datetime = utc_datetime.replace(tzinfo=pytz.timezone('UTC')).astimezone(tz_info)
    #d = tz_utc_datetime.isoformat()
    return tz_utc_datetime.strftime('%Y-%m-%dT%H:%M:%S.000Z')

def date_to_milliseconds(date_str):
    """Convert UTC date to milliseconds

    If using offset strings add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"

    See dateparse docs for formats http://dateparser.readthedocs.io/en/latest/

    :param date_str: date in readable format, i.e. "January 01, 2018", "11 hours ago UTC", "now UTC"
    :type date_str: str
    """
    # get epoch value in UTC
    epoch = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
    # parse our date string
    d = dateparser.parse(date_str)

    #print('Date Str{}. DateParsed{}.tzinfo{} '.format(date_str, d, d.tzinfo))
    # print('{0}.{1} epoch'.format(date_str, epoch))

    # if the date is not timezone aware apply UTC timezone
    if d.tzinfo is None or d.tzinfo.utcoffset(d) is None:
        d = d.replace(tzinfo=pytz.utc)
        # print('{0}.{1} hragoDateStr'.format(date_str, d.tzinfo.utcoffset(d)))
        # print('{0}.{1} hragoDateStr'.format(date_str, d.tzinfo))
        # print('input {0} output {1} DateStr'.format(date_str, d))

    # return the difference in time
    return int((d - epoch).total_seconds() * 1000.0)


def interval_to_milliseconds(interval):
    """Convert a Binance interval string to milliseconds

          :param interval: Binance interval string 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w
    :type interval: str

    :return:
               None if unit not one of m, h, d or w
               None if string not in correct format
         int value of interval in milliseconds
    """
    ms = None
    timeintervals = {
        '1Min': 60,
        '5Min': 300,
        '15Min': 900,
        '1H': 3600,
        # '6h': 21600,
        '1D': 86400,
    }
    seconds_per_unit = {
        "m": 60,
        "h": 60 * 60,
        "d": 24 * 60 * 60,
        "w": 7 * 24 * 60 * 60
    }
    unit = interval[-1]
    if unit in seconds_per_unit:
        try:
            ms = int(interval[:-1]) * seconds_per_unit[unit] * 1000
        except ValueError:
            pass
    elif interval in timeintervals:
        ms = timeintervals[interval]*1000
    return ms

def interval_to_seconds(interval):
    """Convert a Binance interval string to seconds

          :param interval: Binance interval string 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w
    :type interval: str

    :return:
               None if unit not one of m, h, d or w
               None if string not in correct format
         int value of interval in seconds
    """
    sec = None

    timeintervals = {
        '1Min': 60,
        '5Min': 300,
        '15Min': 900,
        '1H': 3600,
        # '6h': 21600,
        '1D': 86400,
    }

    seconds_per_unit = {
        "m": 60,
        "h": 60 * 60,
        "d": 24 * 60 * 60,
        "w": 7 * 24 * 60 * 60
    }
    unit = interval[-1]
    if unit in seconds_per_unit:
        try:
            sec = int(interval[:-1]) * seconds_per_unit[unit]
        except ValueError:
            pass
    elif interval in timeintervals:
        sec = timeintervals[interval]
    return sec

def read_base_file(rbf_folder, rbf_base_file):
    # print("before data_folder: {}. data_folder_type {}. base_file {}".format(rbf_folder, type(rbf_folder), rbf_base_file))
    # rbf_folder=str(rbf_folder)
    # data_folder='.\\data_folder\\binance\\last_run\\1h'
    # print("data_folder: {}. data_folder_type {}. base_file {}".format(data_folder, type(data_folder), base_file))
    files = os.listdir(rbf_folder)
    # print("files list: {}".format(files))
    if rbf_base_file in files:
        try:
            full_file_path = rbf_folder + "\\" + rbf_base_file
            # print("trying to read file {}".format(full_file_path))
            df = pd.read_csv(full_file_path)
        except Exception as e:
            print("Error in reading {}".format(rbf_base_file))
            print(e)
            df = pd.DataFrame()
    else:
        print("######File Not Found. data_folder={}  base_file={}#####".format(rbf_folder, rbf_base_file))
        print("######                  Quitting                  #####")
        quit()
        #df = pd.DataFrame()
    return df


def appendDFToCSV_void(df, csvFilePath, sep=","):
    if not os.path.isfile(csvFilePath):
        # df.to_csv(csvFilePath, mode='a', index=False, sep=sep)
        df.to_csv(csvFilePath, mode='a', index=True, sep=sep)
    elif len(df.columns) != len(pd.read_csv(csvFilePath, nrows=1, sep=sep, index_col='Unnamed: 0').columns):
        raise Exception(
            "Columns do not match!! Dataframe has " + str(len(df.columns)) + " columns. CSV file has " + str(
                len(pd.read_csv(csvFilePath, nrows=1, sep=sep).columns)) + " columns." + pd.read_csv(csvFilePath,
                                                                                                     nrows=1,
                                                                                                     sep=sep).columns.values)
    elif not (df.columns == pd.read_csv(csvFilePath, nrows=1, sep=sep, index_col='Unnamed: 0').columns).all():
        raise Exception("Columns and column order of dataframe and csv file do not match!!")
    else:
        # df.to_csv(csvFilePath, mode='a', index=False, sep=sep, header=False)
        df.to_csv(csvFilePath, mode='a', index=True, sep=sep, header=False)
