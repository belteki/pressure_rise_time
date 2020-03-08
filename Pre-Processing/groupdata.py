#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 13:34:24 2019

@author: David Chong Tian Wei
"""
import pandas as pd
import numpy as np
import math
import os

#Directories
WORKING_DIRECTORY = "/media/hdd/Clinical School/Year 4/SSC/evelynflowpaper/data"
INDEX = WORKING_DIRECTORY + "/EFstudybyslope.txt"
OUTPUTFILE = WORKING_DIRECTORY + "/CombinedEFData.csv"

#Filter params
MIN_LENGTH = 20
MAX_LENGTH = 300
PF_CORR_THRESHOLD = 0
SYNC_VS_BACKUP_THRESHOLD = 0

# Create entry for each slope-ventilator-sample combi
def createEntry(sample, row, mode, firstminute, lastminute, physiology, breaths, tcm, raw_data, slow_data, settings, weight):
    entry = {}
    entry["Sample_ID"] = sample
    entry["Slope"] = row["Value"]
    entry["Mode"] = groups.iloc[group_index,2]
    entry["Seconds"] = lastminute - firstminute + 120000
    entry["Starting_etco2"] = np.nanmean(physiology.loc[physiology["Time [ms]"] <= firstminute].iloc[:,4].astype("float64"))
    entry["Starting_rr"] = np.nanmean(physiology.loc[physiology["Time [ms]"] <= firstminute].iloc[:,5].astype("float64"))
    entry["Starting_spo2"] = np.nanmean(physiology.loc[physiology["Time [ms]"] <= firstminute].iloc[:,6].astype("float64"))
    entry["Starting_pr"] = np.nanmean(physiology.loc[physiology["Time [ms]"] <= firstminute].iloc[:,7].astype("float64"))
    entry["Ending_etco2"] = np.nanmean(physiology.loc[physiology["Time [ms]"] >= lastminute].iloc[:,4].astype("float64"))
    entry["Ending_rr"] = np.nanmean(physiology.loc[physiology["Time [ms]"] >= lastminute].iloc[:,5].astype("float64"))
    entry["Ending_spo2"] = np.nanmean(physiology.loc[physiology["Time [ms]"] >= lastminute].iloc[:,6].astype("float64"))
    entry["Ending_pr"] = np.nanmean(physiology.loc[physiology["Time [ms]"] >= lastminute].iloc[:,7].astype("float64"))
    entry["Overall_etco2"] = np.nanmean(physiology.iloc[:,4].astype("float64"))
    #entry["Overall_etco2_absolute"] = np.nanmean(physiology.iloc[:,4].astype("float64"))
    entry["Overall_rr"] = np.nanmean(physiology.iloc[:,5].astype("float64"))
    entry["Overall_spo2"] = np.nanmean(physiology.iloc[:,6].astype("float64"))
    entry["Overall_pr"] = np.nanmean(physiology.iloc[:,7].astype("float64"))
    entry["MAPAvg"] = np.nanmean(slow_data["5001|Pmean [mbar]"])
    entry["FiO2Avg"] = np.nanmean(slow_data["5001|FiO2 [%]"])
    entry["DevFlowAvg"] = np.nanmean(slow_data["5001|FlowDev [L/min]"])
    entry["VTeAvg"] = np.nanmean(slow_data["5001|VTmand [mL]"] / weight)
    entry["PIPAvg"] = np.nanmean(slow_data["5001|PIP [mbar]"])
    entry["RRAvg"] = np.nanmean(slow_data["5001|RR [1/min]"])
    entry["MVAvg"] = np.nanmean(slow_data["5001|MV [L/min]"] / weight)
    entry["RRSet"] = settings["Value New"].loc[settings["Name"] == "RR"].iat[0]
    entry["VTSet"] = settings["Value New"].loc[settings["Name"] == "VTi"].iat[1] / weight
    entry["TiSet"] = settings["Value New"].loc[settings["Name"] == "Ti"].iat[0]
    temp = settings["Value New"].loc[(settings["Name"] == "Pmax") & (settings["Time [ms]"] <= lastminute)]
    if temp.shape[0] > 0:
        entry["PMaxSet"] = temp.iat[temp.shape[0] - 1]
    else:
        entry["PMaxSet"] = settings["Value New"].loc[settings["Name"] == "Pmax"].iat[0]
    entry["TiAvg"] = 0.4 if mode == "SIPPV-VG" else np.nanmean(slow_data["5001|Tispon [s]"])
    entry["VTDiff"] = np.nanmean(slow_data["5001|VTmand [mL]"] / weight - entry["VTSet"])
    entry["RRDiff"] = np.nanmean(slow_data["5001|RRmand [1/min]"] / weight - entry["RRSet"])
    
    
    
    entry[tcm.columns[2]] = np.nanmean(tcm.iloc[:,2].astype("float64"))
    entry[tcm.columns[3]] = np.nanmean(tcm.iloc[:,3].astype("float64"))
    entry[tcm.columns[5]] = np.nanmean(tcm.iloc[:,5].astype("float64"))
    
    for j in range(4, len(breaths.columns.values)):
        entry[breaths.columns.values[j]] = np.nanmean(breaths[breaths.columns.values[j]])
    return entry

# Process data
index = pd.read_csv(INDEX)
df = []
samplegroups = {}
breathcols = []
patient_info = pd.read_csv("/media/hdd/Clinical School/Year 4/SSC/evelynflowpaper/data/Evelyn_Flow_Study_Patient_Data.csv")

for sample in index["Sample_ID"].unique():
    groups = pd.read_csv(WORKING_DIRECTORY + "/" + sample + "/randomisation_list.csv")
    settings = pd.read_csv(WORKING_DIRECTORY + "/" + sample + "/" + 
                                   list(filter(lambda x : "slow_Setting" in x, os.listdir(WORKING_DIRECTORY + "/" + sample)))[0])
    raw_data = pd.read_csv(WORKING_DIRECTORY + "/" + sample + "/" + 
                                   list(filter(lambda x : "fast_Unknown" in x, os.listdir(WORKING_DIRECTORY + "/" + sample)))[0])
    slow_data = pd.read_csv(WORKING_DIRECTORY + "/" + sample + "/" + 
                                   list(filter(lambda x : "slow_Measurement" in x, os.listdir(WORKING_DIRECTORY + "/" + sample)))[0])
    physiology = pd.read_csv(WORKING_DIRECTORY + "/" + sample + "/FCTR_INFANT_NEONATAL_combined.csv", na_values="--")
    tcm = pd.read_csv(WORKING_DIRECTORY + "/" + sample + "/tcm_combined.csv", na_values="- ")
    breaths = pd.read_csv(WORKING_DIRECTORY + "/" + sample + "/predicted_breaths.csv")
    breaths = breaths.loc[breaths["Pressure_Flow_Correlation"] > 0]
    VTset = settings.loc[settings["Name"] == "VTi"].iloc[-1,8]
    group_index = 0
    subset = index.loc[index["Sample_ID"] == sample]
    physiologygroups = {}
    breathgroups = {}
    tcmgroups = {}
    for rowi in range(0,subset.shape[0]):
        row = subset.iloc[rowi,:]
        if group_index >= groups.shape[0]:
            break
        if groups.iloc[group_index,3] != row["Value"]:
            pass
        else:
            similarcount = 0
            i = group_index
            while groups.iloc[i,3] == groups.iloc[group_index,3]:
                similarcount += 1
                i += 1
                if i >= groups.shape[0]:
                    break
            if similarcount > 1:
                splits = list(range(row["Start"],row["End"],math.ceil((row["End"]-row["Start"])/similarcount)))
            else:
                splits = [row["Start"]]
            for i in range(0,len(splits)):
                if rowi == 0 and i == 0:
                    end = splits[i]
                    start = end - 450000
                elif rowi == subset.shape[0]-1 and i == len(splits)-1:
                    start = splits[i] + 450000
                    end = start + 450000
                elif i < len(splits)-1:
                    end = splits[i+1]
                    start = end - 450000
                else:
                    end = row["End"]
                    start = end - 450000
                    
                print(sample + " - " + str(group_index) + " - " + str((end-start)/1000) + " " + str(start) + " " + str(end))
                breathtimes = raw_data.iloc[breaths["Start"].values,0].values
                if groups.iloc[group_index,2] not in physiologygroups.keys():
                    physiologygroups[groups.iloc[group_index,2]] = physiology.loc[(physiology["Time [ms]"] >= start) & (physiology["Time [ms]"] <= end)]
                    breathgroups[groups.iloc[group_index,2]] = breaths.loc[(breathtimes >= start) & (breathtimes <= end)]
                    tcmgroups[groups.iloc[group_index,2]] = tcm.loc[(tcm["Time [ms]"] >= start) & (tcm["Time [ms]"] <= end)]
                    print(physiologygroups[groups.iloc[group_index,2]].shape)
                else:
                    physiologygroups[groups.iloc[group_index,2]] = pd.concat((physiologygroups[groups.iloc[group_index,2]], physiology.loc[(physiology["Time [ms]"] >= start) & (physiology["Time [ms]"] <= end)]),axis=0)
                    breathgroups[groups.iloc[group_index,2]] = pd.concat((breathgroups[groups.iloc[group_index,2]], breaths.loc[(breathtimes >= start) & (breathtimes <= end)]),axis=0)
                    tcmgroups[groups.iloc[group_index,2]] = pd.concat((tcmgroups[groups.iloc[group_index,2]], tcm.loc[(tcm["Time [ms]"] >= start) & (tcm["Time [ms]"] <= end)]), axis=0)
                    print(physiologygroups[groups.iloc[group_index,2]].shape)
                df.append(createEntry(sample, row, groups.iloc[group_index,2], start + 60000, end-60000,
                            physiology.loc[(physiology["Time [ms]"] >= start) & (physiology["Time [ms]"] <= end)],
                         breaths.loc[(breathtimes >= start) & (breathtimes <= end)],
                         tcm.loc[(tcm["Time [ms]"] >= start) & (tcm["Time [ms]"] <= end)],
                         raw_data.loc[(raw_data["Time [ms]"] > start) & (raw_data["Time [ms]"] < end)],
                         slow_data.loc[(slow_data["Time [ms]"] > start) & (slow_data["Time [ms]"] < end)], settings, patient_info["Weight during study (g)"].loc[patient_info["Recording"]==sample].iat[0]/1000 ))
                group_index += 1
df = pd.DataFrame(df, columns=list(df[0].keys()))
df.to_csv(OUTPUTFILE)
