#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 18:42:45 2019

@author: David Chong Tian Wei
"""
import pandas as pd
import numpy as np
from statsmodels.stats.anova import AnovaRM
from statsmodels.stats.multitest import multipletests
from scipy.stats import linregress
from scipy.stats import levene
import statsmodels.api as sm
import statsmodels.formula.api as smf

def getmeanandsd(data, mode, slope, feature):
    return (np.nanmean(data.loc[(data["Mode"] == mode) & (data["Slope"] == slope)][feature]), np.nanstd(data.loc[(data["Mode"] == mode) & (data["Slope"] == slope)][feature]), sum(~np.isnan(data.loc[(data["Mode"] == mode) & (data["Slope"] == slope)][feature])))

features = ["DevFlowAvg", "VTeAvg", "VTDiff", "RRAvg", "MVAvg", "PIPAvg", "MAPAvg", "FiO2Avg", "Overall_spo2", "Overall_etco2", "TiAvg", "PMaxSet"]

data = pd.read_csv("/media/hdd/Clinical School/Year 4/SSC/evelynflowpaper/data/CombinedEFData.csv")
entries = []
for m in data.Mode.unique():
    for s in data.Slope.unique():
        for f in features:
            entry = {}
            entry["Mode"] = m
            entry["Slope"] = s
            entry["Feature"] = f
            entry["Mean"], entry["Std"], entry["N"] = getmeanandsd(data, m, s, f)
            entries.append(entry)
            
output = pd.DataFrame(entries,columns=["Mode","Slope","Feature","N","Mean","Std"]).sort_values(by=["Mode","Slope"])
output.to_csv("/media/hdd/Clinical School/Year 4/SSC/evelynflowpaper/data/Table2.csv", index=False)

models = []

for m in data.Mode.unique():
    for f in features:
        entry = {}
        entry["Mode"] = m
        entry["Feature"] = f
        df = data.loc[data["Mode"] == m][["Sample_ID","Slope",f]]
        dropped = df[np.isnan(df[f])]["Sample_ID"].unique()
        df = df[~df["Sample_ID"].isin(dropped)]
        entry["N"] = len(df["Sample_ID"].unique())
        model = AnovaRM(data=df, depvar=f, within=["Slope"], subject="Sample_ID")
        temp = model.fit().anova_table
        entry["F"] = temp["F Value"].values[0]
        entry["df"] = temp["Num DF"].values[0]
        entry["Den DF"] = temp["Den DF"].values[0]
        entry["P"] = temp["Pr > F"].values[0]
        regression = linregress(df["Slope"],df[f])
        #entry["linregress_p"] = regression[3]
        #entry["linregress_r"] = regression[2]
        l = levene(df[df["Slope"] == 0.08][f],
                   df[df["Slope"] == 0.16][f],
                   df[df["Slope"] == 0.24][f],
                   df[df["Slope"] == 0.32][f],
                   df[df["Slope"] == 0.4][f])
        entry["levene"] = l.pvalue
        #entry["linregress_slope"] = regression[0]
        model = smf.mixedlm(f + " ~ Slope", df, groups=df["Sample_ID"], re_formula="~Slope")
        temp = model.fit()
        entry["slope_p"] = temp.pvalues["Slope"]
        entry["intercept_p"] = temp.pvalues["Intercept"]
        entry["slope"] = temp.params["Slope"]
        entry["intercept"] = temp.params["Intercept"]
        entry["slope_var"] = temp.params["Slope Var"]
        entry["group_var"] = temp.params["Group Var"]
        ci = temp.conf_int()
        entry["slope_lci"] = ci.loc["Slope"][0]
        entry["slope_uci"] = ci.loc["Slope"][1]
        entry["intercept_lci"] = ci.loc["Intercept"][0]
        entry["intercept_uci"] = ci.loc["Intercept"][1]
        models.append(entry)

output = pd.DataFrame(models,columns=["Mode","Feature","N","F","levene","P","df","Den DF","slope","slope_lci","slope_uci","slope_p","intercept","intercept_lci","intercept_uci","intercept_p","slope_var","group_var"]).sort_values(by=["Mode"])
temp = np.concatenate([multipletests(output.loc[output["Mode"] == "PSV-VG"]["P"],method="fdr_bh")[1], multipletests(output.loc[output["Mode"] == "SIPPV-VG"]["P"],method="fdr_bh")[1]])
output["corrected_P"] = temp
output.to_csv("/media/hdd/Clinical School/Year 4/SSC/evelynflowpaper/data/Table2_stats.csv", index=False)
