#!/usr/bin/env python

import argparse
import pathlib
import tkinter as tk
from tkinter import filedialog

from enum import Enum
from typing import Any, Literal

import feplot.pyro as pyro
import feplot.pund as pund

from feplot import __version__

class Datatype(Enum):
    """
    Enum specifying the different available datatypes to process.
    """
    PUND = 'pund'
    ENDU = 'endu'
    UNICV = 'unicv'
    BICV = 'bicv'
    PYRO = 'pyro'

    def __init__(self, type: str) -> None:
        self.type = type

    @classmethod
    def valuelist(cls) -> list[str]:
        """
        Returns the values of the Datatype members.
        """
        return [member.value for _, member in cls.__members__.items()]

    def run(self) -> None:
        """
        Gets data files and runs function based on the Datatype.
        """
        paths: tuple[str, ...] | Literal[''] = self.select_file()
        plotparams = {'raw': True,} # Plot everything by default for dev purposes

        if self.type == Datatype.PUND.value:
            pund.main(paths, plotparams)
        elif self.type == Datatype.ENDU.value:
            print(f"{self}")
        elif self.type == Datatype.UNICV.value:
            print(f"{self}")
        elif self.type == Datatype.BICV.value:
            print(f"{self}")
        elif self.type == Datatype.PYRO.value:
            pyro.main(paths)
        else:
            raise ValueError(f"The selected datatype is not defined.")

    def select_file(self) -> tuple[str, ...] | Literal['']:
        tk.Tk().withdraw()
        paths = filedialog.askopenfilenames(
                initialdir=".", 
                title=f"{self.type} file selector", 
                filetypes=((".dat files", "*.dat"), (".csv files", "*.csv"))
                )

        return paths

def get_parser() -> argparse.ArgumentParser:
    """
    Initiate argument parser with specified paramenters and return parser with
    arguments for said paramenters.
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('type',
            help='specify type of data to process',
            nargs='?',
            choices=Datatype.valuelist())
    parser.add_argument('-v', '--version', 
            help='display the current version of FePlot', 
            action='store_true')
    parser.add_argument('-c', '--clean',
            help='initiate cleaning of data at DATA_PATH before plotting',
            dest='clean_path',
            nargs=1,
            type=pathlib.Path,
            metavar='DATA_PATH')

    return parser

def user_args(uargs: dict[str, Any]) -> None:
    """
    Do different thing depending on the input dictionary.
    Dictionary should come from parser.parse_args().
    """
    if uargs['version']:
        print(__version__)
        return

    # This is yet to be implemented!
    if uargs['clean_path']:
        print(f"Cleaning data in {uargs['clean_path']}!")

    # if the positional argument is omitted/invalid - raise a ValueError
    if uargs['type'] not in Datatype.valuelist():  
        raise ValueError(
            f"You forgot to add the positional argument of 'type'.\n\
            Please see: feplot --help"
            )
    else:
        Datatype(uargs['type']).run()


def main() -> None:
    parser = get_parser()

    #convert args to dict and pass to user_args
    user_args(vars(parser.parse_args()))


if __name__ == '__main__':
    main()
