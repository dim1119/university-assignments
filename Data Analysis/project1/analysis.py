import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Function that imitates the timeseries 
def func(x):
    return int(1200*((int(x)-45)/8)**3)


#import from statsmodels the ARIMA and ExponentialSmoothing functions
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing


#read the years and publications from the file
series=pd.read_csv('publications.txt',index_col=0,sep='   ',engine='python')


#make the ExponentialSmoothing model
model = ExponentialSmoothing(series,trend="mul")
model_fit = model.fit()
# make prediction
yhat = model_fit.predict()
print(yhat)

#ARIMA code that doesn't work

# create_model=ARIMA(series.values,order=(7,0,7))
# model2 = create_model.fit(disp=0)
# print(model.summary())



#create a figure
plt.figure(figsize=(12,8))

#plot the exponential smoothing graph
plt.plot(yhat.index,yhat, label='Exponential Smoothing')

#plot the data from the xml
plt.plot(series.index,series, label='Publications per year')

#plot the output of the function that I created
#plt.plot(series.index,func(series.index), label="function")

#add the legend and set the limits
plt.legend(loc='best')
plt.xlim([1918,2022])
plt.show()
