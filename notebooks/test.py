# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 18:09:18 2021

@author: Ian's
"""

import pandas as pd
import numpy as np

data = pd.read_csv("avocado.csv")
data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
data.sort_values("Date", inplace=True)

def update_charts(region, avocado_type, start_date, end_date):
    
    #print((data.type == avocado_type) & (data.region == region) )
    
    
    mask = (
        (data.region == region)
        & (data.type == avocado_type)
        & (data.Date >= start_date)
        & (data.Date <= end_date)
    )
    
    
    
    filtered_data = data.loc[mask, :]
    
    print(filtered_data)
    
    return 0

update_charts("Chicago", "organic", "2015-01-04", "2015-01-05")

#print(data)