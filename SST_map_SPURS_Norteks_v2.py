# -*- coding: utf-8 -*-
"""
Read MODIS and VIIRS NPP SST data during the SPURS-1 deployment cruise.


Created on Mon Jul 13 23:21:16 2020
Initially followed Intro_06_Xarray-basics.py tutorial obtained from Chelle Gentemann

@author: jtomf
"""
import sys
sys.path.append('C:/Users/jtomf/Documents/Python/Tom_tools/')

import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import pandas as pd
import datetime as dt
import Tom_tools_v1 as tt

# from scipy import signal
# import Utils

################################
#

plt.close("all")
__figdir__ = "Figz"
savefig_args = {'bbox_inches':'tight', 'pad_inches':0}

###########################
# Load MODIS SST data
#url = 'https://opendap.jpl.nasa.gov/opendap/OceanTemperature/modis/L3/aqua/11um/v2014.0/4km/daily/2012/274/A2012274.L3m_DAY_NSST_sst_4km.nc'
#url = 'https://opendap.jpl.nasa.gov/opendap/OceanTemperature/modis/L3/aqua/11um/v2014.0/4km/daily/2012/273/A2012273.L3m_DAY_NSST_sst_4km.nc'
#url = 'https://opendap.jpl.nasa.gov/opendap/OceanTemperature/modis/L3/aqua/11um/v2014.0/4km/daily/2012/275/A2012275.L3m_DAY_NSST_sst_4km.nc'
daystr = '274'  # 274N is good; also looked at 270-280
Nstr = 'N'  # '' or 'N' for day or night
url = 'https://opendap.jpl.nasa.gov/opendap/OceanTemperature/modis/L3/aqua/11um/v2014.0/4km/daily/2012/' + daystr + '/A2012' + daystr + '.L3m_DAY_' + Nstr + 'SST_sst_4km.nc'

ds_sst = xr.open_dataset(url)

##################
# from http://xarray.pydata.org/en/stable/plotting.html
# xarray plotting functionality is a thin wrapper around the popular matplotlib library. 
# Matplotlib syntax and function names were copied as much as possible, which makes for an easy 
# transition between the two. Matplotlib must be installed before xarray can plot.

SPURSlon = -(38+00.0017/60)
SPURSlat = 24+35.0247/60

fig = plt.figure(figsize=(8, 4))
ds_sst.sst.sel(lat=slice(28,23),lon=slice(-42,-34)).plot(cmap='coolwarm',levels=np.linspace(26,28,15))
plt.axis('tight')
plt.plot(SPURSlon, SPURSlat, 'o', color='k')
plt.title(ds_sst.time_coverage_start)

#Same as above, but zoomed in on the axes used for VIIRS NPP below
fig = plt.figure(figsize=(8, 4))
foo = ds_sst.sst.sel(lat=slice(28, 23), lon=slice(-42, -34)).plot.contourf(cmap='coolwarm', levels=np.linspace(27.15,27.85,20))
plt.axis('tight')
plt.plot(SPURSlon, SPURSlat, 'o', color='k')
plt.title(ds_sst.time_coverage_start)
plt.axis([-38.708669,  -37.26713,  24.23951,  25.3261])
plt.axis('scaled')


fig = plt.figure(figsize=(8, 4))
ds_sst.sst.sel(lat=slice(28,23),lon=slice(-42,-34)).plot.contourf(cmap='coolwarm',levels=np.linspace(26,28,15))
plt.axis('tight')
plt.plot(SPURSlon,SPURSlat,'o',color='k')
plt.title(ds_sst.time_coverage_start)

plt.savefig(__figdir__ + "/Figure1a.png", **savefig_args, dpi=600)


#####################################
# This is AVHRR from VIIRS NPP, not MODIS
# This takes a long time:
url = 'https://thredds.jpl.nasa.gov/thredds/dodsC/OceanTemperature/VIIRS_NPP-OSPO-L3U-v2.61.nc'
ds_npp = xr.open_dataset(url)
ds_sub = ds_npp.sea_surface_temperature.sel(time=slice('20120929','20120930'),lat=slice(28,23),lon=slice(-42,-34))-273.15

ff = ~np.isnan(ds_sub.sel(lat=slice(24.55, 24.45), lon=slice(-38.05, -37.95)).mean('lon').mean('lat'))
ff2 = np.where(ff)
fig = plt.figure(figsize=(8, 4))
plt.plot(ff)
plt.title('Indices of subset with non-nan data')

