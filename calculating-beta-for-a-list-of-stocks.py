# ================================================================================

#Calculating CAPM beta factor for a list of different stocks relative to an index
#Author: ManuFinancialTech
#https://github.com/ManuFinancialTech

# =================================================================================

#Imports
import numpy as np
from scipy import stats
import datetime
import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt

#Inputs
interval = 'd'
timedelta = 1900
tickers = ["DPW.DE","VNA.DE","EOAN.DE","FRE.DE","BEI.DE","LHA.DE","DB1.DE", "DTE.DE","FME.DE","SAP.DE","BMW.DE",
           "BAYN.DE","ALV.DE","DAI.DE","SIE.DE","VOW3.DE","RWE.DE","MUV2.DE","MRK.DE","ADS.DE","HEN3.DE","BAS.DE",
           "1COV.DE","CON.DE","HEI.DE","LIN.DE","IFX.DE","DBK.DE","TKA.DE"]
index = '^GDAXI'

#Download historical data for example stocks
ohlc = {}           
attempt = 0
drop = []
while len(tickers) != 0 and attempt <= 5:
    tickers = [j for j in tickers if j not in drop]
    for i in range(len(tickers)):
        try:
            ohlc[tickers[i]] = pdr.get_data_yahoo(tickers[i],datetime.date.today()-datetime.timedelta(timedelta),datetime.date.today(),interval=interval)
            ohlc[tickers[i]].dropna(inplace = True)
            drop.append(tickers[i])       
        except:
            print(tickers[i]," :failed to fetch data...retrying")
            continue
    attempt+=1
tickers = ohlc.keys()

#Download historical data for example index
ohlc_index = pdr.get_data_yahoo(index,datetime.date.today()-datetime.timedelta(timedelta),datetime.date.today(),interval=interval)

#Calculate simple rate of return
ohlc_index['Pct Change'] = ohlc_index['Adj Close'].pct_change().values 
for ticker in tickers:
    ohlc[ticker]['Pct Change'] = ohlc[ticker]['Adj Close'].pct_change().values 

#Delete possible length mismatches
ohlc_new = {} 
for ticker in tickers:
    idx = ohlc[ticker].index.intersection(ohlc_index.index)
    ohlc_index_new = ohlc_index.loc[idx]
    ohlc_new[ticker] = ohlc[ticker].loc[idx]
    
#Delete data where no return could be calculated 
ohlc_index_new = ohlc_index_new.dropna()
for ticker in tickers:
    ohlc_new[ticker] = ohlc_new[ticker].dropna()
   
#Plotting Results with linear regression
results = {}
results[timedelta] = {}  
for ticker in tickers:
    results[timedelta][ticker] = {} 

for ticker in tickers:
    slope, intercept, r, p, std_err = stats.linregress(ohlc_index_new['Pct Change'], ohlc_new[ticker]['Pct Change'])  
    r_squared = r**2
    x_curve = np.linspace(np.amin(ohlc_index_new['Pct Change']), np.amax(ohlc_index_new['Pct Change']))
    y_curve = slope * x_curve + intercept
    plt.plot(ohlc_index_new['Pct Change'], ohlc_new[ticker]['Pct Change'], 'r.', alpha = 0.2)
    plt.plot(x_curve, y_curve, 'k')
    plt.xlabel(index + ' Return')
    plt.ylabel(ticker + ' Return')
    plt.title('CAPM Beta Factor = ' + str(slope) + '   R-Squared = ' + str(r_squared))
    plt.grid(True)
    plt.show()
    results[timedelta][ticker]['Beta'] = slope
    results[timedelta][ticker]['R Squared'] = r_squared









