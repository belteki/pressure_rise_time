#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 11:33:08 2019

@author: david
"""

import os
import re
import datetime
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.stats import linregress
from PIL import Image

WORKING_DIR = "/media/hdd/Clinical School/Year 4/SSC/evelynflowpaper/data"
IMAGE_DIR = "/media/hdd/Clinical School/Year 4/SSC/evelynflowpaper/images"
regexp = re.compile("EF[0-9]{2}")
epoch = datetime.datetime.utcfromtimestamp(0)

etco2readings = []
paco2readings = []

for s in [x for x in os.listdir(WORKING_DIR) if regexp.search(x) is not None]:
    data = pd.read_excel(WORKING_DIR + "/" + s + "/BG_" + s + ".xlsx")
    etco2data = pd.read_csv(WORKING_DIR + "/" + s + "/FCTR_INFANT_NEONATAL_combined.csv", na_values="--")
    for i in range(1,len(data.columns)):
        if type(data.columns[i]) is not datetime.datetime:
            datecomp = datetime.datetime.strptime(data.columns[i].split(".")[0], "%Y-%m-%d %H:%M:%S")
        else:
            datecomp = data.columns[i]
        bgtime = datetime.datetime.combine(datecomp, data.iloc[0,i])
        start = ((bgtime - datetime.timedelta(minutes=12)) - epoch).total_seconds() * 1000.0
        end = ((bgtime - datetime.timedelta(minutes=2)) - epoch).total_seconds() * 1000.0
        etco2avg = np.nanmean(etco2data[(etco2data["Time [ms]"] >= start) & (etco2data["Time [ms]"] <= end)].iloc[:,4].astype(float))
        if not np.isnan(etco2avg):
            etco2readings.append(etco2avg)
            paco2readings.append(data.iloc[4,i])

etco2readings = np.array(etco2readings)
paco2readings = np.array(paco2readings)
lm = linregress(etco2readings, paco2readings)
print(lm)
lobfx = np.linspace(3,7,10)
lobfy = [x*lm[0] + lm[1] for x in lobfx]

def plot(filename, color=True):
    if color:
        tcol = "r--"
        acol = "r"
        pcol = "b"
    else:
        tcol = "k--"
        acol = "k"
        pcol = "grey"
    plt.figure(figsize=(6,4), dpi=600)
    plt.subplot(1,2,1)
    plt.rcParams.update({'font.size': 8})
    plt.scatter(etco2readings, paco2readings, color=pcol)
    plt.plot(lobfx, lobfy,tcol)
    plt.xlabel("EtCO$_2$ [kPa]")
    plt.ylabel("PaCO$_2$ [kPa]")
    plt.grid()
    plt.text(3,8,"y=" + str(round(lm[0],2)) + "x + " + str(round(lm[1],2)))
    plt.text(3,8.25,"N=" + str(len(etco2readings)))
    plt.text(3,7.75,"R=" + str(round(lm[2],2)) + " [" + str(round(lm[2] - 1.96 * lm[4],2)) + "," + str(round(lm[2] + 1.96 * lm[4],2)) + "]")
    plt.text(3,7.5,"p < 0.001")
    plt.title("A", loc="left", fontdict = {"fontsize":20})
    
    plt.subplot(1,2,2)
    delta = paco2readings - etco2readings
    avgs = []
    for i in range(len(etco2readings)):
        avgs.append(np.mean([paco2readings[i],etco2readings[i]]))
    stds = np.std(delta)
    plt.scatter(avgs,delta, color=pcol)
    plt.ylabel("PaCO$_2$ - EtCO$_2$ [kPa]")
    plt.xlabel("Mean of PaCO$_2$ and EtCO$_2$ [kPa]")
    plt.axhline(y=np.mean(delta), color=acol)
    plt.text(4,np.mean(delta) + 0.1,"Mean difference=" + str(round(np.mean(delta),3)))
    plt.axhline(y=np.mean(delta) + stds, color=acol)
    plt.text(4,np.mean(delta) + stds + 0.1,"+1.96SD=" + str(round(np.mean(delta) + stds,3)))
    plt.axhline(y=np.mean(delta) - stds, color=acol)
    plt.text(4,np.mean(delta) - stds + 0.1,"-1.96SD=" + str(round(np.mean(delta) - stds,3)))
    plt.title("B", loc="left", fontdict = {"fontsize":20})
    plt.grid()
    plt.savefig(filename + ".jpg")
    plt.close()
    
    Image.open(filename + ".jpg").save(filename + ".tiff")
    
    print("Mean: " + str(np.mean(delta)))
    print("Min: " + str(np.min(delta)))
    print("Max: " + str(np.max(delta)))

plot(IMAGE_DIR + "/etco2-paco2-correlation")
plot(IMAGE_DIR + "/etco2-paco2-correlation_no_color", False)