fig = plt.figure(figsize=(8, 4))
#ds_sub.mean(['time']).plot(cmap='coolwarm',levels=np.linspace(26,28,15))
ds_sub.isel(time=ff2[0][1]).plot(cmap='coolwarm',levels=np.linspace(26,28,15))
plt.plot(SPURSlon,SPURSlat,'o',color='k')


fig= plt.figure(figsize=(8,4))
ds_sub.isel(time=ff2[0][0]).plot(cmap='coolwarm',levels=np.linspace(26,28,15))
plt.plot(SPURSlon,SPURSlat,'o',color='k')

fig= plt.figure(figsize=(8,4))
ds_sub.isel(time=ff2[0][2]).plot(cmap='coolwarm',levels=np.linspace(26,28,15))
plt.plot(SPURSlon,SPURSlat,'o',color='k')


sst_im = ds_sub.isel(time=ff2[0][1])

##############################################
fig= plt.figure(figsize=(8,4))
ds_sub.isel(time=ff2[0][1]).plot(cmap='coolwarm',levels=np.linspace(27.15,27.9,15))
#plt.plot(SPURSlon,SPURSlat,'o',color='k')
plt.axis([-38.708669354838705,  -37.26713709677419,  24.239516041550388,  25.32612009257010])
gpsdata = pd.read_csv('buoy_and_glider_lat_lon.csv')
gpsdata['date_time'] = [tt.matlab2datetime(tval) for tval in gpsdata['mday']]
gpssub = gpsdata.loc[gpsdata['date_time'] >= '201209300000']
gpssub = gpssub.loc[gpssub['date_time'] <= '201209300600']
plt.plot(gpssub['buoy-lon'], gpssub['buoy-lat'], color='k')
plt.plot(gpssub['gldr-lon'], gpssub['gldr-lat'], color='m')
plt.plot(gpssub.iloc[-1]['buoy-lon'], gpssub.iloc[-1]['buoy-lat'], 'o', color='k')
plt.plot(gpssub.iloc[-1]['gldr-lon'], gpssub.iloc[-1]['gldr-lat'], 'o', color='m')
plt.axis('scaled')

plt.savefig(__figdir__ + "/VIIRS_NPP_SST.png",**savefig_args,dpi=600)


##########################################
# Make a smoothed version of SST (ds_sub)
ds = ds_sub.isel(time=ff2[0][1])
sst = np.reshape(ds.data, (len(ds.lat), len(ds.lon)))
N = 3
sst_smooth = tt.run_avg2d(sst, N, 1)
sst_smooth = tt.run_avg2d(sst_smooth, N, 2)


fig = plt.figure(figsize=(6, 4))
plt.contourf(ds.lon, ds.lat, sst_smooth, cmap='coolwarm', levels=np.linspace(27.3,27.8,26))
#plt.plot(SPURSlon,SPURSlat,'o',color='k')
plt.axis('scaled')
plt.colorbar(label='SST ($^\circ$C)')
plt.axis([-38.708669354838705,  -37.26713709677419,  24.239516041550388,  25.32612009257010])



#fig = plt.figure(figsize=(8, 4))
plt.plot(gpssub['buoy-lon'], gpssub['buoy-lat'], color='k')
plt.plot(gpssub['gldr-lon'], gpssub['gldr-lat'], color='m')
plt.plot(gpssub.iloc[-1]['buoy-lon'], gpssub.iloc[-1]['buoy-lat'], 'o', color='k')
plt.plot(gpssub.iloc[-1]['gldr-lon'], gpssub.iloc[-1]['gldr-lat'], 'o', color='m')
plt.axis('scaled')
plt.axis([-38.113580307811965, -37.89454310774521, 24.479272006279203, 24.70908152766072])
plt.xlabel('Longitude ($^\circ$W)')
plt.ylabel('Latitude ($^\circ$N)')

locs, labels = plt.xticks()
labels2 = []
for n in np.arange(len(locs)): 
    labels2.append(str(-round(locs[n],3)))

plt.xticks(locs,labels=labels2)

plt.savefig(__figdir__ + "/VIIRS_NPP_SST_zoom.png",**savefig_args,dpi=600)

