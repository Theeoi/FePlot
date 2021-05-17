#!/usr/bin/env python

import os
import matplotlib.pyplot as plt
import CapacitancePlot

fig = plt.figure(figsize = (10,6))
ax1 = fig.add_subplot(111)

dataLoc = "../Data/InAsFlashIntC/CV/"

dataToPlot = [ 
        ["%s1/C12/"%dataLoc, "2.5V"],
        ["%s1/D13/"%dataLoc, "2.5V"],
        ["%s1/D2/"%dataLoc, "293K", "2.5V"],
        ["%s1/D2/"%dataLoc, "13K", "2.5V"],
        #["%s1/E5/"%dataLoc, "3V"],
        #["%s1/D2/"%dataLoc, "293K", "3V"],
        #["%s1/D3/"%dataLoc, "3V"],
        #["%s1/E12/"%dataLoc],
        #["%s1/E2/"%dataLoc, "13K", "3V"],
        ["%s1/D3/"%dataLoc, "2.5V"]
        ]

for data in dataToPlot:
    CapacitancePlot.PlotCV(ax1, data)

ax1.legend(fontsize = 10, loc = 1, bbox_to_anchor = (1,1), bbox_transform = ax1.transAxes)
plt.show()
