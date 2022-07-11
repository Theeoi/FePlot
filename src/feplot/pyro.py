#!/usr/bin/python
import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt

from typing import Literal

def select_file() -> tuple[str, ...] | Literal['']:
    tk.Tk().withdraw()
    paths = filedialog.askopenfilenames(
            initialdir=".", 
            title="PYRO File Selector", 
            filetypes=((".dat files", "*.dat"),))

    return paths

def get_data(path: str) -> tuple[list[float], ...]:
    data = ([], [])
    with open(path, 'r') as file:
        for line in file.readlines():
            data[0].append(float(line.split(",")[0]))
            data[1].append(float(line.split(",")[1]))

    return data

def get_max_temp(temp: list[float]) -> float:
    return round(np.max(temp), 2)

def get_pyro_figure() -> plt.Axes:
    fig = plt.figure(figsize = (9,6))
    ax = fig.add_subplot(111)

    ax.tick_params('both', labelsize = "x-large")

    ax.set_xlabel("Time [s]", fontsize = "xx-large")
    ax.set_ylabel("Temperature [\N{DEGREE SIGN}C]", fontsize = "xx-large")

    return ax

def main() -> None:
    paths: tuple[str, ...] | Literal[''] = select_file()

    for path in paths:
        pyro_data: tuple[list[float], ...] = get_data(path)

        Tpeak: float = get_max_temp(pyro_data[1])

        ax: plt.Axes = get_pyro_figure()

        ax.plot(pyro_data[0], pyro_data[1], 
                label = "Pyrometer Temperature",
                color = "r")
        ax.text(0.1,0.85,'$T_{peak}$ = %s \N{DEGREE SIGN}C' %Tpeak, 
                fontsize = "xx-large",
                transform=ax.transAxes)

    plt.show()

if __name__ == '__main__':
    main()
