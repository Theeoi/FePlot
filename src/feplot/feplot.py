#!/usr/bin/env python

import argparse
import os
import readline
import glob
import inquirer

from feplot import __version__

def prompt_choice(name: str, question: str, choice: list[str]) -> str:
    q = [inquirer.List(name, message=question, choices=choice),]

    return inquirer.prompt(q)[name]

def prompt_mchoice(name: str, question: str, choice: list[str]) -> list[str]:
    q = [inquirer.Checkbox(name, message=question, choices=choice),]

    return inquirer.prompt(q)[name]

def pathCompleter(text: str, state: int) -> str:
    """ 
    Function for generating the path autocomplete.  
    """

    if '~' in text:
        text = os.path.expanduser('~')

    if os.path.isdir(text):
        text += "/"

    return [x for x in glob.glob(text+'*')][state]

def get_dataloc() -> str:
    """
    Get a valid path from user with tab autocomplete feature.
    """

    readline.set_completer_delims("\t")
    readline.parse_and_bind("tab: complete")
    readline.set_completer(pathCompleter)

    while True:
        data_loc: str = str(input("Enter data path: "))
        if not os.path.isdir(data_loc): 
           print(f"The entered path '{data_loc}' does not exist. Please try again.") 
           continue
        else:
            return data_loc

def get_parser():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-v', '--version', help='display the current version of\
            FePlot', action='store_true')

    return parser


def main() -> None:
    parser = get_parser()
    args = vars(parser.parse_args())

    if args['version']:
        print(__version__)
        return

    question = "What type of data would you like to process?"
    choices = ["PUND", "Endu", "UniCV"]
    data_type: str = prompt_choice('type', question, choices)

    data_loc: str = get_dataloc()
    question = "Which sample series are to be included?"
    choices = list(filter(lambda x: os.path.isdir(os.path.join(data_loc, x)), os.listdir(data_loc)))
    data_series: list[str] = prompt_mchoice('series', question, choices)
    for dir in data_series:
        question = f"Which samples are to be included from {dir}?"
        choices = list(filter(lambda x: os.path.isdir(os.path.join(data_loc,
            dir, x)), os.listdir(os.path.join(data_loc, dir))))
        data_samples: list[str] = prompt_mchoice(f'{dir}_samples', question,
                choices)

if __name__ == '__main__':
    main()
