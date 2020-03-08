#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 11:38:05 2019

@author: David Chong Tian Wei
"""
import re, os
from datetime import datetime
import numpy as np
import pandas as pd

WORKING_DIR = "/media/hdd/Clinical School/Year 4/SSC/evelynflowpaper/data"
p = re.compile("[0-9 -]+\.csv")

epoch = datetime.utcfromtimestamp(0)

def parseTomillis(input):
    if pd.isna(input):
        return np.nan
    else:
        return (datetime.strptime(str(input), '%H:%M:%S %d/%m/%y') - epoch).total_seconds() * 1000
    
for sample in os.listdir(WORKING_DIR):
    if os.path.isdir(WORKING_DIR + "/" + sample):
        cursamplepath = WORKING_DIR + "/" + sample
        tcmfiles = []
        for tcmfile in os.listdir(cursamplepath):
            if p.match(tcmfile) is not None:
                print(cursamplepath + "/" + tcmfile)
                tcmfiles.append(pd.read_csv(cursamplepath + "/" + tcmfile, skiprows=8, sep=";", encoding="utf-16le"))
        if len(tcmfiles) > 0:
            output = pd.concat(tcmfiles, copy=False)
            output.drop(output.columns[6],inplace=True,axis=1)
            output.sort_values(by="Time",inplace=True)
            output["Time [ms]"] = (output["Time"]).apply(parseTomillis)
            output.to_csv(cursamplepath + "/tcm_combined.csv", index=False)
        else:
            print("Warning: No tcm files found")

