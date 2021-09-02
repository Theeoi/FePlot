#!/usr/bin/env python

import matplotlib.pyplot as plt
import CVPlotter
import PUNDPlotter
import UniCVPlotter

dataLoc = "../Data/InAsFlashIntC/UniCV/"
saveFig = "../Fig/InAsFlashIntC/"

gf1 = "293K"
gf2 = "2V"
gf3 = "3V"
"""
## CV FlashIntC
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
            ["%s5/C12/"%dataLoc, gf1, gf2],
            ["%s5/C13/"%dataLoc, gf1, gf2],
            ["%s5/C3/"%dataLoc, gf1, gf2],
            ["%s5/D13/"%dataLoc, gf1, gf2],
            ["%s5/D2/"%dataLoc, gf1, gf2],
            ["%s5/D4/"%dataLoc, gf1, gf2],
            ["%s5/E4/"%dataLoc, gf1, gf2]
        ]
    ]

dataToPlot = [
        [
            ["%s1/D13/"%dataLoc],
            ["%s1/E12/"%dataLoc],
            ["%s1/E3/"%dataLoc],
            ["%s1/D1/"%dataLoc]
        ],
        [
            ["%s2/D11/"%dataLoc],
            ["%s2/E1/"%dataLoc],
            ["%s2/E2/"%dataLoc],
            ["%s2/C13/"%dataLoc],
            ["%s2/E13/"%dataLoc],
            ["%s2/E12/"%dataLoc]
        ],
        [
            ["%s3/C13/"%dataLoc],
            ["%s3/D1/"%dataLoc],
            ["%s3/E1/"%dataLoc],
            ["%s3/D10/"%dataLoc],
            ["%s3/D9/"%dataLoc],
            ["%s3/E8/"%dataLoc]
        ],
        [
            ["%s4/D12/"%dataLoc],
            ["%s4/D13/"%dataLoc],
            ["%s4/E13/"%dataLoc],
            ["%s4/D11/"%dataLoc],
            ["%s4/E11/"%dataLoc],
            ["%s4/E12/"%dataLoc],
            ["%s4/D9/"%dataLoc],
            ["%s4/E9/"%dataLoc]
        ]
    ]

## FlashNumA PUNDTrends
dataToPlot = [
        [
           ["%s1/D13/"%dataLoc, "3V"],
           ["%s2/E1/"%dataLoc, "3V"],
           ["%s3/E1/"%dataLoc, "3V"]
        ],
        [
           ["%s1/D1/"%dataLoc, "2.5V"],
           ["%s2/E13/"%dataLoc, "2.5V"],
           ["%s3/D10/"%dataLoc, "2.5V"]
        ],
        [
           ["%s1/D1/"%dataLoc, "2V"],
           ["%s2/E12/"%dataLoc, "2V"],
           ["%s3/E8/"%dataLoc, "2V"]
        ]
    ]

dataToPlot = [
        [
           ["%s4/D13/"%dataLoc, "3V"]
        ],
        [
           ["%s4/D11/"%dataLoc, "2.5V"]
        ],
        [
           ["%s4/E9/"%dataLoc, "2V"]
        ]
    ]


## FlashIntA PUNDTrends
dataToPlot = [
        [
           ["%s2/D2/"%dataLoc, "3V"],
           ["%s1/D9/"%dataLoc, "3V"],
           ["%s5/D7/"%dataLoc, "3V"]
        ],
        [
           ["%s2/D2/"%dataLoc, "2.5V"],
           ["%s1/E1/"%dataLoc, "2.5V"],
           ["%s5/D9/"%dataLoc, "2.5V"]
        ],
        [
           ["%s2/D2/"%dataLoc, "2V"],
           ["%s1/D8/"%dataLoc, "2V"],
           ["%s5/D9/"%dataLoc, "2V"]
        ]
    ]
"""
UniCVPlotter.PlotUniCV([["%s1/E9/"%dataLoc]])
#CVPlotter.PlotFreqDispGroup(dataToPlot)

plt.show()
