#!/usr/bin/python

### USAGE ###
# ./PUNDPlot.py <Path to clean PUND data>
# Example: ./PUNDPlot.py ../Data/InAsFlashIntA/PUND

import os
import numpy as np
from scipy.signal import find_peaks
from scipy.constants import pi
import matplotlib.pyplot as plt

d = 10e-9 ## Ferroelectric layer thickness (m)

def SortAndFilterDir(dataArray):
    path = dataArray[0]
    dataFilter = ['.csv', dataArray[1] if len(dataArray) > 1 else '']
    files = [fn for fn in os.listdir(path) if all(fn.find(df) != -1 for df in dataFilter)]
    files.sort()

    if len(files) < 1:
        print("Didn't find any matching data for '%s' with specified filter: %s"%(path, dataFilter))

    return path, files


def GetPUNDData(PUNDpath, PUNDfiles):
    PUNDTime = []
    PUNDCurrent = []
    PUNDVoltage = []
    EFieldPeaks = []
    FECurrent = []
    QFEScaled = []

    i = 0
    for Pfile in PUNDfiles:
        PUNDfile = open(os.path.join(PUNDpath, Pfile), 'r')
        PUNDfilelines = PUNDfile.readlines()

        PUNDTime.append([float(line.split(",")[1]) for line in PUNDfilelines])
        PUNDCurrent.append([float(line.split(",")[2]) for line in PUNDfilelines])
        PUNDVoltage.append([float(line.split(",")[3]) for line in PUNDfilelines])

        PUNDfile.close()

        r = float(Pfile.split("_")[4].replace('um','')) * 10**-6
        
        peak_ind, _ = find_peaks(np.abs(PUNDVoltage[i]), 0.1)
        numpeaks = len(peak_ind)
        peak_width = np.average(peak_ind[0:2]) #Finds index between the first and second peak.
        
        peak_range = [np.arange(peak_ind[j]-peak_width*0.49, peak_ind[j]+peak_width*0.49 + 1, dtype=int) for j in range(numpeaks)]
        
        EFieldPeaks.append(np.append([v/d for v in [PUNDVoltage[i][j] for j in peak_range[1]]], [v/d for v in [PUNDVoltage[i][j] for j in peak_range[3]]]))

        FECurrentDown = np.subtract([-PUNDCurrent[i][j] for j in peak_range[1]], [-PUNDCurrent[i][j] for j in peak_range[2]])
        FECurrentUp = np.subtract([-PUNDCurrent[i][j] for j in peak_range[3]], [-PUNDCurrent[i][j] for j in peak_range[4]])
        FECurrent.append(np.append(FECurrentDown, FECurrentUp))

        QFE = [0] * len(FECurrent[i])
        for t in range(1, len(FECurrent[i])):
            dTime = PUNDTime[i][t] - PUNDTime[i][t-1]
            QFE[t] = FECurrent[i][t] * dTime + QFE[t-1]

        QFE = np.subtract(QFE, (np.max(QFE) + np.min(QFE))/2)

        QFEScaled.append(np.array([(k / (pi * r**2)) for k in QFE]))

        i += 1

    return PUNDTime, PUNDCurrent, PUNDVoltage, EFieldPeaks, FECurrent, QFEScaled


