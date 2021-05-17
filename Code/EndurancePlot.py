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
Endufiles.sort(key = lambda x: int(x.split("_")[2]))

Cycles = []
EFieldPeaks = []
QFEScaled = []
Prpos = []
LeakCurr = []

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
        Cycles.append(float(Efile.split("_")[2]))

        peak_ind, _ = find_peaks(np.abs(EnduVoltage), 0.1)
        numpeaks = len(peak_ind)
        peak_width = np.average(peak_ind[0:2])

        peak_range = [np.arange(peak_ind[j]-peak_width*0.49, peak_ind[j]+peak_width*0.49 + 1, dtype=int) for j in range(numpeaks)]

        EFieldPeaks.append(np.append([v/d for v in [EnduVoltage[j] for j in peak_range[1]]], [v/d for v in [EnduVoltage[j] for j in peak_range[2]]]))

        FECurrent = np.append([-EnduCurrent[j] for j in peak_range[1]], [-EnduCurrent[j] for j in peak_range[2]])

        QFE = [0] * len(FECurrent)
        for t in range(1, len(FECurrent)):
            dTime = EnduTime[t] - EnduTime[t-1]
            QFE[t] = FECurrent[t] * dTime + QFE[t-1]

        QFE = np.subtract(QFE, (np.max(QFE) + np.min(QFE))/2)
        QFEScaled.append(np.array([(k / (pi * r**2)) for k in QFE]))

        Prpos.append(round(QFEScaled[i][-1] * 10**2, 2))
        Prneg = round(QFEScaled[i][int(len(FECurrent)/2)] * 10**2, 2)
        
        ## Finding leakcurrent
        LeakRange = np.arange(peak_ind[1] - 10, peak_ind[1] + 10 + 1, dtype = int)
        LeakPeak, _ = find_peaks([EnduCurrent[j] for j in LeakRange], 0.1 * 10**-6)
        LeakCurr.extend([EnduCurrent[LeakRange[j]] for j in LeakPeak])

        if len(LeakCurr) < len(Cycles):
            LeakCurr.append(10 * 10**-6)

        """
        ## Plotting raw Endurance Data
        fig = plt.figure(figsize = (9,6))
        ax1 = fig.add_subplot(111)
        ax2 = ax1.twinx()

        ax1.plot([t * 10**3 for t in EnduTime], [i * 10**6 for i in EnduCurrent], label = "Current", color = "b")

        ax2.plot([t * 10**3 for t in EnduTime], EnduVoltage, label = "Voltage", color = "c")

        fig.legend(fontsize = 'x-large', loc = 4, bbox_to_anchor = (1,0), bbox_transform = ax1.transAxes)
        plt.title(Efile)

        ax1.tick_params('both', labelsize = "xx-large")
        ax2.tick_params('both', labelsize = "xx-large")

        ax1.set_xlabel("Time [ms]", fontsize = "xx-large")
        ax1.set_ylabel("Current [uA]", fontsize = "xx-large")
        ax2.set_ylabel("Voltage [V]", fontsize = "xx-large")
        """

        i += 1

SampleID = Efile.split("_")[4] + "_" + Efile.split("_")[5] + "_" + Efile.split("_")[7].replace('.csv','')

## Plotting PE-curves
fig = plt.figure(figsize = (9,6))
ax1 = fig.add_subplot(111)

for i in range(i - 1) :
    ax1.plot([e * 10**-8 for e in EFieldPeaks[i]], [p * 10**2 for p in QFEScaled[i]], label = '%s'%"{:.1e}".format(Cycles[i]))

fig.legend(title = "Cycles", fontsize = 'x-large', loc = 2, bbox_to_anchor = (0,1), bbox_transform = ax1.transAxes)

plt.ylim(np.min(QFEScaled[0:-1]) * 10**2, np.max(QFEScaled[0:-1]) * 10**2)

plt.title(SampleID)
ax1.tick_params('both', labelsize = "xx-large")

ax1.set_xlabel("Electric Field [MV/cm]", fontsize = "xx-large")
ax1.set_ylabel("Polarization [$\mu$C/cm²]", fontsize = "xx-large")

#plt.savefig('../Fig/InAs%s'%Efile.split("_")[4] + '/PEEndu_%s.png'%SampleID)

## Plotting Pr vs Cycle
fig = plt.figure(figsize = (9,6))
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()

ax1.semilogx(Cycles, Prpos, marker = 'o', label = 'Remnant Polarization')
ax1.set_ylim([0, max(Prpos[0:-2]) + 1])

ax2.semilogx(Cycles, [i * 10**6 for i in LeakCurr], linestyle = '--', marker = 'x', color = 'g', label = 'Leak Current')
ax2.set_ylim([0, (max(LeakCurr[0:-2]) + 10**-6) * 10**6])

fig.legend(fontsize = 'x-large', loc = 3, bbox_to_anchor = (0,0), bbox_transform = ax1.transAxes)

plt.title(SampleID)
ax1.tick_params('both', labelsize = "xx-large")
ax2.tick_params('both', labelsize = "xx-large")

ax1.set_xlabel("Cycles", fontsize = "xx-large")
ax1.set_ylabel("Remnant Polarization [$\mu$C/cm²]", fontsize = "xx-large")
ax2.set_ylabel("Leak Current [$\mu$A]", fontsize = "xx-large")

#plt.savefig('../Fig/InAs%s'%Efile.split("_")[4] + '/PrEndu_%s.png'%SampleID)

plt.show()



