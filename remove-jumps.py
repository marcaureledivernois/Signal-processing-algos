"""
This script removes discontinuities/jumps in a time-serie. It computes the median of the beginning of a segment and the median of the end of the previous segment. 
It then shifts the rest of the time-serie based on the difference between the medians. The result is a signal corrected from discontinuities.
This algorithm keeps the potential trends inter-segments and intra-segments.
"""

import pandas as pd
import numpy as np

ones = list(np.ones(30))
ones.append(np.nan)

twos = list(2*np.ones(50)*3)
twos.append(np.nan)

threes = list(3*np.ones(30))
threes.append(np.nan)

fours = list(4*np.ones(30))
fours.append(np.nan)

fives = list(5*np.ones(30))
fives.append(np.nan)

fives = list(3*np.ones(30))
fives.append(np.nan)

nans = np.empty((15))
nans[:] = np.NaN
nans = list(nans)
                
numbers = [*ones,*fives,*nans, *twos, *fours, *fours, *fives, *threes,*ones,*fives] 

test = pd.DataFrame(data={'data':numbers})
test['isnull'] = test.isnull()*1
test['diff'] = test['isnull'].diff()
first_valid = test['diff']==-1
last_valid = test['diff'].shift(-1)==1
list_first_valid = test.index[first_valid].tolist()
list_last_valid = test.index[last_valid].tolist()

if ~np.isnan(test.loc[0,'data']):
    list_first_valid.insert(0,0)
    
if ~np.isnan(test.loc[test.index[-1],'data']):
    list_last_valid.append(test.index[-1])    

#add random noise
test['data'] += np.random.normal(0,0.1,test.shape[0])
    
#add a trend    
#BETA = (5-test.loc[0,'data'])/(test.shape[0]) # LINEAR TREND
#BETA = 0                                       # NO TREND
test['data'] += BETA*test.index 

#add a quadratic trend
BETA = 0.01  
#test['data'] += BETA*test.index**2

#add sinusoidal trend
test['data'] += 0.3*np.sin(np.linspace(0,100,test.shape[0]))

test['corrected_data'] = np.nan

i=0
WINDOW_SIZE = 5

test.loc[list_first_valid[i]:list_last_valid[i],'corrected_data'] = test.loc[list_first_valid[i]:list_last_valid[i],'data']
median_end = np.median(test.loc[list_first_valid[i]:list_last_valid[i],'corrected_data'].tail(WINDOW_SIZE))

for i in range(1,len(list_first_valid)):
    median_start = np.median(test.loc[list_first_valid[i]:list_last_valid[i],'data'].head(WINDOW_SIZE))
    shift = median_start - median_end
    test.loc[list_first_valid[i]:list_last_valid[i],'corrected_data'] = test.loc[list_first_valid[i]:list_last_valid[i],'data']  - shift
    median_end = np.median(test.loc[list_first_valid[i]:list_last_valid[i],'corrected_data'].tail(WINDOW_SIZE))

