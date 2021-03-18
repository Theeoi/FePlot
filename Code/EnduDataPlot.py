#!/usr/bin/python

### USAGE ###
# ./EndurancePlot.py <Path to clean Endurace data>

import sys
import matplotlib.pyplot as plt

## Read data

EnduPath = sys.argv[1]
EnduFile = open(EnduPath)
EnduFilelines = EnduFile.readlines()

EnduTime = []
EnduCurrent = []
EnduVoltage = []
for line in EnduFilelines:
    EnduTime.append(float(line.split(",")[1]))
    EnduCurrent.append(float(line.split(",")[2]))
    EnduVoltage.append(float(line.split(",")[3]))

EnduFile.close()

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

#plt.savefig('../Fig/PLE_Y.png')
plt.show()


