#!/usr/bin/python

### USAGE ###
# ./EndurancePlot.py <Path to clean Endurace data>
# Example ./EndurancePlot.py ../Data/InAsFlashIntA/Endu

import sys
import os
import numpy as np
from scipy.signal import find_peaks
from scipy.constants import pi
import matplotlib.pyplot as plt

## Read data

EnduPath = sys.argv[1]
Endufiles = os.listdir(EnduPath)
Endufiles.sort()
numfiles = len(Endufiles)

EFieldPeaks = [0] * numfiles
QFEScaled = [0] * numfiles
Prpos = [0] * numfiles

d = 10e-9 ## Ferroelectric layer thickness (m)

i=0
for Efile in Endufiles:
    if Efile.endswith('.csv'):
        EnduFile = open(os.path.join(EnduPath, Efile), 'r')
        EnduFilelines = EnduFile.readlines()

        EnduTime = [float(line.split(",")[1]) for line in EnduFilelines]
        EnduCurrent = [float(line.split(",")[2]) for line in EnduFilelines]
        EnduVoltage = [float(line.split(",")[3]) for line in EnduFilelines]

        EnduFile.close()

        r = float(Efile.split("_")[6].replace('um','')) * 10**-6

        peak_ind, _ = find_peaks(np.abs(EnduVoltage), 0.1)
        numpeaks = len(peak_ind)
        peak_width = np.average(peak_ind[0:2])

        peak_range = [np.arange(peak_ind[j]-peak_width*0.49, peak_ind[j]+peak_width*0.49 + 1, dtype=int) for j in range(numpeaks)]

        EFieldPeaks[i] = np.append([v/d for v in [EnduVoltage[j] for j in peak_range[1]]], [v/d for v in [EnduVoltage[j] for j in peak_range[2]]])

        FECurrent = np.append([EnduCurrent[j] for j in peak_range[2]], [EnduCurrent[j] for j in peak_range[1]])

        QFE = [0] * len(FECurrent)
        for t in range(1, len(FECurrent)):
            dTime = EnduTime[t] - EnduTime[t-1]
            QFE[t] = FECurrent[t] * dTime + QFE[t-1]

        QFE = np.subtract(QFE, (np.max(QFE) + np.min(QFE))/2)
        QFEScaled[i] = np.array([(k / (pi * r**2)) for k in QFE])

        Prpos[i] = round(QFEScaled[i][0] * 10**2, 2)
        Prneg = round(QFEScaled[i][int(len(FECurrent)/2)] * 10**2, 2)

        fig = plt.figure(figsize = (9,6))
        ax1 = fig.add_subplot(111)
        ax2 = ax1.twinx()

        ax1.plot([t * 10**3 for t in EnduTime], [i * 10**6 for i in EnduCurrent], label = "Current", color = "b")

        ax2.plot([t * 10**3 for t in EnduTime], EnduVoltage, label = "Voltage", color = "c")

        fig.legend(fontsize = 'x-large', loc = 4, bbox_to_anchor = (1,0), bbox_transform = ax1.transAxes)

        ax1.tick_params('both', labelsize = "x-large")
        ax2.tick_params('both', labelsize = "x-large")

        ax1.set_xlabel("Time [ms]", fontsize = "xx-large")
        ax1.set_ylabel("Current [uA]", fontsize = "xx-large")
        ax2.set_ylabel("Voltage [V]", fontsize = "xx-large")

        i += 1

print(Prpos)

fig = plt.figure(figsize = (9,6))
ax1 = fig.add_subplot(111)

for i in range(numfiles):
    ax1.plot([e * 10**-8 for e in EFieldPeaks[i]], [p * 10**2 for p in QFEScaled[i]])

ax1.tick_params('both', labelsize = "x-large")

ax1.set_xlabel("Electric Field [MV/cm]", fontsize = "xx-large")
ax1.set_ylabel("Polarization [$\mu$C/cm²]", fontsize = "xx-large")

#plt.savefig('../Fig/PLE_Y.png')
plt.show()



