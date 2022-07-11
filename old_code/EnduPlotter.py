#!/usr/bin/python

import sys
import os
import numpy as np
from scipy.signal import find_peaks
from scipy.constants import pi
import matplotlib.pyplot as plt

d = 10**-9 # FE oxide layer thickness (m)

def SortAndFilterDir(dataArray):
    path = dataArray[0]
    dataFilter = ['.csv', dataArray[1] if len(dataArray) > 1 else '']
    files = [fn for fn in os.listdir(path) if all(fn.find(df) != -1 for df in dataFilter)]
    files.sort(key = lambda x: int(x.split("_")[3]))

    if len(files) < 1:
        print("Didn't find any matching data for '%s' with specified filter: %s"%(path, dataFilter))

    return path, files

def GetEnduData(Endupath, Endufiles):
    Cycles = []
    EFieldPeaks = []
    QFEScaled = []
    Pr = []
    LeakCurr = []
    
    i = 0
    for Efile in Endufiles:
        EnduFile = open(os.path.join(Endupath, Efile), 'r')
        EnduFilelines = EnduFile.readlines()

        if Efile.split("_")[0] == 'EnduranceP':
            EnduTime = [float(line.split(",")[2]) for line in EnduFilelines]
            EnduCurrent = [float(line.split(",")[0]) for line in EnduFilelines]
            EnduVoltage = [float(line.split(",")[1]) for line in EnduFilelines]
        else:
            EnduTime = [float(line.split(",")[1]) for line in EnduFilelines]
            EnduCurrent = [float(line.split(",")[2]) for line in EnduFilelines]
            EnduVoltage = [float(line.split(",")[3]) for line in EnduFilelines]
        
        EnduFile.close()

        maxV = Efile.split("_")[1]
        r = float(Efile.split("_")[7].replace('um','')) * 10**-6
        Cycles.append(float(Efile.split("_")[3]))

        peak_ind, _ = find_peaks(np.abs(EnduVoltage), 0.1)
        numpeaks = len(peak_ind)
        peak_width = np.average(peak_ind[0:2])

        peak_range = [np.arange(peak_ind[j]-peak_width*0.49, peak_ind[j]+peak_width*0.49 + 1, dtype=int) for j in range(numpeaks)]

        if Efile.split("_")[0] == 'EnduranceP':
            EFieldPeaks.append(np.append([v/d for v in [EnduVoltage[j] for j in peak_range[1]]], [v/d for v in [EnduVoltage[j] for j in peak_range[3]]]))
            
            FECurrentDown = np.subtract([-EnduCurrent[j] for j in peak_range[1]], [-EnduCurrent[j] for j in peak_range[2]])
            FECurrentUp = np.subtract([-EnduCurrent[j] for j in peak_range[3]], [-EnduCurrent[j] for j in peak_range[4]])
            FECurrent = np.append(FECurrentDown, FECurrentUp)

        else:
            EFieldPeaks.append(np.append([v/d for v in [EnduVoltage[j] for j in peak_range[1]]], [v/d for v in [EnduVoltage[j] for j in peak_range[2]]]))

            FECurrent = np.append([-EnduCurrent[j] for j in peak_range[1]], [-EnduCurrent[j] for j in peak_range[2]])

        QFE = [0] * len(FECurrent)
        for t in range(1, len(FECurrent)):
            dTime = EnduTime[t] - EnduTime[t-1]
            QFE[t] = FECurrent[t] * dTime + QFE[t-1]

        QFE = np.subtract(QFE, (np.max(QFE) + np.min(QFE))/2)
        QFEScaled.append(np.array([(k / (pi * r**2)) for k in QFE]))

        Prpos = min(round(QFEScaled[i][0] * 10**2, 2), round(QFEScaled[i][-1] * 10**2, 2)) # Pr pos!
        Prneg = round(QFEScaled[i][int(len(FECurrent)/2)] * 10**2, 2)
        Pr.append(np.abs(Prpos))
        
        ## Finding leakcurrent
        #LeakRangeDown = np.arange(peak_ind[1] - 10, peak_ind[1] + 10 + 1, dtype = int)
        #LeakRangeUp = np.arange(peak_ind[2] - 10, peak_ind[2] + 10 + 1, dtype = int)
        #LeakPeakDown, _ = find_peaks([np.abs(EnduCurrent[j]) for j in LeakRangeDown], 0.1 * 10**-6)
        #LeakPeakUp, _ = find_peaks([np.abs(EnduCurrent[j]) for j in LeakRangeDown], 0.1 * 10**-6)
        LeakCurrDown = np.abs(EnduCurrent[peak_ind[1] - 1])
        LeakCurrUp = np.abs(EnduCurrent[peak_ind[2] - 1])
        LeakCurr.append(max(LeakCurrDown, LeakCurrUp))

        if len(LeakCurr) < len(Cycles):
            LeakCurr.append(10 * 10**-6)

        i += 1

    return Cycles, EFieldPeaks, QFEScaled, Pr, LeakCurr

def PlotEndu(dataArray, label, saveFig = ''):
    fig = plt.figure(figsize = (6,5))
    ax1 = fig.add_subplot(111)
    #ax2 = ax1.twinx()

    cmap = plt.get_cmap('Set2')
    colors = iter(cmap(np.linspace(0,1,len(dataArray))))

    j = 0
    for group in dataArray:
        i = 0
        color = next(colors)

        for data in group:
            EnduPath, EnduFiles = SortAndFilterDir(data)
           
            if len(EnduFiles) < 1:
                continue

            Cycles, _, _, Pr, LeakCurr = GetEnduData(EnduPath, EnduFiles)

            if i < 1:
                ax1.semilogx(Cycles, Pr, marker = 'o', ms = 20, mec = 'black', ls = '--', lw = 4, color = color, label = label[j])
                #ax2.semilogx(Cycles, [i * 10**6 for i in LeakCurr], linestyle = '--', marker = 'x', color = 'g', label = 'Leak Current')
                i += 1
            else:
                ax1.semilogx(Cycles, Pr, marker = 'o', color = color, alpha = 0.2)

        j += 1

    fig.legend(fontsize = 'x-large', loc = 3, bbox_to_anchor = (0,0), bbox_transform = ax1.transAxes)

    ax1.set_ylim([-1, 32])

    #plt.title(SampleID)
    ax1.tick_params('both', labelsize = "x-large")
    #ax2.tick_params('both', labelsize = "xx-large")

    ax1.set_xlabel("Cycles", fontsize = "xx-large")
    ax1.set_ylabel("Remnant Polarization [$\mu$C/cm²]", fontsize = "xx-large")
    #ax2.set_ylabel("Leak Current [$\mu$A]", fontsize = "xx-large")


