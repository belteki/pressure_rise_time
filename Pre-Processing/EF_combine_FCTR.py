#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 09:22:50 2019

@author: David Chong Tian Wei
"""
import os
import pandas as pd
import numpy as np
from datetime import datetime

epoch = datetime.utcfromtimestamp(0)

def parseTomillis(input):
    if pd.isna(input):
        return np.nan
    else:
        return (datetime.strptime(str(input), '%b %d,%y,%H:%M:%S') - epoch).total_seconds() * 1000

WORKING_DIRECTORY = "/media/david/Ventilation/Raw_data/Draeger/Evelyn_flow_study"
for item in os.listdir(WORKING_DIRECTORY):
    if os.path.isdir(WORKING_DIRECTORY + "/" + item) and item[0:2] == "EF":
        paths = list(filter(lambda x : "FCTR_INFANT_NEONATAL_1" in x, os.listdir(WORKING_DIRECTORY + "/" + item)))
        data = []
        for p in paths:
            data.append(pd.read_csv(WORKING_DIRECTORY + "/" + item + "/" + p, sep="\t", skiprows=[0,1,2,3,5], encoding="UTF-16"))
        data = pd.concat(data)
        time = (data["Date"] + "," + data["Time"]).apply(parseTomillis)
        data["Time [ms]"] = time;
        data.to_csv(WORKING_DIRECTORY + "/" + item + "/FCTR_INFANT_NEONATAL_combined.csv")
