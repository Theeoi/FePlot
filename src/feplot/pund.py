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

def main(paths: tuple[str, ...]) -> None:

    for path in paths:
        pund_data: tuple[list[float], ...] = get_data(path) 
