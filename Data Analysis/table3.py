#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 22:30:48 2019

@author: david
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf

def subset(data, m, f):
    df = data.loc[data["Mode"] == m][["Sample_ID","Slope",f]]
    dropped = df[np.isnan(df[f])]["Sample_ID"].unique()
    df = df[~df["Sample_ID"].isin(dropped)]
    return df

data = pd.read_csv("/media/hdd/Clinical School/Year 4/SSC/evelynflowpaper/data/CombinedEFData.csv")

#PSV-VG Device Flow
f = "DevFlowAvg"
m = "PSV-VG"

df = subset(data, m, f)
md = smf.mixedlm(f + " ~ Slope", df, groups=df["Sample_ID"], re_formula="~Slope")
mdf = md.fit()
print(mdf.summary())

#PSV-VG Ti
f = "TiAvg"
m = "PSV-VG"

df = subset(data, m, f)
md = smf.mixedlm(f + " ~ Slope", df, groups=df["Sample_ID"], re_formula="~Slope")
mdf = md.fit()
print(mdf.summary())

#PSV-VG PIP
f = "PIPAvg"
m = "PSV-VG"

df = subset(data, m, f)
md = smf.mixedlm(f + " ~ Slope", df, groups=df["Sample_ID"], re_formula="~Slope")
mdf = md.fit()
print(mdf.summary())

#SIPPV-VG MAP
f = "MAPAvg"
m = "SIPPV-VG"

df = subset(data, m, f)
md = smf.mixedlm(f + " ~ Slope", df, groups=df["Sample_ID"], re_formula="~Slope")
mdf = md.fit()
print(mdf.summary())

#SIPPV-VG MAP
f = "Overall_etco2"
m = "SIPPV-VG"

df = subset(data, m, f)
md = smf.mixedlm(f + " ~ Slope", df, groups=df["Sample_ID"], re_formula="~Slope")
mdf = md.fit()
print(mdf.summary())

#SIPPV-VG MAP
f = "Overall_spo2"
m = "SIPPV-VG"

df = subset(data, m, f)
md = smf.mixedlm(f + " ~ Slope", df, groups=df["Sample_ID"], re_formula="~Slope")
mdf = md.fit()
print(mdf.summary())
