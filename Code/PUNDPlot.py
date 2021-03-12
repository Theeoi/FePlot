#!/usr/bin/python

### USAGE ###
# ./PUNDPlot.py <Path to clean PUND data>
# Example: ./PUNDPlot.py ../Data/InAsFlashIntA/PUND_FE...csv

import sys
import os
import numpy as np
from scipy.signal import find_peaks
from scipy.constants import pi
import matplotlib.pyplot as plt

## Read data

PUNDpath = sys.argv[1]

PUNDfile = open(PUNDpath, 'r')
PUNDfilelines = PUNDfile.readlines()

PUNDTime = [float(line.split(",")[1]) for line in PUNDfilelines]
PUNDCurrent = [float(line.split(",")[2]) for line in PUNDfilelines]
PUNDVoltage = [float(line.split(",")[3]) for line in PUNDfilelines]

PUNDfile.close()

### Plotting PUND Measurements
fig = plt.figure(figsize = (9,6))
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()

ax1.plot([t * 10**3 for t in PUNDTime], [c * 10**6 for c in PUNDCurrent], label = "Current", color = "b")

ax2.plot([t * 10**3 for t in PUNDTime], PUNDVoltage, label = "Voltage", color = "c")

fig.legend(fontsize = 'x-large', loc = 4, bbox_to_anchor = (1,0), bbox_transform = ax1.transAxes)

ax1.tick_params('both', labelsize = "x-large")
ax2.tick_params('both', labelsize = "x-large")

ax1.set_xlabel("Time [ms]", fontsize = "xx-large")
ax1.set_ylabel("Current [$\mu$A]", fontsize = "xx-large")
ax2.set_ylabel("Voltage [V]", fontsize = "xx-large")

plt.show()


