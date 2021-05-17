#!/usr/bin/env python

import os
import matplotlib.pyplot as plt
import CapacitancePlot

fig = plt.figure(figsize = (10,6))
ax1 = fig.add_subplot(111)

CapacitancePlot("../Data/InAsFlashIntC/CV/1/D1/")

