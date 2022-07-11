#!/usr/bin/env python

import os
import numpy as np
from scipy.constants import pi
from scipy.constants import epsilon_0
import math
import matplotlib.pyplot as plt
import warnings

d = 10e-9 #Ferroelectric layer thickness (m)

### Take in an array with a path and 2 optional filters. Return a list of files sorted and filtered to specification.
def SortAndFilterDir(DataArray):
    path = DataArray[0]
    dataFilter = ['.csv', DataArray[1] if len(DataArray) > 1 else '', DataArray[2] if len(DataArray) > 2 else '']
    files = [fn for fn in os.listdir(path) if all(fn.find(df) != -1 for df in dataFilter)]
    files.sort()

    if len(files) < 1:
        print("Didn't find any matching data for '%s' with specified filter: %s."%(path, dataFilter))
    elif len(files) > 10:
        print("Found too many matching data for '%s' with specified filter: %s.\nExiting..."%(path, dataFilter))
        exit(1)

    return path, files

### Takes a directory and a list of CV files and outputs all relevant data.
def GetCVData(CVPath, CVFiles): 
    CVVoltage = []
    freq = []
    C_HZO = []
    epsilon_r = []

    i = 0
    for Cfile in CVFiles:
        CVFile = open(os.path.join(CVPath, Cfile), 'r')
        CVFilelines = CVFile.readlines()

        CVVoltage.append([float(line.split(",")[2]) for line in CVFilelines])
        CVX = [float(line.split(",")[1]) * -1 for line in CVFilelines]

        CVFile.close()

        r = float(Cfile.split("_")[5].replace('um','')) * 10**-6
        A = pi * r**2
        freq.append(float(Cfile.split("_")[7].replace('Hz','')))

        C_HZO.append(np.array([1 / (2 * pi * freq[i] * X * A) for X in CVX]))
        epsilon_r.append(np.array([(d / epsilon_0) * c for c in C_HZO[i]]))

        i += 1

    warnings.filterwarnings("ignore", message = "invalid value encountered in double_scalars")
    warnings.filterwarnings("ignore", message = "divide by zero encountered in double_scalars")
    
    Cdisp = [(((C_HZO[0::2][-1][-1] - C_HZO[0::2][j][-1])/C_HZO[0::2][-1][-1]) * 10**2)/math.log10(freq[0::2][j]/freq[-1]) for j in range(int(i/2))]
    Wdep = [((1 / C_HZO[1::2][j][-1]) - (1 / C_HZO[1::2][j][0])) * (15.15 * epsilon_0) for j in range(int(i/2))]

    return CVVoltage, freq, C_HZO, epsilon_r, Cdisp, Wdep
            
### Takes array of arrays with directory and 2 optional filters and plots CV curves for all files in directory matching the filter. 
def PlotCV(dataArray, saveFig = ''):
    for data in dataArray:
        CVPath, CVFiles = SortAndFilterDir(data)

        if len(CVFiles) < 1:
            print("Skipping...")
            continue

        CVVoltage, freq, C_HZO, epsilon_r, _, Wdep = GetCVData(CVPath, CVFiles)

        SampleID = CVFiles[0].split("_")[2] + "_" + CVFiles[0].split("_")[3] + "_" + CVFiles[0].split("_")[4] + "_" + CVFiles[0].split("_")[1]

        fig = plt.figure(figsize = (10,6))
        ax1 = fig.add_subplot(111)
        ax2 = ax1.twinx()

        cmap = plt.get_cmap('Set1')
        colors = iter(cmap(np.linspace(0,1,len(CVFiles))))

        for i in range(len(CVFiles)):
            if i % 2 == 0:
                color = next(colors)
                ax1.plot(CVVoltage[i], [c * 10**2 for c in C_HZO[i]], label = '%s MHz\t$W_{dep}$ = %s nm'%(int(freq[i] * 10**-6), round(Wdep[int(i/2)] * 10**9, 1)) if freq[i] % 1000000 == 0 else '%s kHz\t$W_{dep}$ = %s nm'%(int(freq[i] * 10**-3), round(Wdep[int(i/2)] * 10**9, 1)), color = color)

                ax2.plot(CVVoltage[i], epsilon_r[i], color = "r", alpha = 0)
            else:
                ax1.plot(CVVoltage[i], [c * 10**2 for c in C_HZO[i]], linestyle = '--', dash_capstyle = 'round', color = color)

                ax2.plot(CVVoltage[i], epsilon_r[i], color = "r", alpha = 0)

        ax2.annotate("", (-0.1, np.min(epsilon_r)), (-1, np.min(epsilon_r)), arrowprops = dict(arrowstyle = "->", linewidth = 1.5))
        ax2.annotate("", (0.1, np.min(epsilon_r)), (1, np.min(epsilon_r)), arrowprops = dict(arrowstyle = "->", linestyle = '--', linewidth = 1.5))

        fig.legend(fontsize = 'large', loc = 2, bbox_to_anchor = (0,1), bbox_transform = ax1.transAxes)

        plt.title(SampleID)

        ax1.tick_params('both', labelsize = "x-large")
        ax2.tick_params('both', labelsize = "x-large")

        ax1.set_xlabel("Voltage [V]", fontsize = "xx-large")
        ax1.set_ylabel("Capacitance [$\mu$F/cm²]", fontsize = "xx-large")
        ax2.set_ylabel("Dielectric Constant $\epsilon_r$", fontsize = "xx-large")
        
        if saveFig != '':
            figName = '%s_%sV'%(SampleID, str(round(np.max(CVVoltage), 1)))
            plt.savefig(saveFig + 'CV_%s.png'%figName)

