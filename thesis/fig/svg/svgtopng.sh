#!/bin/bash

find -name "*.svg" -exec sh -c 'inkscape $1 --export-png=../${1%.svg}.png' _ {} \; 2> /dev/null
