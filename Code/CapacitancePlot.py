#!/usr/bin/env python

### USAGE ###
# ./CapacitancePlot.py <Path to clean CV data directory>
# EXAMPLE: ./CapacitancePlot.py ../Data/InAsFlashIntA/CV/..

import sys
import os
import numpy as np
from scipy.constants import pi
from scipy.constants import epsilon_0
import math
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore", message = "invalid value encountered in double_scalars")
warnings.filterwarnings("ignore", message = "divide by zero encountered in double_scalars")

d = 10e-9 #Ferroelectric layer thickness (m)
Filter1 = sys.argv[3] if len(sys.argv) > 3 else ''
Filter2 = sys.argv[4] if len(sys.argv) > 4 else ''

## Read data

CVPath = sys.argv[1]
CVFiles = os.listdir(CVPath)
CVFiles.sort()

CVVoltage = []
freq = []
C_HZO = []
epsilon_r = []

i = 0
for Cfile in CVFiles:
    if Cfile.endswith('.csv') and Cfile.find(Filter1) != -1 and Cfile.find(Filter2) != -1: #find filters to Filter
        CVFile = open(os.path.join(CVPath, Cfile), 'r')
        CVFilelines = CVFile.readlines()
        V_max = Cfile.split("_")[6]
        SampleID = Cfile.split("_")[2] + "_" + Cfile.split("_")[3] + "_" + Cfile.split("_")[4] + "_" + Cfile.split("_")[1]

        CVVoltage.append([float(line.split(",")[2]) for line in CVFilelines])
        CVX = [float(line.split(",")[1]) * -1 for line in CVFilelines]

        CVFile.close()

        r = float(Cfile.split("_")[5].replace('um','')) * 10**-6
        A = pi * r**2
        freq.append(float(Cfile.split("_")[7].replace('Hz','')))

        C_HZO.append(np.array([1 / (2 * pi * freq[i] * X * A) for X in CVX]))
        epsilon_r.append(np.array([(d / epsilon_0) * c for c in C_HZO[i]]))

        i += 1

if i == 0:
    print("Didn't find any matching data. Exiting...")
    exit(1)

Cdisp = [(((C_HZO[0::2][-1][-1] - C_HZO[0::2][j][-1])/C_HZO[0::2][-1][-1]) * 10**2)/math.log10(freq[0::2][j]/freq[-1]) for j in range(int(i/2))]
"""
## Plot Capacitance and Epsilon
fig = plt.figure(figsize = (10,6))
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()

cmap = plt.get_cmap('Set1')
colors = iter(cmap(np.linspace(0,1,9)))

for i in range(i):
    if i % 2 == 0:
        color = next(colors)
        ax1.plot(CVVoltage[i], [c * 10**2 for c in C_HZO[i]], label = '%s MHz'%int(freq[i] * 10**-6) if freq[i] % 1000000 == 0 else '%s kHz'%int(freq[i] * 10**-3), color = color)

        ax2.plot(CVVoltage[i], epsilon_r[i], color = "r", alpha = 0)
    else:
        ax1.plot(CVVoltage[i], [c * 10**2 for c in C_HZO[i]], linestyle = '--', dash_capstyle = 'round', color = color)

        ax2.plot(CVVoltage[i], epsilon_r[i], color = "r", alpha = 0)

ax2.annotate("", (-0.1, np.min(epsilon_r)), (-1, np.min(epsilon_r)), arrowprops = dict(arrowstyle = "->", linewidth = 1.5))
ax2.annotate("", (0.1, np.min(epsilon_r)), (1, np.min(epsilon_r)), arrowprops = dict(arrowstyle = "->", linestyle = '--', linewidth = 1.5))

fig.legend(fontsize = 'x-large', loc = 2, bbox_to_anchor = (0,1), bbox_transform = ax1.transAxes)

plt.title(SampleID)

ax1.tick_params('both', labelsize = "x-large")
ax2.tick_params('both', labelsize = "x-large")

ax1.set_xlabel("Voltage [V]", fontsize = "xx-large")
ax1.set_ylabel("Capacitance [$\mu$F/cm²]", fontsize = "xx-large")
ax2.set_ylabel("Dielectric Constant $\epsilon_r$", fontsize = "xx-large")

#plt.savefig('../Fig/InAs%s'%Cfile.split("_")[2] + '/CV_%s.png'%SampleID)
"""
## Plot Frequency-Dispersion
#fig = plt.figure(figsize = (10,6))
#ax1 = fig.add_subplot(111)

ax1.semilogx(freq[0::2], Cdisp, marker = 'o', markersize = 15, ls = ':')
ax1.set_ylim([0, max(Cdisp) + 1])

plt.title(SampleID)

ax1.tick_params('both', labelsize = "x-large")
ax1.set_xlabel("Frequency [Hz]", fontsize = "xx-large")
ax1.set_ylabel('Frequency Dispersion @ +%s'%V_max + ' [%/dec]', fontsize = "xx-large")

#plt.savefig('../Fig/InAs%s'%Cfile.split("_")[2] + '/FreqDisp_%s.png'%SampleID)

plt.show()


