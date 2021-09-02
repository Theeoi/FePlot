#/usr/bin/env python

import os
import numpy as np
from scipy.constants import pi
from scipy.constants import epsilon_0
from scipy.constants import e
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

d = 10e-9 #Ferroelectric layer thickness (m)

def SortAndFilterDir(dataArray):
    path = dataArray[0]
    dataFilter = ['.csv']
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
    
    i = 0
    for Ufile in UniFiles:
        UniFile = open(os.path.join(UniPath, Ufile), 'r')
        UniFilelines = UniFile.readlines()

        UniVoltage.append([float(line.split(",")[2]) for line in UniFilelines])
        UniX = [float(line.split(",")[1]) * -1 for line in UniFilelines]

        UniFile.close()

        r = float(Ufile.split("_")[5].replace('um','')) * 10**-6
        A = pi * r**2

        C_HZO.append(np.array([1 / (2 * pi * 10**6 * X * A) for X in UniX]))
        epsilon_r.append(np.array([(d / epsilon_0) * c for c in C_HZO[i]]))

        if Ufile.split("_")[6] == '1.csv':
            PsetMax = np.max(C_HZO[i])

        if Ufile.split("_")[6] == '2+3.csv':
            RefMin = np.min(C_HZO[i])
            C_avg = (PsetMax + RefMin) / 2
            V_ref_ind = np.where((C_HZO[i] > C_avg - 8*10**-4) & (C_HZO[i] < C_avg + 8*10**-4))
            V_ref = UniVoltage[i][np.take(V_ref_ind, len(V_ref_ind) / 2)]
            C_ox = C_HZO[i][0]

        if Ufile.split("_")[6] == '5':
            V_ind = np.where((C_HZO[i] > C_avg - 8*10**-4) & (C_HZO[i] < C_avg + 8*10**-4))
            deltaV = np.abs(V_ref - UniVoltage[i][np.take(V_ind, len(V_ind) / 2)])
            Qt.append((deltaV * C_ox) / e)
            V_max.append(Ufile.split("_")[7].replace('V.csv',''))

        i += 1
    
    return UniVoltage, C_HZO, epsilon_r, C_avg, V_max, Qt, V_ref, deltaV

def PlotUniCV(dataArray, saveFig = ''):
    for data in dataArray:
        UniPath, UniFiles = SortAndFilterDir(data)

        if len(UniFiles) < 1:
            print("Skipping...")
            continue

        UniVoltage, C_HZO, epsilon_r, C_avg, V_max, Qt, V_ref, deltaV = GetUniData(UniPath, UniFiles)

        fig = plt.figure(figsize = (10,6))
        ax1 = fig.add_subplot(111)
        ax2 = ax1.twinx()

        for i in range(len(UniFiles)):
            if UniFiles[i].split("_")[6] == '1.csv':
                ax1.plot(UniVoltage[i], [c * 10**2 for c in C_HZO[i]], label = 'P-set', ls = ':', alpha = 0.8)
                ax2.plot(UniVoltage[i], epsilon_r[i], alpha = 0)
            if UniFiles[i].split("_")[6] == '2+3.csv':
                ax1.plot(UniVoltage[i], [c * 10**2 for c in C_HZO[i]], label = 'Reference', lw = 3)
                ax2.plot(UniVoltage[i], epsilon_r[i], alpha = 0)
            if UniFiles[i].split("_")[6] == '5':
                ax1.plot(UniVoltage[i], [c * 10**2 for c in C_HZO[i]], label = '$V_{max}$ = %s'%UniFiles[i].split("_")[7].replace('.csv',''), alpha = 0.9)
                ax2.plot(UniVoltage[i], epsilon_r[i], alpha = 0)

        inax = inset_axes(ax2, width='30%', height='40%', loc=4, borderpad=3.8)
        inax.plot(V_max, Qt, ls='--', marker='o')

        inax.set_xlabel("$V_{max}$ [V]", fontsize = "x-large")
        inax.set_ylabel("Defect Density [$cm^{-2}$]", fontsize = "x-large")

        ax1.hlines(C_avg * 10**2, V_ref - 0.2, V_ref + deltaV, ls = '--')
            
        fig.legend(fontsize = 'large', loc = 2, bbox_to_anchor = (0,1), bbox_transform = ax1.transAxes)
        
        ax1.tick_params('both', labelsize = "x-large")
        ax2.tick_params('both', labelsize = "x-large")
        inax.tick_params('both', labelsize = "large")

        ax1.set_xlabel("Voltage [V]", fontsize = "xx-large")
        ax1.set_ylabel("Capacitance [$\mu$F/cm²]", fontsize = "xx-large")
        ax2.set_ylabel("Dielectric Constant $\epsilon_r$", fontsize = "xx-large")
