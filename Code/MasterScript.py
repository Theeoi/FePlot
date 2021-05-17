#!/usr/bin/env python

import matplotlib.pyplot as plt
import CVPlotter

dataLoc = "../Data/InAsFlashIntC/CV/"

dataToPlot = [ 
        ["%s1/C12/"%dataLoc, "2.5V"],
        #["%s1/D13/"%dataLoc, "2.5V"],
        #["%s1/D2/"%dataLoc, "293K", "2.5V"],
        #["%s1/D2/"%dataLoc, "13K", "2.5V"],
        #["%s1/E5/"%dataLoc, "3V"],
        #["%s1/D2/"%dataLoc, "293K", "3V"],
        #["%s1/D3/"%dataLoc, "3V"],
        #["%s1/E12/"%dataLoc],
        #["%s1/E2/"%dataLoc, "13K", "3V"],
        #["%s1/D3/"%dataLoc, "2.5V"]
        ]

CVPlotter.PlotCV(dataToPlot)
CVPlotter.PlotFreqDisp(dataToPlot)

plt.show()