### Takes array of arrays with directory and 2 optional filters and plots frequency dispersion for all files matching the filter.
def PlotFreqDisp(dataArray, saveFig = ''):
    fig = plt.figure(figsize = (10,8))
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212, sharex = ax1)
    
    collectedCdisp = []
    avgCdisp = []
    stdCdisp = []
    
    for data in dataArray:
        CVPath, CVFiles = SortAndFilterDir(data)

        if len(CVFiles) < 1:
            print("Skipping...")
            continue

        SampleID = CVFiles[0].split("_")[2] + "_" + CVFiles[0].split("_")[3] + "_" + CVFiles[0].split("_")[4] + "_" + CVFiles[0].split("_")[1]
        V_max = CVFiles[0].split("_")[6]

        _, freq, _, _, Cdisp, _ = GetCVData(CVPath, CVFiles)
        collectedCdisp.append(Cdisp)

        ax1.semilogx(freq[0::2], Cdisp, marker = 'o', markersize = 15, ls = ':', label = SampleID)

    collectedCdisp = np.array(collectedCdisp).transpose()
    for i in range(len(collectedCdisp)):
        avgCdisp.append(np.average(collectedCdisp[i]))
        stdCdisp.append(np.std(collectedCdisp[i]))

    ax2.errorbar(freq[0::2], avgCdisp, yerr = stdCdisp, marker = 'o', markersize = 15, ls = ':', capsize = 10, label = 'Average $\pm$ Standard Deviation')

    ax1.tick_params('both', labelsize = "x-large")
    ax2.tick_params('both', labelsize = "x-large")
    ax2.set_xlabel("Frequency [Hz]", fontsize = "xx-large")
    fig.supylabel('Frequency Dispersion @ +%s'%V_max + ' [%/dec]', fontsize = "xx-large")

    ax1.legend(fontsize = 10, loc = 1, bbox_to_anchor = (1,1), bbox_transform = ax1.transAxes)
    ax2.legend(fontsize = 10, loc = 1, bbox_to_anchor = (1,1), bbox_transform = ax2.transAxes)

    if saveFig != '':
        figName = "%s_%s_%s_%s"%(CVFiles[0].split("_")[2], CVFiles[0].split("_")[3], CVFiles[0].split("_")[1], str(V_max))
        plt.savefig(saveFig + 'FreqDisp_%s.png'%figName) 

    return freq, avgCdisp, stdCdisp, SampleID, V_max

###
def PlotFreqDispGroup(dataArray, saveFig = ''):
    fig = plt.figure(figsize = (10,6))
    ax1 = fig.add_subplot(111)

    for i in range(len(dataArray)):
        freq, avgCdisp, stdCdisp, SampleID, V_max = PlotFreqDisp(dataArray[i], saveFig)

        ax1.errorbar(freq[0::2], avgCdisp, yerr = stdCdisp, marker = 'o', markersize = 15, ls = ':', capsize = 10, label = "%s_%s_%s"%(SampleID.split("_")[0], SampleID.split("_")[1], SampleID.split("_")[3]))

    ax1.set_xscale('log')
    ax1.legend(fontsize = 10, loc = 1, bbox_to_anchor = (1,1), bbox_transform = ax1.transAxes)

    ax1.tick_params('both', labelsize = "x-large")
    ax1.set_xlabel("Frequency [Hz]", fontsize = "xx-large")
    ax1.set_ylabel('Frequency Dispersion @ +%s'%V_max + ' [%/dec]', fontsize = "xx-large")
