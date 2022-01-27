#!/bin/bash

usage(){
    echo -e "To call CVClean please use:"
    echo -e "$0 <DataDir Path> <Destination Path>"
    echo -e "-----"
}

OIFS="$IFS"
IFS=$'\n'
FILEPATHS=$(find $1 -type f -name 'UniCV_*')
DATADEST=${2}UniCV

if [[ "x$DATADEST" == "x" ]]; then
    DATADEST=./
fi

if [[ "x$FILEPATHS" == "x" ]]; then
    echo "No files were found in the DataDir Path. Exiting."
    usage
    exit 1
fi

TOTFILES=$(find $1 -type f -name 'UniCV_*' | wc -l)
NUMFILES=$((0))
echo "Found $TOTFILES matching files. Cleaning data.."
for FILEPATH0 in $FILEPATHS; do

    if [[ "x$FILEPATH0" == "x" ]]; then
        echo "Error in file listing. Exiting."
        usage
        exit 1
    fi

    #echo "Removing spaces in file name."
    cp -a "$FILEPATH0" `echo $FILEPATH0 | sed 's/0.00f/f/g' | tr ' ' '_'`
    FILEPATH=`echo $FILEPATH0 | sed 's/0.00f/f/g' | tr ' ' '_'`

    FILENAME=$(basename "$FILEPATH")
    DATALOC=$(dirname "$FILEPATH")

    #echo "Copying input file $FILEPATH to $DATALOC/temp_$FILENAME"
    cp -a $FILEPATH $DATALOC/temp_$FILENAME

    #echo "Finding first line containing 'Real'..."
    STARTLINE=$(grep -n "Real" $DATALOC/temp_$FILENAME | cut -f1 -d: | head -n 1)

    if [[ "x$STARTLINE" == "x" ]]; then
        echo "No line containing 'Real' was found. Skipping file."
        rm -r $DATALOC/temp_$FILENAME
        continue
    fi

    STARTLINE=$(( $STARTLINE + 1 ))

    #echo "Removing the first $STARTLINE lines."
    tail -n +$STARTLINE $DATALOC/temp_$FILENAME > $DATALOC/temp_$FILENAME.tmp
    mv $DATALOC/temp_$FILENAME.tmp $DATALOC/temp_$FILENAME

    SAMPLENUM=$(echo $FILENAME | cut -f 4 -d'_')
    CONDENNUM=$(echo $FILENAME | cut -f 5 -d'_')

    NEWFILENAME=$(echo $FILENAME | cut -f 1-8 -d'_' | sed 's/\([[:digit:]]V\?\)t/\1/g' | sed 's/_NaNV//g' ) 

    mkdir -p $DATADEST/$SAMPLENUM/$CONDENNUM

    #echo "Replacing delimiter with commas in data. Resulting file in $DATADEST/$SAMPLENUM/$CONDENNUM/${NEWFILENAME}.csv"
    sed 's/\t/,/g' $DATALOC/temp_$FILENAME > $DATADEST/$SAMPLENUM/$CONDENNUM/$NEWFILENAME.csv

    #echo "Removing temporary files."
    rm -r $DATALOC/temp_$FILENAME $FILEPATH
    NUMFILES=$((NUMFILES + 1))
    echo "$NUMFILES / $TOTFILES files cleaned."
done
