#!/usr/bin/python

### USAGE ###
# ./CVDataPlot.py <Path to clean CV data file>
# EXAMPLE: ./CVDataPlot.py ../Data/InAsFlashIntA/CV/...csv

import sys
from scipy.constants import pi
from scipy.constants import epsilon_0
import matplotlib.pyplot as plt

d = 10e-9 #Oxide thickness (m)

## Read data

CVPath = sys.argv[1]
CVFile = open(CVPath)
CVFilelines = CVFile.readlines()

CVVoltage = []
CVX = []
for line in CVFilelines:
    CVVoltage.append(float(line.split(",")[2]))
    CVX.append(float(line.split(",")[1]) * -1)

CVFile.close()

r = float(CVPath.split("_")[5].replace('um','')) * 10**-6
A = pi * r**2
freq = float(CVPath.split("_")[7].replace('Hz',''))

C_HZO = [1 / (2 * pi * freq * X * A) for X in CVX]
epsilon_r = [(d / epsilon_0) * c for c in C_HZO]

## Plot raw data
fig = plt.figure(figsize = (10,6))
ax1 = fig.add_subplot(111)

ax1.plot(CVVoltage, [c * 10**-3 for c in CVX], label = "Impedance", color = "g") 

ax1.tick_params('both', labelsize = "x-large")

ax1.set_xlabel("Voltage [V]", fontsize = "xx-large")
ax1.set_ylabel("Impedance [$k\Omega$]", fontsize = "xx-large")

## Plot Capacitance and Epsilon
fig = plt.figure(figsize = (10,6))
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()

ax1.plot(CVVoltage, [c * 10**2 for c in C_HZO], label = "Capacitance", color = "b")

ax2.plot(CVVoltage, epsilon_r, label = "Dielectric Constant", color = "r")

#fig.legend(fontsize = 'x-large', loc = 4, bbox_to_anchor = (1,0), bbox_transform = ax1.transAxes)

ax1.tick_params('both', labelsize = "x-large")
ax2.tick_params('both', labelsize = "x-large")

ax1.set_xlabel("Voltage [V]", fontsize = "xx-large")
ax1.set_ylabel("Capacitance [$\mu$F/cm²]", fontsize = "xx-large")
ax2.set_ylabel("Dielectric Constant $\epsilon_r$", fontsize = "xx-large")

#plt.savefig('../Fig/PLE_Y.png')
plt.show()


