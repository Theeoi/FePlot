#!/usr/bin/env python

import os
import matplotlib.pyplot as plt


def get_data(path: str) -> dict[str, list[float]]:
    data = {"time": [], "current": [], "voltage": []}
    with open(path, 'r') as file:
        for line in file.readlines():
            data["time"].append(float(line.split(",")[1]))
            data["current"].append(float(line.split(",")[2]))
            data["voltage"].append(float(line.split(",")[3]))

    return data

def get_sampleid(path: str) -> str:
    basename: str = os.path.basename(path)

    batch: str = basename.split("_")[2]
    snum: str = basename.split("_")[3]
    cid: str = basename.split("_")[5].replace('.csv', '')

    return f"{batch}-{snum}-{cid}"

def plot_pund(sampleid: str, pund_data: dict[str, list[float]]) -> None:
    fig, ax1 = plt.subplots(figsize = (5,4))
    ax2 = ax1.twinx()

    plt.title(sampleid, fontsize = '10')
    ax1.tick_params('both', labelsize = '16')
    ax2.tick_params('both', labelsize = '16')

    ax1.set_xlabel("Time [ms]", fontsize = '20')
    ax1.set_ylabel("Current [$\mu$A]", fontsize = '20')
    ax2.set_ylabel("Voltage [V]", fontsize = '20')
    
    ax1.plot([t * 10**3 for t in pund_data["time"]], 
            [c * 10**6 for c in pund_data["current"]], 
            label = "Current", 
            color = 'b')

    ax2.plot([t * 10**3 for t in pund_data["time"]], 
            pund_data["voltage"], 
            label = "Voltage", 
            color = 'c')

    fig.legend(fontsize = '16', 
            loc = 4, 
            bbox_to_anchor = (1,0), 
            bbox_transform = ax1.transAxes)


def main(paths: tuple[str, ...], plotparams: dict[str, bool]) -> None:

    for path in paths:
        sampleid: str = get_sampleid(path)

        pund_data: dict[list[float]] = get_data(path)

        if (plotparams['raw']):
            plot_pund(sampleid, pund_data)

    plt.tight_layout()
    plt.show()
