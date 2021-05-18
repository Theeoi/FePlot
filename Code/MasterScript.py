#!/usr/bin/env python

import matplotlib.pyplot as plt
import CVPlotter

dataLoc = "../Data/InAsFlashIntC/CV/"
saveFig = "../Fig/InAsFlashIntC/"

gf1 = "293K"
gf2 = "2.5V"

dataToPlot = [ 
        [ 
            ["%s1/C12/"%dataLoc, gf1, gf2],
            ["%s1/D1/"%dataLoc, gf1, gf2],
            ["%s1/D10/"%dataLoc, gf1, gf2],
            ["%s1/D12/"%dataLoc, gf1, gf2],
            ["%s1/D13/"%dataLoc, gf1, gf2],
            ["%s1/D2/"%dataLoc, gf1, gf2],
            ["%s1/D3/"%dataLoc, gf1, gf2],
            ["%s1/E12/"%dataLoc, gf1, gf2],
            ["%s1/E2/"%dataLoc, gf1, gf2]
        ],
        [
            ["%s2/C3/"%dataLoc, gf1, gf2],
            ["%s2/D4/"%dataLoc, gf1, gf2],
            ["%s2/D5/"%dataLoc, gf1, gf2],
            ["%s2/D8/"%dataLoc, gf1, gf2],
            ["%s2/E12/"%dataLoc, gf1, gf2],
            ["%s2/E4/"%dataLoc, gf1, gf2],
            ["%s2/E7/"%dataLoc, gf1, gf2]
        ],
        [
            ["%s3/C10/"%dataLoc, gf1, gf2],
            ["%s3/C2/"%dataLoc, gf1, gf2],
            ["%s3/D1/"%dataLoc, gf1, gf2],
            ["%s3/D4/"%dataLoc, gf1, gf2],
            ["%s3/E2/"%dataLoc, gf1, gf2],
            ["%s3/E3/"%dataLoc, gf1, gf2],
            ["%s3/E5/"%dataLoc, gf1, gf2],
            ["%s3/F11/"%dataLoc, gf1, gf2]
        ],
        [
            ["%s4/C7/"%dataLoc, gf1, gf2],
            ["%s4/D10/"%dataLoc, gf1, gf2],
            ["%s4/D7/"%dataLoc, gf1, gf2],
            ["%s4/D8/"%dataLoc, gf1, gf2]
        ],
        [
            ["%s5/C12/"%dataLoc, gf1, gf2],
            ["%s5/C13/"%dataLoc, gf1, gf2],
            ["%s5/C3/"%dataLoc, gf1, gf2],
            ["%s5/D13/"%dataLoc, gf1, gf2],
            ["%s5/D2/"%dataLoc, gf1, gf2],
            ["%s5/D4/"%dataLoc, gf1, gf2],
            ["%s5/E4/"%dataLoc, gf1, gf2]
        ]
    ]

CVPlotter.PlotFreqDispGroup(dataToPlot)

plt.show()
