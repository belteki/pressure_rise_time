#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 23:49:09 2019

@author: david
"""

import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image


WORKING_DIR = "/media/hdd/Clinical School/Year 4/SSC/evelynflowpaper"
OUTPUT_DIR = WORKING_DIR + "/images"
df = pd.read_csv(WORKING_DIR + "/data/CombinedEFData.csv")
plt.rcParams.update({'font.size': 5})
# ET-CO2
sampleids = ["01","02","03","04","05","07","08","09","10","11","12","13"]
plt.figure(figsize=(6,4), dpi=600)
for i in range(1,13):
    plt.subplot(4,3,i)
    sippv = df.loc[(df["Sample_ID"] == "EF" + sampleids[i-1]) & (df["Mode"] == "SIPPV-VG")].sort_values(by="Slope")
    psv = df.loc[(df["Sample_ID"] == "EF" + sampleids[i-1]) & (df["Mode"] == "PSV-VG")].sort_values(by="Slope")
    plt.plot(sippv["Slope"], sippv["Overall_etco2"],"ko-",label="SIPPV-VG", lw=1)
    plt.plot(psv["Slope"], psv["Overall_etco2"],"k^-",label="PSV-VG", lw=1)
    plt.title("EF" + sampleids[i-1])
    plt.ylim((3,10))
    plt.ylabel("ET-CO$_2$ [kPa]")
    if i >= 10:
        plt.xticks([0.08,0.16,0.24,0.32,0.40])
        plt.xlabel("Time [s]")
    else:
        plt.xticks([])
    plt.legend(loc="upper right")

plt.subplots_adjust(wspace=0.3, hspace=0.3)
    
plt.savefig(OUTPUT_DIR + "/etco2_individualplots.jpg")
plt.close()

Image.open(OUTPUT_DIR + "/etco2_individualplots.jpg").save(OUTPUT_DIR + "/etco2_individualplots.tiff")