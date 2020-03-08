#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 16:39:57 2019

@author: david
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from PIL import Image

plt.rcParams.update({'font.size': 6})

data = pd.read_csv("/media/hdd/Clinical School/Year 4/SSC/evelynflowpaper/data/CombinedEFData.csv")
def plot(filename, col=True):
    if col:
        rcol = "r--"
        pcol = "b"
    else:
        rcol = "k--"
        pcol = "grey"
    plt.figure(figsize=(6,4), dpi=600)
    
    plt.subplot(1,3,1)
    tipsv = data[["Sample_ID","Slope","TiAvg"]].loc[data["Mode"]=="PSV-VG"].dropna()
    tipsvregression = linregress(tipsv["Slope"],tipsv["TiAvg"])
    plt.scatter(tipsv["Slope"], tipsv["TiAvg"], color=pcol)
    plt.title("A", loc="left", fontdict = {"fontsize":15})
    
    plt.ylabel("Inspiratory Time [s]")
    plt.xlabel("Pressure Rise Time [s]")
    plt.plot(np.linspace(0.08,0.4), np.linspace(0.08,0.4) * tipsvregression[0] + tipsvregression[1], rcol, linewidth=2.0)
    plt.text(0.1,0.5,"p < 0.0001")
    plt.xticks(np.arange(0,0.5,step=0.08), rotation="vertical")
    
    plt.subplot(1,3,2)
    pippsv = data[["Sample_ID","Slope","PIPAvg"]].loc[data["Mode"]=="PSV-VG"].dropna()
    pippsvregression = linregress(pippsv["Slope"],pippsv["PIPAvg"])
    plt.scatter(pippsv["Slope"], pippsv["PIPAvg"], color=pcol)
    plt.title("B", loc="left", fontdict = {"fontsize":15})
    
    plt.ylabel("Peak Inspiratory Pressure [kPa]")
    plt.xlabel("Pressure Rise Time [s]")
    plt.plot(np.linspace(0.08,0.4), np.linspace(0.08,0.4) * pippsvregression[0] + pippsvregression[1], rcol, linewidth=2.0)
    plt.text(0.25,25,"p= 0.003")
    plt.xticks(np.arange(0,0.5,step=0.08), rotation="vertical")
    
    mapsippv = data[["Sample_ID","Slope","MAPAvg"]].loc[data["Mode"]=="SIPPV-VG"].dropna()
    mapsippvregression = linregress(mapsippv["Slope"],mapsippv["MAPAvg"])
    
    plt.subplot(1,3,3)
    plt.scatter(mapsippv["Slope"],mapsippv["MAPAvg"], color=pcol)
    plt.title("C", loc="left", fontdict = {"fontsize":15})
    
    plt.ylabel("Mean Airway Pressure [kPa]")
    plt.xlabel("Pressure Rise Time [s]")
    plt.plot(np.linspace(0.08,0.4), np.linspace(0.08,0.4) * mapsippvregression[0] + mapsippvregression[1], rcol, linewidth=2.0)
    plt.xticks(np.arange(0,0.5,step=0.08), rotation="vertical")
    plt.text(0.25,12,"p=0.001")
    
    plt.subplots_adjust(wspace=0.35)
    plt.savefig(filename + ".jpg")
    plt.close()
    Image.open(filename + ".jpg").save(filename + ".tiff")
    
plot("/media/hdd/Clinical School/Year 4/SSC/evelynflowpaper/images/Figure2")
plot("/media/hdd/Clinical School/Year 4/SSC/evelynflowpaper/images/Figure2_no_color", False)