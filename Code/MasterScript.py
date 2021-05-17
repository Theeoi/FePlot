#!/usr/bin/env python

import matplotlib.pyplot as plt
import CVPlotter

dataLoc = "../Data/InAsFlashIntC/CV/"
saveFig = "../Fig/test/"

gf1 = "13K"
gf2 = "3V"

dataToPlot = [ 
        #["%s1/D1/"%dataLoc, gf1, gf2],
        #["%s1/D12/"%dataLoc, gf1, gf2],
        ["%s1/C12/"%dataLoc, gf1, gf2],
        ["%s1/D2/"%dataLoc, gf1, gf2],
        ["%s1/D3/"%dataLoc, gf1, gf2],
        #["%s1/E12/"%dataLoc, gf1, gf2],
        ["%s1/E2/"%dataLoc, gf1, gf2],
        #["%s1/E12/"%dataLoc],
        #["%s1/E2/"%dataLoc, "13K", "3V"],
        #["%s1/D3/"%dataLoc, "2.5V"]
        ]

CVPlotter.PlotFreqDisp(dataToPlot)
CVPlotter.PlotFreqDispAvg(dataToPlot)

plt.show()
