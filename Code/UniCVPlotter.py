#/usr/bin/env python

import os
import numpy as np
from scipy.constants import pi
from scipy.constants import epsilon_0
from scipy.constants import e
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

d = 10**-9 #Ferroelectric layer thickness (m)
f = 10**6 #CV Frequency (Hz)

def SortAndFilterDir(dataArray):
    path = dataArray[0]
    dataFilter = ['.csv', dataArray[1] if len(dataArray) > 1 else '']
    files = [fn for fn in os.listdir(path) if all(fn.find(df) != -1 for df in dataFilter)]
    files.sort()

    if len(files) < 1:
        print("Didn't find any matching data for '%s' with specified filter: %s."%(path, dataFilter))

    return path, files

def GetUniData(UniPath, UniFiles):
    UniVoltage = []
    C_HZO = []
    epsilon_r = []
    Qt = []
    V_max = []
    V_ref = -1
    
    i = 0
    for Ufile in UniFiles:
        UniFile = open(os.path.join(UniPath, Ufile), 'r')
        UniFilelines = UniFile.readlines()

        UniVoltage.append([float(line.split(",")[2]) for line in UniFilelines])
        UniX = [float(line.split(",")[1]) * -1 for line in UniFilelines]

        UniFile.close()

        r = float(Ufile.split("_")[5].replace('um','')) * 10**-6
        A = pi * r**2

        C_HZO.append(np.array([1 / (2 * pi * f * X * A) for X in UniX]))
        epsilon_r.append(np.array([(d / epsilon_0) * c for c in C_HZO[i]]))

        if Ufile.split("_")[6] == '1.csv':
            PsetMax = np.max(C_HZO[i])

        if Ufile.split("_")[6] == '2+3.csv':
            RefMin = np.min(C_HZO[i])
            C_avg = (PsetMax + RefMin) / 2
            C_ox = C_HZO[i][0]
        
        if Ufile.split("_")[6] == '4':
            V_ref_ind = np.where((C_HZO[i] > C_avg - 8*10**-4) & (C_HZO[i] < C_avg + 8*10**-4))
            V_ref = UniVoltage[i][np.take(V_ref_ind, len(V_ref_ind) / 2)]

        if Ufile.split("_")[6] == '5':
            V_ind = np.where((C_HZO[i] > C_avg - 8*10**-4) & (C_HZO[i] < C_avg + 8*10**-4))
            deltaV = np.abs(V_ref - UniVoltage[i][np.take(V_ind, len(V_ind) / 2)])
            Qt.append((deltaV * C_ox) / e)
            V_max.append(Ufile.split("_")[7].replace('V.csv',''))

        i += 1
    
    return UniVoltage, C_HZO, epsilon_r, C_avg, V_max, Qt, V_ref, deltaV

def PlotUniCV(dataArray, saveFig = ''):
    collectedQt = []
    avgQt = []
    stdQt = []

    for data in dataArray:
        UniPath, UniFiles = SortAndFilterDir(data)

        if len(UniFiles) < 1:
            print("Skipping...")
            continue

        SampleID = UniFiles[0].split("_")[0] + "_" + UniFiles[0].split("_")[2] + "_" + UniFiles[0].split("_")[3] + "_" + UniFiles[0].split("_")[4] + "_" + UniFiles[0].split("_")[1]

        UniVoltage, C_HZO, epsilon_r, C_avg, V_max, Qt, V_ref, deltaV = GetUniData(UniPath, UniFiles)
        collectedQt.append(Qt)

        fig = plt.figure(figsize = (10,6))
        ax1 = fig.add_subplot(111)
        ax2 = ax1.twinx()

        plt.title(SampleID)

        for i in range(len(UniFiles)):
            if UniFiles[i].split("_")[6] == '1.csv':
                ax1.plot(UniVoltage[i], [c * 10**2 for c in C_HZO[i]], label = 'P-set', ls = ':', alpha = 0.8)
                ax2.plot(UniVoltage[i], epsilon_r[i], alpha = 0)
            if UniFiles[i].split("_")[6] == '2+3.csv':
                ax1.plot(UniVoltage[i], [c * 10**2 for c in C_HZO[i]], label = 'Reference', lw = 3)
                ax2.plot(UniVoltage[i], epsilon_r[i], alpha = 0)
            if UniFiles[i].split("_")[6] == '4':
                ax1.plot(UniVoltage[i], [c * 10**2 for c in C_HZO[i]], ls = '-.', alpha = 0.3)
                ax2.plot(UniVoltage[i], epsilon_r[i], alpha = 0)
            if UniFiles[i].split("_")[6] == '5':
                ax1.plot(UniVoltage[i], [c * 10**2 for c in C_HZO[i]], label = '$V_{max}$ = %s'%UniFiles[i].split("_")[7].replace('.csv',''), alpha = 0.9)
                ax2.plot(UniVoltage[i], epsilon_r[i], alpha = 0)

        inax = inset_axes(ax2, width='30%', height='40%', loc=4, borderpad=3.8)
        inax.plot(V_max, [q * 10**-4 for q in Qt], ls='--', marker='o') #Convertion from m2 to cm2

        inax.set_xlabel("$V_{max}$ [V]", fontsize = "x-large")
        inax.set_ylabel("Defect Density [$cm^{-2}$]", fontsize = "x-large")

        ax1.hlines(C_avg * 10**2, V_ref - 0.1, V_ref + deltaV + 0.1, ls = '--')
            
        fig.legend(fontsize = 'large', loc = 2, bbox_to_anchor = (0,1), bbox_transform = ax1.transAxes)
        
        ax1.tick_params('both', labelsize = "x-large")
        ax2.tick_params('both', labelsize = "x-large")
        inax.tick_params('both', labelsize = "large")

        ax1.set_xlabel("Voltage [V]", fontsize = "xx-large")
        ax1.set_ylabel("Capacitance [$\mu$F/cm²]", fontsize = "xx-large")
        ax2.set_ylabel("Dielectric Constant $\epsilon_r$", fontsize = "xx-large")

        if saveFig != '':
            figName = SampleID
            plt.savefig(saveFig + '%s.png'%figName)

    collectedQt = np.array(collectedQt).transpose() * 10**-4
    for i in range(len(collectedQt)):
        avgQt.append(np.average(collectedQt[i]))
        stdQt.append(np.std(collectedQt[i]))

    return V_max, avgQt, stdQt, SampleID

def PlotDDGroup(dataArray, saveFig = '', labelArray = []):
    fig = plt.figure(figsize = (6,5))
    ax1 = fig.add_subplot(111)

    for i in range(len(dataArray)):
        V_max, avgQt, stdQt, SampleID = PlotUniCV(dataArray[i], saveFig)

        if labelArray[i] == '':
            labelArray[i] = "%s_%s_%s"%(SampleID.split("_")[1], SampleID.split("_")[2], SampleID.split("_")[4])

        ax1.errorbar(V_max, avgQt, yerr = stdQt, marker = 'o', markersize = 20, mec = 'black', ls = ':', capsize = 10, label = labelArray[i]) 

    ax1.legend(fontsize = 'x-large', loc = 2, bbox_to_anchor = (0,1), bbox_transform = ax1.transAxes)
    
    ax1.set_xlabel("$V_{max}$ [V]", fontsize = "xx-large")
    ax1.set_ylabel("Defect Density [$cm^{-2}$]", fontsize = "xx-large")

    ax1.tick_params('both', labelsize = "x-large")

    
