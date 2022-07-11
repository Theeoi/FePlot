#!/usr/bin/env python

def get_data(path: str) -> tuple[list[float], ...]:
    data = ([], [], [])
    with open(path, 'r') as file:
        for line in file.readlines():
            data[0].append(float(line.split(",")[1]))
            data[1].append(float(line.split(",")[2]))
            data[2].append(float(line.split(",")[3]))

    return data

def main(paths: tuple[str, ...]) -> None:

    for path in paths:
        pund_data: tuple[list[float], ...] = get_data(path) 
