#!/usr/bin/env python

import matplotlib.pyplot as plt
import CVPlotter
import PUNDPlotter
import EnduPlotter
import UniCVPlotter

dataLoc = "../Data/InAsFlashIntE/UniCV/"
saveFig = "../Fig/InAsFlashIntE/"

gf1 = "293K"
gf2 = "2V"
gf3 = "3.0V"
gf4 = "13K"
"""
## FlashIntC PUNDTrends
dataToPlot = [
    [
        [
            [20],
            ["%s3/D2/"%dataLoc]
        ],
        [
            [25],
            ["%s2/C2/"%dataLoc],
            ["%s2/D1/"%dataLoc],
            ["%s2/D2/"%dataLoc],
            ["%s2/D3/"%dataLoc]
        ],
        [
            [30],
            ["%s1/C4/"%dataLoc],
            ["%s1/C7/"%dataLoc],
            ["%s1/D1/"%dataLoc],
            ["%s1/D10/"%dataLoc],
            ["%s1/D4/"%dataLoc],
            ["%s1/D9/"%dataLoc],
            ["%s1/E1/"%dataLoc],
            ["%s1/E11/"%dataLoc],
            ["%s1/E4/"%dataLoc],
            ["%s1/E9/"%dataLoc]
        ],
        [
            [32.5],
            ["%s5/C7/"%dataLoc],
            ["%s5/C8/"%dataLoc],
            ["%s5/D10/"%dataLoc],
            ["%s5/D7/"%dataLoc],
            ["%s5/D9/"%dataLoc],
            ["%s5/E10/"%dataLoc],
        ]
    ]
]

## FlashIntC + FlashIntE PUNDTrends
dataToPlot = [ 
    [
        [
            [20],
            ["%s3/D2/"%dataLoc]
        ],
        [
            [25],
            ["%s2/C2/"%dataLoc],
            ["%s2/D1/"%dataLoc],
            ["%s2/D2/"%dataLoc],
            ["%s2/D3/"%dataLoc]
        ],
        [
            [30],
            ["%s1/C4/"%dataLoc],
            ["%s1/C7/"%dataLoc],
            ["%s1/D1/"%dataLoc],
            ["%s1/D10/"%dataLoc],
            ["%s1/D4/"%dataLoc],
            ["%s1/D9/"%dataLoc],
            ["%s1/E1/"%dataLoc],
            ["%s1/E11/"%dataLoc],
            ["%s1/E4/"%dataLoc],
            ["%s1/E9/"%dataLoc]
        ],
        [
            [32.5],
            ["%s5/C7/"%dataLoc],
            ["%s5/C8/"%dataLoc],
            ["%s5/D10/"%dataLoc],
            ["%s5/D7/"%dataLoc],
            ["%s5/D9/"%dataLoc],
            ["%s5/E10/"%dataLoc],
        ]
    ],
    [
        [
            [30],
            ["../Data/InAsFlashIntE/PUND/1/E1/"],
            ["../Data/InAsFlashIntE/PUND/1/E2/"]
        ],
        [
            [25],
            ["../Data/InAsFlashIntE/PUND/2/E12/"],
            ["../Data/InAsFlashIntE/PUND/2/E13/"]
        ],
        [
            [20],
            ["../Data/InAsFlashIntE/PUND/3/D11/"]
        ]
    ] 
]

## FlashNumA + FlashNumC PUNDTrends
dataToPlot = [
    [
        [
            [1],
            ["%s1/D1/"%dataLoc],
            ["%s1/D13/"%dataLoc],
            ["%s1/E12/"%dataLoc],
            ["%s1/E3/"%dataLoc]
        ],
        [
            [2],
            ["%s2/C13/"%dataLoc],
            ["%s2/D11/"%dataLoc],
            ["%s2/E1/"%dataLoc],
            ["%s2/E12/"%dataLoc],
            ["%s2/E13/"%dataLoc],
            ["%s2/E2/"%dataLoc]
        ],
        [
            [4],
            ["%s3/C13/"%dataLoc],
            ["%s3/D1/"%dataLoc],
            ["%s3/D10/"%dataLoc],
            ["%s3/D9/"%dataLoc],
            ["%s3/E1/"%dataLoc],
            ["%s3/E8/"%dataLoc],
        ],
        [
            [8],
            ["../Data/InAsFlashNumC/PUND/4/D4/"],
            ["../Data/InAsFlashNumC/PUND/4/D5/"],
            ["../Data/InAsFlashNumC/PUND/4/D6/"]
        ]
    ],
    [
        [
            [2],
            ["../Data/InAsFlashNumC/PUND/1/D5/"],
            ["../Data/InAsFlashNumC/PUND/1/E5"]
        ],
        [
            [4],
            ["../Data/InAsFlashNumC/PUND/2/D7/"],
            ["../Data/InAsFlashNumC/PUND/2/E7/"]
        ],
        [
            [8],
            ["../Data/InAsFlashNumC/PUND/3/D4/"],
            ["../Data/InAsFlashNumC/PUND/3/D5/"],
            ["../Data/InAsFlashNumC/PUND/3/E5/"]
        ]
    ]
]

## FlashNumD PUNDTrends
dataToPlot = [
    [
        [
            [1],
            ["../Data/InAsFlashIntE/PUND/3/D11/"]
        ],
        [
            [2],
            ["%s4/D12/"%dataLoc],
            ["%s4/E12/"%dataLoc]
        ],
        [
            [4],
            ["%s5/D3/"%dataLoc],
            ["%s5/D4/"%dataLoc],
        ]
    ]
]

## FlashIntC Endu
dataToPlot = [
        [
            ["%s2/C2/"%dataLoc, gf3],
            ["%s2/D1/"%dataLoc, gf3],
            ["%s2/D2/"%dataLoc, gf3],
            ["%s2/D3/"%dataLoc, gf3]
        ],
        [
            ["%s1/C4/"%dataLoc, gf3],
            ["%s1/C7/"%dataLoc, gf3],
            ["%s1/D4/"%dataLoc, gf3],
            ["%s1/D1/"%dataLoc, gf3],
            ["%s1/D10/"%dataLoc, gf3],
            ["%s1/D7/"%dataLoc, gf3],
            ["%s1/D8/"%dataLoc, gf3],
            ["%s1/D9/"%dataLoc, gf3],
            ["%s1/E1/"%dataLoc, gf3],
            ["%s1/E11/"%dataLoc, gf3],
            ["%s1/E4/"%dataLoc, gf3],
            ["%s1/E9/"%dataLoc, gf3]
        ],
        [
            ["%s5/C7/"%dataLoc, gf3],
            ["%s5/C8/"%dataLoc, gf3],
            ["%s5/D10/"%dataLoc, gf3],
            ["%s5/D7/"%dataLoc, gf3],
            ["%s5/D9/"%dataLoc, gf3],
            ["%s5/E10/"%dataLoc, gf3],
            ["%s5/E7/"%dataLoc, gf3],
            ["%s5/E8/"%dataLoc, gf3],
            ["%s5/E9/"%dataLoc, gf3]
        ],
        [
            ["../Data/InAsFlashNumA/Endu/4/D11/", gf3],
            ["../Data/InAsFlashNumA/Endu/4/D12/", gf3],
            ["../Data/InAsFlashNumA/Endu/4/D13/", gf3],
            ["../Data/InAsFlashNumA/Endu/4/D9/", gf3],
            ["../Data/InAsFlashNumA/Endu/4/E11/", gf3],
            ["../Data/InAsFlashNumA/Endu/4/E12/", gf3],
            ["../Data/InAsFlashNumA/Endu/4/E13/", gf3],
            ["../Data/InAsFlashNumA/Endu/4/E9/", gf3]
        ]
    ]

## FlashNumA Endu
dataToPlot = [
        [
           ["%s1/E3/"%dataLoc, gf3],
           ["%s1/D1/"%dataLoc, gf3],
           ["%s1/D13/"%dataLoc, gf3],
           ["%s1/E1/"%dataLoc, gf3],
           ["%s1/E12/"%dataLoc, gf3],
           ["%s1/E2/"%dataLoc, gf3],
        ],
        [
           ["%s2/E1/"%dataLoc, gf3],
           ["%s2/C13/"%dataLoc, gf3],
           ["%s2/D1/"%dataLoc, gf3],
           ["%s2/D11/"%dataLoc, gf3],
           ["%s2/D12/"%dataLoc, gf3],
           ["%s2/D13/"%dataLoc, gf3],
           ["%s2/D2/"%dataLoc, gf3],
           ["%s2/E11/"%dataLoc, gf3],
           ["%s2/E12/"%dataLoc, gf3],
           ["%s2/E13/"%dataLoc, gf3],
           ["%s2/E2/"%dataLoc, gf3]
        ],
        [
           ["%s3/E1/"%dataLoc, gf3],
           ["%s3/C13/"%dataLoc, gf3],
           ["%s3/D1/"%dataLoc, gf3],
           ["%s3/D10/"%dataLoc, gf3],
           ["%s3/D9/"%dataLoc, gf3],
           ["%s3/E8/"%dataLoc, gf3]
        ],
        [
           ["../Data/InAsFlashNumC/Endu/4/D4/", gf3],
           ["../Data/InAsFlashNumC/Endu/4/D5/", gf3],
           ["../Data/InAsFlashNumC/Endu/4/D6/", gf3],
           ["../Data/InAsFlashNumC/Endu/4/E6/", gf3]
        ],
        [
            ["../Data/InAsFlashNumA/Endu/4/D11/", gf3],
            ["../Data/InAsFlashNumA/Endu/4/D12/", gf3],
            ["../Data/InAsFlashNumA/Endu/4/D13/", gf3],
            ["../Data/InAsFlashNumA/Endu/4/D9/", gf3],
            ["../Data/InAsFlashNumA/Endu/4/E11/", gf3],
            ["../Data/InAsFlashNumA/Endu/4/E12/", gf3],
            ["../Data/InAsFlashNumA/Endu/4/E13/", gf3],
            ["../Data/InAsFlashNumA/Endu/4/E9/", gf3]
        ]
    ]

## FlashIntE Endu
dataToPlot = [
        [
           ["%s1/E1/"%dataLoc, gf3],
           ["%s1/E2/"%dataLoc, gf3],
        ],
        [
           ["%s2/E13/"%dataLoc, gf3],
           ["%s2/E12/"%dataLoc, gf3]
        ],
        [
           ["%s3/D11/"%dataLoc, gf3]
        ],
        [
            ["../Data/InAsFlashNumA/Endu/4/D11/", gf3],
            ["../Data/InAsFlashNumA/Endu/4/D12/", gf3],
            ["../Data/InAsFlashNumA/Endu/4/D13/", gf3],
            ["../Data/InAsFlashNumA/Endu/4/D9/", gf3],
            ["../Data/InAsFlashNumA/Endu/4/E11/", gf3],
            ["../Data/InAsFlashNumA/Endu/4/E12/", gf3],
            ["../Data/InAsFlashNumA/Endu/4/E13/", gf3],
            ["../Data/InAsFlashNumA/Endu/4/E9/", gf3]
        ]
    ]

## FlashNumC Endu
dataToPlot = [
        [
           ["%s1/D5/"%dataLoc, gf3],
           ["%s1/E5/"%dataLoc, gf3]
        ],
        [
           ["%s2/D7/"%dataLoc, gf3],
           ["%s2/E7/"%dataLoc, gf3]
        ],
        [
           ["%s3/D4/"%dataLoc, gf3],
           ["%s3/D5/"%dataLoc, gf3],
           ["%s3/E5/"%dataLoc, gf3]
        ],
        [
            ["../Data/InAsFlashNumA/Endu/4/D11/", gf3],
            ["../Data/InAsFlashNumA/Endu/4/D12/", gf3],
            ["../Data/InAsFlashNumA/Endu/4/D13/", gf3],
            ["../Data/InAsFlashNumA/Endu/4/D9/", gf3],
            ["../Data/InAsFlashNumA/Endu/4/E11/", gf3],
            ["../Data/InAsFlashNumA/Endu/4/E12/", gf3],
            ["../Data/InAsFlashNumA/Endu/4/E13/", gf3],
            ["../Data/InAsFlashNumA/Endu/4/E9/", gf3]
        ]
    ]

## FlashNumD Endu
dataToPlot = [
        [
           ["../Data/InAsFlashIntE/Endu/3/D11/", gf3]
        ],
        [
           ["%s4/D12/"%dataLoc, gf3],
           ["%s4/D13/"%dataLoc, gf3],
           ["%s4/E12/"%dataLoc, gf3]
        ],
        [
           ["%s5/D1/"%dataLoc, gf3],
           ["%s5/D2/"%dataLoc, gf3],
           ["%s5/D3/"%dataLoc, gf3],
           ["%s5/D4/"%dataLoc, gf3],
           ["%s5/E2/"%dataLoc, gf3],
           ["%s5/E3/"%dataLoc, gf3]
        ],
        [
            ["../Data/InAsFlashNumA/Endu/4/D11/", gf3],
            ["../Data/InAsFlashNumA/Endu/4/D12/", gf3],
            ["../Data/InAsFlashNumA/Endu/4/D13/", gf3],
            ["../Data/InAsFlashNumA/Endu/4/D9/", gf3],
            ["../Data/InAsFlashNumA/Endu/4/E11/", gf3],
            ["../Data/InAsFlashNumA/Endu/4/E12/", gf3],
            ["../Data/InAsFlashNumA/Endu/4/E13/", gf3],
            ["../Data/InAsFlashNumA/Endu/4/E9/", gf3]
        ]
    ]

## FlashIntC UniCV
dataToPlot = [
        [
            ["%s3/C5/"%dataLoc, gf4],
            ["%s3/D5/"%dataLoc, gf4]
        ],
        [
            ["%s2/C10/"%dataLoc, gf4],
            ["%s2/D11/"%dataLoc, gf4],
            ["%s2/E11/"%dataLoc, gf4],
            ["%s2/E3/"%dataLoc, gf4],
        ],
        [
            ["%s1/C4/"%dataLoc, gf4],
            ["%s1/D13/"%dataLoc, gf4],
            ["%s1/D9/"%dataLoc, gf4],
            ["%s1/E3/"%dataLoc, gf4],
            ["%s1/E4/"%dataLoc, gf4],
            ["%s1/E9/"%dataLoc, gf4]
        ],
        [
            ["%s5/C11/"%dataLoc, gf4],
            ["%s5/D1/"%dataLoc, gf4],
            ["%s5/E10/"%dataLoc, gf4],
            ["%s5/E5/"%dataLoc, gf4]
        ],
        [
            ["../Data/InAsFlashNumA/UniCV/4/E1/", gf4],
            ["../Data/InAsFlashNumA/UniCV/4/E11/", gf4],
            ["../Data/InAsFlashNumA/UniCV/4/E12/", gf4]
        ]
    ]

## FlashNumA UniCV
dataToPlot = [
        [
            ["../Data/InAsFlashIntC/UniCV/2/C10/", gf4],
            ["../Data/InAsFlashIntC/UniCV/2/D11/", gf4],
            ["../Data/InAsFlashIntC/UniCV/2/E11/", gf4],
            ["../Data/InAsFlashIntC/UniCV/2/E3/", gf4]
        ],
        [
            ["%s2/C3/"%dataLoc, gf4],
            ["%s2/D3/"%dataLoc, gf4],
            ["%s2/E4/"%dataLoc, gf4]
        ],
        [
            ["%s3/D1/"%dataLoc, gf4],
            ["%s3/D2/"%dataLoc, gf4],
            ["%s3/E2/"%dataLoc, gf4]
        ],
        [
            ["../Data/InAsFlashNumC/UniCV/4/D2/", gf4],
            ["../Data/InAsFlashNumC/UniCV/4/D3/", gf4],
            ["../Data/InAsFlashNumC/UniCV/4/E2/", gf4]
        ],
        [
            ["%s4/E1/"%dataLoc, gf4],
            ["%s4/E11/"%dataLoc, gf4],
            ["%s4/E12/"%dataLoc, gf4]
        ]
    ]
"""
## FlashIntE UniCV
dataToPlot = [
        [
            ["%s1/C7/"%dataLoc, gf4],
            ["%s1/E5/"%dataLoc, gf4],
            ["%s1/E7/"%dataLoc, gf4],
            ["%s1/E8/"%dataLoc, gf4]
        ],
        [
            ["%s2/D2/"%dataLoc, gf4],
            ["%s2/E1/"%dataLoc, gf4],
            ["%s2/E2/"%dataLoc, gf4],
            ["%s2/F2/"%dataLoc, gf4]
        ],
        [
            ["%s3/C12/"%dataLoc, gf4],
            ["%s3/D12/"%dataLoc, gf4],
            ["%s3/E12/"%dataLoc, gf4]
        ],
        [
            ["../Data/InAsFlashNumA/UniCV/4/E1/", gf4],
            ["../Data/InAsFlashNumA/UniCV/4/E11/", gf4],
            ["../Data/InAsFlashNumA/UniCV/4/E12/", gf4]
        ]
    ]
