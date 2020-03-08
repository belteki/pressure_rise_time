#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 11:34:13 2019

@author: David Chong Tian Wei
"""

import pandas as pd
import os
import gc

WORKING_DIRECTORY = "/media/hdd/Clinical School/Year 4/SSC/evelynflowpaper/data"
SETTING = "Slope"
OUTPUT_FILE = WORKING_DIRECTORY + "/EFstudybyslope.txt"

df = []

for item in os.listdir(WORKING_DIRECTORY):
    if os.path.isdir(WORKING_DIRECTORY + "/" + item) and item[0:2] == "EF":
        if os.path.exists(WORKING_DIRECTORY + "/" + item + "/predicted_breaths.csv"):
            print(item)
            data = pd.read_csv(WORKING_DIRECTORY + "/" + item + "/" + 
                                   list(filter(lambda x : "fast_Unknown" in x, os.listdir(WORKING_DIRECTORY + "/" + item)))[0], usecols=[0])
            breaths = pd.read_csv(WORKING_DIRECTORY + "/" + item + "/predicted_breaths.csv")
            settings = pd.read_csv(WORKING_DIRECTORY + "/" + item + "/" + 
                                   list(filter(lambda x : "slow_Setting" in x, os.listdir(WORKING_DIRECTORY + "/" + item)))[0])
            changes = settings.loc[settings["Name"]==SETTING]
            if changes.shape[0] > 1:
                periodstart = data.iloc[0,0]
                for i in range(1,changes.shape[0]):
                    entry = {}
                    entry["Sample_ID"] = item
                    entry["Start"] = periodstart
                    entry["End"] = changes.iloc[i,0]
                    entry["Value"] = changes.iloc[i,7]
                    periodstart = entry["End"]
                    df.append(entry)
                entry = {}
                entry["Sample_ID"] = item
                entry["Start"] = periodstart
                entry["End"] = data.iloc[data.shape[0]-1,0]
                entry["Value"] = changes.iloc[i,8]
                df.append(entry)
            else:
                entry = {}
                entry["Sample_ID"] = item
                entry["Start"] = data.iloc[0,0]
                entry["End"] = data.iloc[data.shape[0]-1,0]
                entry["Value"] = changes.iloc[0,8]
                df.append(entry)
            del data
            del breaths
            del settings
            gc.collect()
df = pd.DataFrame(df, columns=["Sample_ID","Start","End","Value"])
df.to_csv(OUTPUT_FILE)
        