def PlotPUND(dataArray, saveFig = ''):
    for data in dataArray:
        PUNDpath, PUNDfiles = SortAndFilterDir(data)

        if len(PUNDfiles) < 1:
            print("Skipping...")
            continue

        PUNDTime, PUNDCurrent, PUNDVoltage, _, _, _ = GetPUNDData(PUNDpath, PUNDfiles)

        SampleID = PUNDfiles[0].split("_")[2] + "_" + PUNDfiles[0].split("_")[3] + "_" + PUNDfiles[0].split("_")[5].replace('.csv','')

        for i in range(len(PUNDfiles)):
            fig = plt.figure(figsize = (9,6))
            ax1 = fig.add_subplot(111)
            ax2 = ax1.twinx()

            ax1.plot([t * 10**3 for t in PUNDTime[i]], [c * 10**6 for c in PUNDCurrent[i]], label = "Current", color = "b")

            ax2.plot([t * 10**3 for t in PUNDTime[i]], PUNDVoltage[i], label = "Voltage", color = "c")

            plt.title(SampleID)
            fig.legend(fontsize = 'x-large', loc = 4, bbox_to_anchor = (1,0), bbox_transform = ax1.transAxes)

            ax1.tick_params('both', labelsize = "x-large")
            ax2.tick_params('both', labelsize = "x-large")

            ax1.set_xlabel("Time [ms]", fontsize = "xx-large")
            ax1.set_ylabel("Current [$\mu$A]", fontsize = "xx-large")
            ax2.set_ylabel("Voltage [V]", fontsize = "xx-large")

            if saveFig != '':
                plt.savefig(saveFig + 'PUND_%s.png'%SampleID)


def PlotIE(dataArray, saveFig = ''):
    for data in dataArray:
        PUNDpath, PUNDfiles = SortAndFilterDir(data)

        if len(PUNDfiles) < 1:
            print("Skipping...")
            continue

        _, _, _, EFieldPeaks, FECurrent, QFEScaled = GetPUNDData(PUNDpath, PUNDfiles)

        SampleID = PUNDfiles[0].split("_")[2] + "_" + PUNDfiles[0].split("_")[3] + "_" + PUNDfiles[0].split("_")[5].replace('.csv','')

        for i in range(len(PUNDfiles)):
            IE_min, IE_max = min(FECurrent[i]), max(FECurrent[i])
            IE_min_xs, IE_max_xs = [e for e in EFieldPeaks[i] if FECurrent[i][np.where(EFieldPeaks[i] == e)[0][0]] < IE_min/2.0], [e for e in EFieldPeaks[i] if FECurrent[i][np.where(EFieldPeaks[i] == e)[0][0]] > IE_max/2.0]
            IE_min_FWHM, IE_max_FWHM = round((max(IE_min_xs) - min(IE_min_xs)) * 10**-8, 2), round((max(IE_max_xs) - min(IE_max_xs)) * 10**-8, 2)

            fig = plt.figure(figsize = (9,6))
            ax1 = fig.add_subplot(111)

            ax1.plot([e * 10**-8 for e in EFieldPeaks[i]], [c * 10**6 for c in FECurrent[i]], color = "b")

            ax1.hlines(IE_min/2 * 10**6, min(IE_min_xs) * 10**-8, max(IE_min_xs) * 10**-8, linestyles = 'dashed')
            ax1.hlines(IE_max/2 * 10**6, min(IE_max_xs) * 10**-8, max(IE_max_xs) * 10**-8, linestyles = 'dashed')

            plt.title(SampleID)
            plt.text(max(IE_min_xs) * 10**-8 + 0.1, IE_min/2 * 10**6, '%s MV/cm'%IE_min_FWHM, fontsize = "x-large")
            plt.text(max(IE_max_xs) * 10**-8 + 0.1, IE_max/2 * 10**6, '%s MV/cm'%IE_max_FWHM, fontsize = "x-large")

            ax1.tick_params('both', labelsize = "x-large")

            ax1.set_xlabel("Electric Field [MV/cm]", fontsize = "xx-large")
            ax1.set_ylabel("FE Current [$\mu$A]", fontsize = "xx-large")

            if saveFig != '':
                plt.savefig(saveFig + 'IE_%s.png'%SampleID)