"""
## FlashNumC UniCV
dataToPlot = [
        [
            ["../Data/InAsFlashIntC/UniCV/3/C5/", gf4],
            ["../Data/InAsFlashIntC/UniCV/3/D5/", gf4]
        ],
        [
            ["%s1/D2/"%dataLoc, gf4],
            ["%s1/E2/"%dataLoc, gf4],
            ["%s1/E3/"%dataLoc, gf4]
        ],
        [
            ["%s2/D2/"%dataLoc, gf4],
            ["%s2/D4/"%dataLoc, gf4],
            ["%s2/E2/"%dataLoc, gf4]
        ],
        [
            ["%s3/D2/"%dataLoc, gf4],
            ["%s3/D3/"%dataLoc, gf4],
            ["%s3/E2/"%dataLoc, gf4]
        ],
        [
            ["../Data/InAsFlashNumA/UniCV/4/E1/", gf4],
            ["../Data/InAsFlashNumA/UniCV/4/E11/", gf4],
            ["../Data/InAsFlashNumA/UniCV/4/E12/", gf4]
        ]
    ]

## FlashNumD UniCV
dataToPlot = [
        [
            ["../Data/InAsFlashIntE/UniCV/3/C12/", gf4],
            ["../Data/InAsFlashIntE/UniCV/3/D12/", gf4],
            ["../Data/InAsFlashIntE/UniCV/3/E12/", gf4]
        ],
        [
            ["%s4/C2/"%dataLoc, gf4],
            ["%s4/D1/"%dataLoc, gf4],
            ["%s4/D2/"%dataLoc, gf4]
        ],
        [
            ["%s5/D1/"%dataLoc, gf4],
            ["%s5/D2/"%dataLoc, gf4],
            ["%s5/E1/"%dataLoc, gf4]
        ],
        [
            ["../Data/InAsFlashNumA/UniCV/4/E1/", gf4],
            ["../Data/InAsFlashNumA/UniCV/4/E11/", gf4],
            ["../Data/InAsFlashNumA/UniCV/4/E12/", gf4]
        ]
    ]
"""

#PUNDPlotter.PUNDTrend(dataToPlot, '', ['ALD 200C'], xlabel = 'Flash Intensity [J/cm²]')
#EnduPlotter.PlotEndu(dataToPlot, ['30 J/cm²', '25 J/cm²', '20 J/cm²', 'RTP Reference'])
UniCVPlotter.PlotDDGroup(dataToPlot, '', ['30 J/cm²', '25 J/cm²', '20 J/cm²', 'RTP Reference'])

#plt.tight_layout()
plt.show()
