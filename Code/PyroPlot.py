#!/usr/bin/python

### USAGE ###
# ./PyroPlot.py <Path to clean Pyro data>

import sys
import numpy as np
import matplotlib.pyplot as plt

## Read data

PyroPath = sys.argv[1]
PyroFile = open(PyroPath)
PyroFilelines = PyroFile.readlines()

PyroTime = []
PyroTemp = []
for line in PyroFilelines:
    PyroTime.append(float(line.split(",")[0]))
    PyroTemp.append(float(line.split(",")[1]))

PyroFile.close()

Tpeak = np.max(PyroTemp) + 273.15

fig = plt.figure(figsize = (9,6))
ax1 = fig.add_subplot(111)

ax1.plot(PyroTime, PyroTemp, label = "Pyrometer Temperature", color = "r")
fig.text(0.2,0.75,'$T_{peak}$ = %s K' %Tpeak, fontsize = "xx-large")

ax1.tick_params('both', labelsize = "x-large")

ax1.set_xlabel("Time [s]", fontsize = "xx-large")
ax1.set_ylabel("Temperature [C]", fontsize = "xx-large")

#plt.savefig('../Fig/PLE_Y.png')
plt.show()


