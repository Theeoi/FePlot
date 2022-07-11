#!/bin/bash

usage(){
    echo -e "To call EnduranceClean please use:"
    echo -e "$0 <File Path> <Destination Path>"
    echo -e "-----"
}

FILEPATH0=$1
DATADEST=$2/Endu

if [[ "x$DATADEST" == "x" ]]; then
    DATADEST=.
fi

if [[ "x$FILEPATH0" == "x" ]]; then
    echo "Missing input file parameter. Exiting."
    usage
fi

echo "Removing spaces in file name."
cp -a "$FILEPATH0" `echo $FILEPATH0 | sed 's/0 0/00/g' | tr ' ' '_'`
FILEPATH=`echo $FILEPATH0 | sed 's/0 0/00/g' | tr ' ' '_'`

FILENAME=$(basename "$FILEPATH")
DATALOC=$(dirname "$FILEPATH")

echo "Copying input file $FILEPATH to $DATALOC/temp_$FILENAME"
cp -a $FILEPATH $DATALOC/temp_$FILENAME

echo "Finding first line containing 'DataName'..."
STARTLINE=$(grep -n "DataName" $DATALOC/temp_$FILENAME | cut -f1 -d: | head -n 1)

if [[ "x$STARTLINE" == "x" ]]; then
    echo "No line containing 'DataName' was found. Exiting."
    rm -r $DATALOC/temp_$FILENAME
    exit 1
fi

STARTLINE=$(( $STARTLINE + 1 ))

echo "Removing the first $STARTLINE lines."
tail -n +$STARTLINE $DATALOC/temp_$FILENAME > $DATALOC/temp_$FILENAME.tmp
mv $DATALOC/temp_$FILENAME.tmp $DATALOC/temp_$FILENAME

echo "Finding first line containing 'SetupTitle, WGFMU'..."
ENDLINE=$(grep -n "SetupTitle, WGFMU" $DATALOC/temp_$FILENAME | cut -f1 -d:)

if [[ "x$ENDLINE" == "x" ]]; then
    echo "No line containing 'SetupTitle, WGFMU' was found. Exiting."
    rm -r $DATALOC/temp_$FILENAME
    exit 1
fi

echo "Removing all lines after line $ENDLINE."
END=$(wc -l $DATALOC/temp_$FILENAME | cut -f1 -d' ')
ENDLINE=$(( $END - $ENDLINE + 2 ))
head -n -$ENDLINE $DATALOC/temp_$FILENAME > $DATALOC/temp_$FILENAME.tmp
mv $DATALOC/temp_$FILENAME.tmp $DATALOC/temp_$FILENAME

MAXVOLTAGE=$(cut -f 4 -d',' $DATALOC/temp_$FILENAME | sort -n | tail -1 | awk '{printf "%.1f", $1}')

NEWFILENAME1=$(echo $FILENAME | cut -f 1 -d'_') 
NEWFILENAME2=$(echo $FILENAME | cut -f 3,5-10 -d'_')
NEWFILENAME=$(echo "${NEWFILENAME1}_${MAXVOLTAGE}V_${NEWFILENAME2}" | sed 's/[][]//g' | sed 's/([^)]*)//g')

echo "Removing spaces in data. Resulting file in $DATADEST/${NEWFILENAME}.csv"
sed 's/ //g' $DATALOC/temp_$FILENAME > $DATADEST/$NEWFILENAME.csv

echo "Removing temporary files."
rm -r $DATALOC/temp_$FILENAME $FILEPATH
echo "Done."
