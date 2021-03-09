#!/usr/bin/python

### USAGE ###
# ./PUNDPlot.py <Path to clean PUND data>
# Example: ./PUNDPlot.py ../Data/InAsFlashIntA/PUND

import sys
import matplotlib.pyplot as plt

## Read data

PUNDpath = sys.argv[1]
PUNDfile = open(PUNDpath)
PUNDfilelines = PUNDfile.readlines()

PUNDTime = []
PUNDCurrent = []
PUNDVoltage = []
for line in PUNDfilelines:
    PUNDTime.append(float(line.split(",")[1]))
    PUNDCurrent.append(float(line.split(",")[2]))
    PUNDVoltage.append(float(line.split(",")[3]))

PUNDfile.close()

fig = plt.figure(figsize = (9,6))
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()

ax1.plot([t * 10**3 for t in PUNDTime], [i * 10**6 for i in PUNDCurrent], label = "Current", color = "b")

ax2.plot([t * 10**3 for t in PUNDTime], PUNDVoltage, label = "Voltage", color = "c")

fig.legend(fontsize = 'x-large', loc = 4, bbox_to_anchor = (1,0), bbox_transform = ax1.transAxes)

ax1.tick_params('both', labelsize = "x-large")
ax2.tick_params('both', labelsize = "x-large")

ax1.set_xlabel("Time [ms]", fontsize = "xx-large")
ax1.set_ylabel("Current [uA]", fontsize = "xx-large")
ax2.set_ylabel("Voltage [V]", fontsize = "xx-large")

#plt.savefig('../Fig/PLE_Y.png')
plt.show()