def PlotPE(dataArray, saveFig = ''):
    avgPr = []
    avgEc = []

    for data in dataArray:
        PUNDpath, PUNDfiles = SortAndFilterDir(data)

        _, _, _, EFieldPeaks, _, QFEScaled = GetPUNDData(PUNDpath, PUNDfiles)

        label = data[1]

        if PUNDfiles:
            SampleID = PUNDfiles[0].split("_")[2] + "_" + PUNDfiles[0].split("_")[3] + "_" + PUNDfiles[0].split("_")[5].replace('.csv','')
        else:
            avgPr.append(None)
            avgEc.append(None)
            print("Skipping...")
            continue

        for i in range(len(PUNDfiles)):
            Prpos = round(QFEScaled[i][0] * 10**2, 2)
            Prneg = round(QFEScaled[i][int(len(QFEScaled[i])/2)] * 10**2, 2)
            avgPr.append(np.mean(np.abs([Prpos, Prneg])))

            Ec_ind = np.where((QFEScaled[i] > -5 * 10**-3) & (QFEScaled[i] < 5 * 10**-3))
            Ecneg = round(EFieldPeaks[i][Ec_ind[0][0]] * 10**-8, 2)
            Ecpos = round(EFieldPeaks[i][Ec_ind[0][-1]] * 10**-8, 2)
            avgEc.append(np.mean(np.abs([Ecpos, Ecneg])))

            fig = plt.figure(figsize = (9,6))
            ax1 = fig.add_subplot(111)

            ax1.plot([e * 10**-8 for e in EFieldPeaks[i]], [p * 10**2 for p in QFEScaled[i]], color = "b")

            ax1.plot(0, Prpos, marker = 'o', fillstyle = 'none', markersize = 15, color = 'g')
            ax1.plot(0, Prneg, marker = 'o', fillstyle = 'none', markersize = 15, color = 'g')
            ax1.plot(Ecneg, 0, marker = 'o', fillstyle = 'none', markersize = 15, color = 'r')
            ax1.plot(Ecpos, 0, marker = 'o', fillstyle = 'none', markersize = 15, color = 'r')

            plt.title(SampleID)
            plt.text(0, Prpos * 0.85, '%s $\mu$C/cm²'%Prpos, fontsize = "x-large")
            plt.text(Ecneg * 0.25, Prneg * 0.9, '%s $\mu$C/cm²'%Prneg, fontsize = "x-large")
            plt.text(Ecneg * 0.85, 0, '%s MV/cm'%Ecneg, fontsize = "x-large")
            plt.text(Ecpos * 1.1, 0, '%s MV/cm'%Ecpos, fontsize = "x-large")

            ax1.tick_params('both', labelsize = "x-large")

            ax1.set_xlabel("Electric Field [MV/cm]", fontsize = "xx-large")
            ax1.set_ylabel("Polarization [$\mu$C/cm²]", fontsize = "xx-large")

            if saveFig != '':
                plt.savefig(saveFig + 'PE_%s.png'%SampleID)

    return avgPr, avgEc, label

def PUNDTrend(dataArray, xaxes, **kwargs):
    figPr = plt.figure(figsize = (9,6))
    axPr = figPr.add_subplot(111)

    figEc = plt.figure(figsize = (9,6))
    axEc = figEc.add_subplot(111)

    for i in range(len(dataArray)):
        avgPr, avgEc, label = PlotPE(dataArray[i])

        axPr.plot(xaxes, avgPr, label=label, marker='o', ls='--')
        axEc.plot(xaxes, avgEc, label=label, marker='o', ls='--')

    figPr.legend(title="Cycling Voltage", fontsize = 'x-large', loc = 4, bbox_to_anchor = (1,0), bbox_transform = axPr.transAxes)
    figEc.legend(title="Cycling Voltage", fontsize = 'x-large', loc = 4, bbox_to_anchor = (1,0), bbox_transform = axEc.transAxes)

    axPr.tick_params('both', labelsize = "x-large")
    axEc.tick_params('both', labelsize = "x-large")

    axPr.set_xlabel(kwargs.get('xlabel'), fontsize = "xx-large")
    axEc.set_xlabel(kwargs.get('xlabel'), fontsize = "xx-large")
    axPr.set_ylabel("Remnant Polarization [$\mu$C/cm²]", fontsize = "xx-large")
    axEc.set_ylabel("Coercive Field [MV/cm]", fontsize = "xx-large")


