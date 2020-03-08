#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 09:18:01 2019

@author: David Chong Tian Wei
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

wd = "/media/hdd/Clinical School/Year 4/SSC/evelynflowpaper/data/EF01/"

data = pd.read_csv(wd + "predicted_breaths.csv")
#labels = pd.read_csv(wd + "predicted_flow_and_pressure_states.csv")
fast = pd.read_csv(wd + "CsvLogBase_2017-10-02_124729.614_fast_Unknown.csv")
breathtimes = fast.iloc[data["Start"].values,0].values

sippv40 = data.loc[(breathtimes >= 1506947213539) & (breathtimes < 1506948165551)]
sippv08 = data.loc[(breathtimes > 1506951888583) & (breathtimes <= 1506952824549)]
psv08 = data.loc[(breathtimes > 1506955595563)]
psv40 = data.loc[(breathtimes > 1506950025523) & (breathtimes <= 1506950949571)]

def plotPressure(i, l, d, maintext, pos, col=True):
    if col:
        pcol = "r"
        acol = "k"
        fcol = "g"
        hcol = "b"
    else:
        pcol = "k"
        acol = "k"
        fcol = "k"
        hcol = "k"
    plt.subplot(4,2,pos)
    plt.plot(np.arange(0,int(l.iat[i,1]) - int(l.iat[i,0]))/100,d.iloc[int(l.iat[i,0]):int(l.iat[i,1]), 4],label="Pressure", color=pcol)
    plt.title(maintext, loc="left", fontdict = {"fontsize":12})
    plt.ylabel("Pressure [mbar]")
    plt.ylim((0,plt.ylim()[1]))
    plt.axvline((l.iat[i,3] - l.iat[i,0]) / 100, color=acol, linestyle="--") # PIP
    plt.text((l.iat[i,3] - l.iat[i,0]) / 100 - 0.15, plt.ylim()[0] + 0.5, "PRT") # Label PRT
    if l.iat[i,4] - l.iat[i,3] > 3:
        plt.axvspan((l.iat[i,3] - l.iat[i,0])/100, (l.iat[i,4] - l.iat[i,0])/100, facecolor=acol, alpha=0.25)
    
    
    plt.subplot(4,2,pos+2)
    plt.plot(np.arange(0,int(l.iat[i,1]) - int(l.iat[i,0]))/100,d.iloc[int(l.iat[i,0]):int(l.iat[i,1]), 5],label="Flow",color=fcol)
    plt.axhline(0,color=hcol,linestyle="--")
    plt.ylabel("Flow [L/min]")
    plt.xlabel("Time [s]")
    
    plt.axvline((l.iat[i,9] - l.iat[i,0]) / 100, color=acol, linestyle="--") # Inspiration Hold
    plt.text((l.iat[i,9] - l.iat[i,0]) / 100 - 0.25, plt.ylim()[0]+0.1, "Lung\nInflation") # Label Lung Inflation
    plt.axvline((l.iat[i,13] - l.iat[i,0]) / 100, color=acol, linestyle="--") # Expiration Hold
    plt.text((l.iat[i,13] - l.iat[i,0]) / 100 - 0.25, plt.ylim()[1]-1.5, "Lung\nDeflation") # Label Lung Deflation
    if l.iat[i,10] - l.iat[i,9] > 3:
        plt.axvspan((l.iat[i,9] - l.iat[i,0])/100, (l.iat[i,10] - l.iat[i,0])/100, facecolor=acol, alpha=0.25)
        plt.annotate("",xy=(0,plt.ylim()[1]), xytext=((l.iat[i,10] - l.iat[i,0]) / 100, plt.ylim()[1]+0.01), arrowprops=dict(arrowstyle="<->"))
        plt.text((l.iat[i,10] - l.iat[i,0]) / 200, plt.ylim()[1]+0.5,"Ti")
        plt.annotate("",xy=((l.iat[i,10] - l.iat[i,0]) / 100,plt.ylim()[1]), xytext=(plt.xlim()[1], plt.ylim()[1]+0.01), arrowprops=dict(arrowstyle="<->"))
        plt.text(((l.iat[i,10] - l.iat[i,0]) / 100 + plt.xlim()[1]) / 2 , plt.ylim()[1]+0.5,"Te")
    else:
        plt.annotate("",xy=(0,plt.ylim()[1]), xytext=((l.iat[i,10] - l.iat[i,0]) / 100, plt.ylim()[1]+0.01), arrowprops=dict(arrowstyle="<->"))
        plt.text((l.iat[i,9] - l.iat[i,0]) / 200, plt.ylim()[1]+0.5,"Ti")
        plt.annotate("",xy=((l.iat[i,9] - l.iat[i,0]) / 100,plt.ylim()[1]), xytext=(plt.xlim()[1], plt.ylim()[1]+0.01), arrowprops=dict(arrowstyle="<->"))
        plt.text(((l.iat[i,9] - l.iat[i,0]) / 100 + plt.xlim()[1]) / 2 , plt.ylim()[1]+0.5,"Te")
    
