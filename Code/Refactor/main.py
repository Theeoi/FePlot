#!/usr/bin/env python

import os
import readline
import glob

def pathCompleter(text: str, state: int) -> str:
    """
    Function for generating the path autocomplete.
    """

    if '~' in text:
        text = os.path.expanduser('~')

    if os.path.isdir(text):
        text += "/"

    return [x for x in glob.glob(text+'*')][state]

def get_dataLoc() -> str:
    """
    Get a valid path from user with tab autocomplete feature.
    """

    readline.set_completer_delims("\t")
    readline.parse_and_bind("tab: complete")
    readline.set_completer(pathCompleter)

    while True:
        dataLoc: str = str(input("Enter data path: "))
        if not os.path.isdir(dataLoc): 
           print(f"The entered path '{dataLoc}' does not exist. Please try again.") 
           continue
        else:
            return dataLoc

def main() -> None:
    dataLoc: str = get_dataLoc()
    print(dataLoc)

if __name__ == '__main__':
    main()
