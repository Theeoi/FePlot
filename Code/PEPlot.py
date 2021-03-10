#!/usr/bin/python

### USAGE ###
# ./PUNDPlot.py <Path to clean PUND data>
# Example: ./PUNDPlot.py ../Data/InAsFlashIntA/PUND

import sys
import os
import numpy as np
from scipy.signal import find_peaks
from scipy.constants import pi
import matplotlib.pyplot as plt

## Read data

PUNDpath = sys.argv[1]
PUNDfiles = os.listdir(PUNDpath)
PUNDfiles.sort()
numfiles = len(PUNDfiles)

PUNDTime = [0] * numfiles
PUNDCurrent = [0] * numfiles
PUNDVoltage = [0] * numfiles

r = 25e-6 ## Condensator radius (Will implement automatically later)
d = 10e-9 ## Ferroelectric layer thickness (m)

i = 0
for Pfile in PUNDfiles:
    if Pfile.endswith('.csv'):
        PUNDfile = open(os.path.join(PUNDpath, Pfile), 'r')
        PUNDfilelines = PUNDfile.readlines()

        PUNDTime[i] = [float(line.split(",")[1]) for line in PUNDfilelines]
        PUNDCurrent[i] = [float(line.split(",")[2]) for line in PUNDfilelines]
        PUNDVoltage[i] = [float(line.split(",")[3]) for line in PUNDfilelines]

        PUNDfile.close()
        
        peak_ind, _ = find_peaks(np.abs(PUNDVoltage[i]), 0.1)
        numpeaks = len(peak_ind)
        peak_width = np.average(peak_ind[0:2])
        
        peak_range = [np.arange(peak_ind[j]-peak_width*0.49, peak_ind[j]+peak_width*0.49 + 1, dtype=int) for j in range(numpeaks)]
        
        FECurrentDown = np.subtract([PUNDCurrent[i][j] for j in peak_range[1]], [PUNDCurrent[i][j] for j in peak_range[2]])
        FECurrentUp = np.subtract([PUNDCurrent[i][j] for j in peak_range[3]], [PUNDCurrent[i][j] for j in peak_range[4]])

        QFEDown = [0] * len(FECurrentDown)
        QFEUp = [0] * len(FECurrentUp)
        for t in range(1, len(FECurrentDown)):
            dTime = PUNDTime[i][t] - PUNDTime[i][t-1]
            QFEDown[t] = FECurrentDown[t] * dTime + QFEDown[t-1]
            QFEUp[t] = FECurrentUp[t] * dTime + QFEUp[t-1]

        QFEDown = np.subtract(QFEDown, (np.max(QFEDown) + np.min(QFEDown))/2)
        QFEUp = np.subtract(QFEUp, (np.max(QFEUp) + np.min(QFEUp))/2)

        QFEDownScaled = [(k / (pi * r**2)) for k in QFEDown]
        QFEUpScaled = [(k / (pi * r**2)) for k in QFEUp]

        Pr = round(QFEDownScaled[-1] * 10**2, 2)

        ### Plotting PUND Measurements
        fig = plt.figure(figsize = (9,6))
        ax1 = fig.add_subplot(111)
        ax2 = ax1.twinx()

        ax1.plot([t * 10**3 for t in PUNDTime[i]], [c * 10**6 for c in PUNDCurrent[i]], label = "Current", color = "b")

        ax2.plot([t * 10**3 for t in PUNDTime[i]], PUNDVoltage[i], label = "Voltage", color = "c")

        plt.title(Pfile)
        fig.legend(fontsize = 'x-large', loc = 4, bbox_to_anchor = (1,0), bbox_transform = ax1.transAxes)

        ax1.tick_params('both', labelsize = "x-large")
        ax2.tick_params('both', labelsize = "x-large")

        ax1.set_xlabel("Time [ms]", fontsize = "xx-large")
        ax1.set_ylabel("Current [$\mu$A]", fontsize = "xx-large")
        ax2.set_ylabel("Voltage [V]", fontsize = "xx-large")

        plt.savefig('../Fig/InAsFlashIntA/%s.png'%Pfile)

        ### Plotting I-E
        fig = plt.figure(figsize = (9,6))
        ax1 = fig.add_subplot(111)

        ax1.plot([(v * 10**-8)/d for v in [PUNDVoltage[i][j] for j in peak_range[1]]], [c * 10**6 for c in FECurrentDown], label = "Down Current", color = "b")
        ax1.plot([(v * 10**-8)/d for v in [PUNDVoltage[i][j] for j in peak_range[3]]], [c * 10**6 for c in FECurrentUp], label = "Up Current", color = "r")

        plt.title(Pfile)
        fig.legend(fontsize = 'x-large', loc = 1, bbox_to_anchor = (1,1), bbox_transform = ax1.transAxes)

        ax1.tick_params('both', labelsize = "x-large")

        ax1.set_xlabel("Electric Field [MV/cm]", fontsize = "xx-large")
        ax1.set_ylabel("FE Current [$\mu$A]", fontsize = "xx-large")

        plt.savefig('../Fig/InAsFlashIntA/IE_%s.png'%Pfile)

        ### Plotting P-E
        fig = plt.figure(figsize = (9,6))
        ax1 = fig.add_subplot(111)

        ax1.plot([(v * 10**-8)/d for v in [PUNDVoltage[i][j] for j in peak_range[1]]], [p * 10**2 for p in QFEDownScaled], color = "b")
        ax1.plot([(v * 10**-8)/d for v in [PUNDVoltage[i][j] for j in peak_range[3]]], [p * 10**2 for p in QFEUpScaled], color = "b")

        plt.title(Pfile)
        fig.text(0.68, 0.83, '$P_r$ = %s $\mu$C/cm²'%Pr, fontsize = "x-large")

        ax1.tick_params('both', labelsize = "x-large")

        ax1.set_xlabel("Electric Field [MV/cm]", fontsize = "xx-large")
        ax1.set_ylabel("Polarization [$\mu$C/cm²]", fontsize = "xx-large")

        plt.savefig('../Fig/InAsFlashIntA/PE_%s.png'%Pfile)

        i += 1

plt.show()