plt.rcParams.update({'font.size': 7})
plt.rc('lines', linewidth=2)
plt.figure(figsize=(6,4), dpi=600)
# For plot A SIPPV-VG PRT 0.08
sippv08.iat[sippv08.shape[0]//2,0] -= 3
sippv08.iat[sippv08.shape[0]//2,3] -= 3
sippv08.iat[sippv08.shape[0]//2,4] -= 3
sippv08.iat[sippv08.shape[0]//2,10] -= 3
plotPressure(sippv08.shape[0]//2,sippv08,fast,"A",1)
# For plot B SIPPV-VG PRT 0.40
sippv40.iat[sippv40.shape[0]//2-1,0] -= 3
sippv40.iat[sippv40.shape[0]//2-1,9] += 6
sippv40.iat[sippv40.shape[0]//2-1,13] += 3
plotPressure(sippv40.shape[0]//2-1,sippv40,fast,"B",2)
# For plot C PSV-VG PRT 0.08
plotPressure(10,psv08,fast,"C",5)
# For plot D PSV-VG PRT 0.40
psv40.iat[psv40.shape[0]//2-2,0] -= 3
plotPressure(psv40.shape[0]//2-2,psv40,fast,"D",6)

plt.subplots_adjust(hspace=0.6)
plt.savefig("/media/hdd/Clinical School/Year 4/SSC/evelynflowpaper/images/Figure1.jpg")
plt.close()
Image.open("/media/hdd/Clinical School/Year 4/SSC/evelynflowpaper/images/Figure1.jpg").save("/media/hdd/Clinical School/Year 4/SSC/evelynflowpaper/images/Figure1.tiff")

# For black and white
plt.figure(figsize=(6,4), dpi=600)
# For plot A SIPPV-VG PRT 0.08
plotPressure(sippv08.shape[0]//2,sippv08,fast,"A",1, False)
# For plot B SIPPV-VG PRT 0.40
plotPressure(sippv40.shape[0]//2-1,sippv40,fast,"B",2, False)
# For plot C PSV-VG PRT 0.08
plotPressure(10,psv08,fast,"C",5, False)
# For plot D PSV-VG PRT 0.40
plotPressure(psv40.shape[0]//2-2,psv40,fast,"D",6, False)

plt.subplots_adjust(hspace=0.6)
plt.savefig("/media/hdd/Clinical School/Year 4/SSC/evelynflowpaper/images/Figure1_no_color.jpg")
plt.close()
Image.open("/media/hdd/Clinical School/Year 4/SSC/evelynflowpaper/images/Figure1_no_color.jpg").save("/media/hdd/Clinical School/Year 4/SSC/evelynflowpaper/images/Figure1_no_color.tiff")