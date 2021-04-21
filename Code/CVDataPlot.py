#!/usr/bin/python

### USAGE ###
# ./CVDataPlot.py <Path to clean CV data file>
# EXAMPLE: ./CVDataPlot.py ../Data/InAsFlashIntA/CV/...csv

import sys
import matplotlib.pyplot as plt

## Read data

CVPath = sys.argv[1]
CVFile = open(CVPath)
CVFilelines = CVFile.readlines()

CVVoltage = []
CVCapacitance = []
for line in CVFilelines:
    CVVoltage.append(float(line.split(",")[2]))
    CVCapacitance.append(float(line.split(",")[1]))

CVFile.close()

fig = plt.figure(figsize = (9,6))
ax1 = fig.add_subplot(111)

ax1.plot(CVVoltage, [i for i in CVCapacitance], label = "Capacitance", color = "b")

ax1.tick_params('both', labelsize = "x-large")

ax1.set_xlabel("Voltage [V]", fontsize = "xx-large")
ax1.set_ylabel("Capacitance [F]", fontsize = "xx-large")

#plt.savefig('../Fig/PLE_Y.png')
plt.show()


