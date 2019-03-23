# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 09:53:38 2019

@author: Sony
"""

import numpy as np 
import pylab 
import scipy.stats as stats

import pandas as pd

a=pd.DataFrame.from_csv("rates.csv")

measurements = np.random.normal(loc = 20, scale = 5, size=100)   
stats.probplot(a["rate"], dist="norm", plot=pylab)

pylab.show()