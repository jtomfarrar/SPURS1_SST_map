# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 15:53:57 2020

@author: jtomf
"""

import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import pandas as pd
import datetime as dt


# From a Stackoverflow post by Rich Signell
# https://stackoverflow.com/questions/13965740/converting-matlabs-datenum-format-to-python
def matlab2datetime(matlab_datenum):
    day = dt.datetime.fromordinal(int(matlab_datenum))
    dayfrac = dt.timedelta(days=matlab_datenum%1) - dt.timedelta(days = 366)
    return day + dayfrac


gpsdata = pd.read_csv('buoy_and_glider_lat_lon.csv')
gpsdata['date_time'] = [matlab2datetime(tval) for tval in gpsdata['mday']]


gpssub = gpsdata.loc[gpsdata['date_time'] >= '201209291800']
gpssub = gpssub.loc[gpssub['date_time'] <= '201209300700']


#fig = plt.figure(figsize=(8, 4))
plt.plot(gpssub['buoy-lon'], gpssub['buoy-lat'], color='y')
plt.plot(gpssub['gldr-lon'], gpssub['gldr-lat'], color='m')

plt.plot(gpssub.iloc[-1]['buoy-lon'], gpssub.iloc[-1]['buoy-lat'], 'o', color='y')
plt.plot(gpssub.iloc[-1]['gldr-lon'], gpssub.iloc[-1]['gldr-lat'], 'o', color='m')

plt.axis('scaled')
