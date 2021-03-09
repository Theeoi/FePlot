#!/usr/bin/python

### USAGE ###
# ./PUNDPlot.py <Path to clean PUND data>
# Example: ./PUNDPlot.py ../Data/InAsFlashIntA/PUND

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

## Read data

PUNDpath = sys.argv[1]
PUNDfiles = os.listdir(PUNDpath)
PUNDfiles.sort()
numfiles = len(PUNDfiles)

PUNDTime = [0] * numfiles
PUNDCurrent = [0] * numfiles
PUNDVoltage = [0] * numfiles

i = 0
for file in PUNDfiles:
    if file.endswith('.csv'):
        PUNDfile = open(os.path.join(PUNDpath, file), 'r')
        PUNDfilelines = PUNDfile.readlines()

        PUNDTime[i] = [float(line.split(",")[1]) for line in PUNDfilelines]
        PUNDCurrent[i] = [float(line.split(",")[2]) for line in PUNDfilelines]
        PUNDVoltage[i] = [float(line.split(",")[3]) for line in PUNDfilelines]

        PUNDfile.close()

        fig = plt.figure(figsize = (9,6))
        ax1 = fig.add_subplot(111)
        ax2 = ax1.twinx()

        ax1.plot([t * 10**3 for t in PUNDTime[i]], [c * 10**6 for c in PUNDCurrent[i]], label = "Current", color = "b")

        ax2.plot([t * 10**3 for t in PUNDTime[i]], PUNDVoltage[i], label = "Voltage", color = "c")

        plt.title(file)
        fig.legend(fontsize = 'x-large', loc = 4, bbox_to_anchor = (1,0), bbox_transform = ax1.transAxes)

        ax1.tick_params('both', labelsize = "x-large")
        ax2.tick_params('both', labelsize = "x-large")

        ax1.set_xlabel("Time [ms]", fontsize = "xx-large")
        ax1.set_ylabel("Current [uA]", fontsize = "xx-large")
        ax2.set_ylabel("Voltage [V]", fontsize = "xx-large")

        i += 1


plt.show()


