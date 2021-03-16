#!/bin/bash

usage(){
    echo -e "To call EnduClean please use:"
    echo -e "$0 <DataDir Path> <Destination Path>"
    echo -e "-----"
}

OIFS="$IFS"
IFS=$'\n'
FILEPATHS=$(find $1 -type f -name 'Endurance Measure*')
DATADEST=${2}Endu

if [[ "x$DATADEST" == "x" ]]; then
    DATADEST=./
fi

if [[ "x$FILEPATHS" == "x" ]]; then
    echo "No files were found in the DataDir Path. Exiting."
    usage
    exit 1
fi

for FILEPATH0 in $FILEPATHS; do

    if [[ "x$FILEPATH0" == "x" ]]; then
        echo "Error in file listing. Exiting."
        usage
        exit 1
    fi

    echo "Removing spaces in file name."
    cp -a "$FILEPATH0" `echo $FILEPATH0 | sed 's/\([[:digit:]]\) 0/\10/g' | tr ' ' '_'`
    FILEPATH=`echo $FILEPATH0 | sed 's/\([[:digit:]]\) 0/\10/g' | tr ' ' '_'`

    FILENAME=$(basename "$FILEPATH")
    DATALOC=$(dirname "$FILEPATH")

    echo "Copying input file $FILEPATH to $DATALOC/temp_$FILENAME"
    cp -a $FILEPATH $DATALOC/temp_$FILENAME

    echo "Finding first line containing 'DataName'..."
    STARTLINE=$(grep -n "DataName" $DATALOC/temp_$FILENAME | cut -f1 -d: | head -n 1)

    if [[ "x$STARTLINE" == "x" ]]; then
        echo "No line containing 'DataName' was found. Skipping file."
        rm -r $DATALOC/temp_$FILENAME
        continue
    fi

    STARTLINE=$(( $STARTLINE + 1 ))

    echo "Removing the first $STARTLINE lines."
    tail -n +$STARTLINE $DATALOC/temp_$FILENAME > $DATALOC/temp_$FILENAME.tmp
    mv $DATALOC/temp_$FILENAME.tmp $DATALOC/temp_$FILENAME

    echo "Finding first line containing 'SetupTitle, WGFMU'..."
    ENDLINE=$(grep -n "SetupTitle, WGFMU" $DATALOC/temp_$FILENAME | cut -f1 -d:)

    if [[ "x$ENDLINE" == "x" ]]; then
        echo "No line containing 'SetupTitle, WGFMU' was found. Skipping file."
        rm -r $DATALOC/temp_$FILENAME
        continue
    fi

    echo "Removing all lines after line $ENDLINE."
    END=$(wc -l $DATALOC/temp_$FILENAME | cut -f1 -d' ')
    ENDLINE=$(( $END - $ENDLINE + 2 ))
    head -n -$ENDLINE $DATALOC/temp_$FILENAME > $DATALOC/temp_$FILENAME.tmp
    mv $DATALOC/temp_$FILENAME.tmp $DATALOC/temp_$FILENAME

    SAMPLENUM=$(echo $FILENAME | cut -f 8 -d'_')
    CONDENNUM=$(echo $FILENAME | cut -f 10 -d'_' | sed 's/([^)]*)//g')

    NEWFILENAME=$(echo $FILENAME | cut -f 1,3,5-10 -d'_' | sed 's/[][]//g' | sed 's/([^)]*)//g')

    mkdir -p $DATADEST/$SAMPLENUM/$CONDENNUM

    echo "Removing spaces in data. Resulting file in $DATADEST/$SAMPLENUM/$CONDENNUM/${NEWFILENAME}.csv"
    sed 's/ //g' $DATALOC/temp_$FILENAME > $DATADEST/$SAMPLENUM/$CONDENNUM/$NEWFILENAME.csv

    echo "Removing temporary files."
    rm -r $DATALOC/temp_$FILENAME $FILEPATH
    echo "Done."
done
