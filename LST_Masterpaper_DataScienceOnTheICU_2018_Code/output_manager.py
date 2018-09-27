# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 15:00:14 2018

@author: grego
"""

import pandas as pd
import time

df = pd.read_pickle("output.pkl")
timestr = time.strftime("%Y%m%d-%H%M%S")
filename = "./backup5/output5-"+timestr
df.to_excel(filename+".xlsx")
df.to_pickle(filename+".pkl")
