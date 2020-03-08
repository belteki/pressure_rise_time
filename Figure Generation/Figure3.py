#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 18:26:56 2019

@author: david
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image


def plotBar(df, feature, pos, ylabel, maintext, ymin, ymax):
    counter = 0
    minval = None
    maxval = None
    plt.subplot(1,2,pos)
    for mode in df.Mode.unique():
        barheights = {}
        barsdevs = {}
        for slope in np.sort(df.Slope.unique()):
            barheights[slope] = np.mean(df[(df["Mode"]==mode) & (df["Slope"]==slope)][feature])
            barsdevs[slope] = 2.262 * np.std(df[(df["Mode"]==mode) & (df["Slope"]==slope)][feature]) / np.sqrt(df[(df["Mode"]==mode) & (df["Slope"]==slope)].shape[0])
        if mode == "SIPPV-VG":
            plt.bar(np.arange(0,5) - (0.4 * counter), barheights.values(), label=mode, width=0.35, yerr = barsdevs.values(), color="grey", edgecolor="black", capsize=5)
        else:
            plt.bar(np.arange(0,5) + (0.4 * counter), barheights.values(), label=mode, width=0.35, yerr = barsdevs.values(), color="white", edgecolor="black", capsize=5)
        if maxval == None:
            maxval = np.amax(np.array(list(barheights.values())) + np.array(list(barsdevs.values())))
        elif np.amax(np.array(list(barheights.values())) + np.array(list(barsdevs.values()))) >  maxval:
            maxval = np.amax(np.array(list(barheights.values())) + np.array(list(barsdevs.values())))
        if minval == None:
            minval = np.amin(np.array(list(barheights.values())) - np.array(list(barsdevs.values())))
        elif np.amin(np.array(list(barheights.values())) - np.array(list(barsdevs.values()))) <  minval:
            minval = np.amin(np.array(list(barheights.values())) - np.array(list(barsdevs.values())))
        counter += 1
        plt.xticks(np.arange(0,5), list(barheights.keys()))
    
    plt.xlabel("Set Pressure Rise Time [s]")
    plt.ylabel(ylabel)
    plt.title(maintext, loc="left", fontdict = {"fontsize":30})
    plt.ylim(ymin, ymax)
    plt.legend(loc="upper right")

WORKING_DIR = "/media/hdd/Clinical School/Year 4/SSC/evelynflowpaper"
OUTPUT_DIR = WORKING_DIR + "/images"
df = pd.read_csv(WORKING_DIR + "/data/CombinedEFData.csv")

plt.rcParams.update({'font.size': 10})
plt.figure(figsize=(6,4), dpi=600)

plotBar(df, "Overall_spo2", 1, "SpO$_2$ [%]", "A", 84, 100)
plotBar(df, "Overall_etco2", 2, "ET-CO$_2$ [kPa]", "B", 4, 7)

plt.subplots_adjust(wspace=0.25)
plt.savefig(OUTPUT_DIR + "/Figure3.jpg")
plt.close()
Image.open(OUTPUT_DIR + "/Figure3.jpg").save(OUTPUT_DIR + "/Figure3.tiff")