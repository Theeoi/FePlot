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

        r = float(Pfile.split("_")[4].replace('um','')) * 10**-6

        peak_ind, _ = find_peaks(np.abs(PUNDVoltage[i]), 0.1)
        numpeaks = len(peak_ind)
        peak_width = np.average(peak_ind[0:2]) #Finds index between the first and second peak.
        
        peak_range = [np.arange(peak_ind[j]-peak_width*0.49, peak_ind[j]+peak_width*0.49 + 1, dtype=int) for j in range(numpeaks)]
        
        if (numpeaks == 1):
            EFieldPeaks = [v/d for v in [PUNDVoltage[i][j] for j in peak_range[0]]]
            
            FECurrent = [PUNDCurrent[i][j] for j in peak_range[0]]

        elif (numpeaks > 4):
            EFieldPeaks = np.append([v/d for v in [PUNDVoltage[i][j] for j in peak_range[1]]], [v/d for v in [PUNDVoltage[i][j] for j in peak_range[3]]])

            FECurrentDown = np.subtract([PUNDCurrent[i][j] for j in peak_range[1]], [PUNDCurrent[i][j] for j in peak_range[2]])
            FECurrentUp = np.subtract([PUNDCurrent[i][j] for j in peak_range[3]], [PUNDCurrent[i][j] for j in peak_range[4]])
            FECurrent = np.append(FECurrentUp, FECurrentDown)

        else:
            print("Could not calculate PE curve for file: %s."%Pfile)
            print("Skipping file.")
            continue

        IE_min = min(FECurrent)
        IE_min_xs = [e for e in EFieldPeaks if FECurrent[np.where(EFieldPeaks == e)[0][0]] < IE_min/2.0] 
        IE_min_FWHM = round((max(IE_min_xs) - min(IE_min_xs)) * 10**-8, 2)

        IE_max = max(FECurrent)
        IE_max_xs = [e for e in EFieldPeaks if FECurrent[np.where(EFieldPeaks == e)[0][0]] > IE_max/2.0]
        IE_max_FWHM = round((max(IE_max_xs) - min(IE_max_xs)) * 10**-8, 2)

        QFE = [0] * len(FECurrent)
        for t in range(1, len(FECurrent)):
            dTime = PUNDTime[i][t] - PUNDTime[i][t-1]
            QFE[t] = FECurrent[t] * dTime + QFE[t-1]

        QFE = np.subtract(QFE, (np.max(QFE) + np.min(QFE))/2)

        QFEScaled = np.array([(k / (pi * r**2)) for k in QFE])

        Prpos = round(QFEScaled[0] * 10**2, 2)
        Prneg = round(QFEScaled[int(len(FECurrent)/2)] * 10**2, 2)

        Ec_ind = np.where((QFEScaled > -10**-2) & (QFEScaled < 10**-2))
        Ecneg = round(EFieldPeaks[Ec_ind[0][0]] * 10**-8, 2)
        Ecpos = round(EFieldPeaks[Ec_ind[0][-1]] * 10**-8, 2)

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

        ax1.plot([e * 10**-8 for e in EFieldPeaks], [c * 10**6 for c in FECurrent], color = "b")

        ax1.hlines(IE_min/2 * 10**6, min(IE_min_xs) * 10**-8, max(IE_min_xs) * 10**-8, linestyles = 'dashed')
        ax1.hlines(IE_max/2 * 10**6, min(IE_max_xs) * 10**-8, max(IE_max_xs) * 10**-8, linestyles = 'dashed')

        plt.title(Pfile)
        plt.text(max(IE_min_xs) * 10**-8 + 0.1, IE_min/2 * 10**6, '%s MV/cm²'%IE_min_FWHM, fontsize = "x-large")
        plt.text(max(IE_max_xs) * 10**-8 + 0.1, IE_max/2 * 10**6, '%s MV/cm²'%IE_max_FWHM, fontsize = "x-large")

        ax1.tick_params('both', labelsize = "x-large")

        ax1.set_xlabel("Electric Field [MV/cm]", fontsize = "xx-large")
        ax1.set_ylabel("FE Current [$\mu$A]", fontsize = "xx-large")

        plt.savefig('../Fig/InAsFlashIntA/IE_%s.png'%Pfile)

        ### Plotting P-E
        fig = plt.figure(figsize = (9,6))
        ax1 = fig.add_subplot(111)

        ax1.plot([e * 10**-8 for e in EFieldPeaks], [p * 10**2 for p in QFEScaled], color = "b")

        ax1.plot(0, Prpos, marker = 'o', fillstyle = 'none', markersize = 15, color = 'g')
        ax1.plot(0, Prneg, marker = 'o', fillstyle = 'none', markersize = 15, color = 'g')
        ax1.plot(Ecneg, 0, marker = 'o', fillstyle = 'none', markersize = 15, color = 'r')
        ax1.plot(Ecpos, 0, marker = 'o', fillstyle = 'none', markersize = 15, color = 'r')

        plt.title(Pfile)
        plt.text(0, Prpos * 0.85, '%s $\mu$C/cm²'%Prpos, fontsize = "x-large")
        plt.text(Ecneg * 0.25, Prneg * 0.9, '%s $\mu$C/cm²'%Prneg, fontsize = "x-large")
        plt.text(Ecneg * 0.85, 0, '%s MV/cm²'%Ecneg, fontsize = "x-large")
        plt.text(Ecpos * 1.1, 0, '%s MV/cm²'%Ecpos, fontsize = "x-large")

        ax1.tick_params('both', labelsize = "x-large")

        ax1.set_xlabel("Electric Field [MV/cm]", fontsize = "xx-large")
        ax1.set_ylabel("Polarization [$\mu$C/cm²]", fontsize = "xx-large")

        plt.savefig('../Fig/InAsFlashIntA/PE_%s.png'%Pfile)

        i += 1

plt.show()


