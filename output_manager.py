# -*- coding: utf-8 -*-

import pandas as pd
import time

df = pd.read_pickle("output.pkl")
timestr = time.strftime("%Y%m%d-%H%M%S")
filename = "./backup/output-"+timestr
df.to_excel(filename+".xlsx")
df.to_pickle(filename+".pkl")
