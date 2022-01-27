#!/bin/bash

usage(){
    echo -e "To call PyroClean please use:"
    echo -e "$0 <File Path> <Destination Path>"
    echo -e "-----"
}

FILEPATH=$1
DATADEST=$2Pyro
mkdir $DATADEST

if [[ "x$DATADEST" == "x" ]]; then
    DATADEST=.
fi

if [[ "x$FILEPATH" == "x" ]]; then
    echo "Missing input file parameter. Exiting."
    usage
fi

FILENAME=$(basename "$FILEPATH")
DATALOC=$(dirname "$FILEPATH")

echo "Copying input file $FILEPATH to $DATALOC/temp_$FILENAME"
cp -a $FILEPATH $DATALOC/temp_$FILENAME

echo "Finding first line containing 'MeasurementTrigger:'..."
STARTLINE=$(grep -n "MeasurementTrigger:" $DATALOC/temp_$FILENAME | cut -f1 -d: | head -n 1)

if [[ "x$STARTLINE" == "x" ]]; then
    echo "No line containing 'MeasurementTrigger:' was found. Exiting."
    rm -r $DATALOC/temp_$FILENAME
    exit 1
fi

STARTLINE=$(( $STARTLINE + 2 ))

echo "Removing the first $STARTLINE lines."
tail -n +$STARTLINE $DATALOC/temp_$FILENAME > $DATALOC/temp_$FILENAME.tmp
mv $DATALOC/temp_$FILENAME.tmp $DATALOC/temp_$FILENAME

echo "Finding first line containing 'End of File'..."
ENDLINE=$(grep -n "End of File" $DATALOC/temp_$FILENAME | cut -f1 -d:)

if [[ "x$ENDLINE" == "x" ]]; then
    echo "No line containing 'End of File' was found. Exiting."
    rm -r $DATALOC/temp_$FILENAME
    exit 1
fi

ENDLINE=$(( $ENDLINE - 2 ))
echo "Removing all lines after line $ENDLINE."
END=$(wc -l $DATALOC/temp_$FILENAME | cut -f1 -d' ')
head -n -$(( $END - $ENDLINE )) $DATALOC/temp_$FILENAME > $DATALOC/temp_$FILENAME.tmp

echo "Replacing ',' with '.' and '/t' with ','."
sed -e 's/,/./g' -e 's/[[:space:]]/,/g' $DATALOC/temp_$FILENAME.tmp > $DATALOC/temp_$FILENAME

echo "Cleaning up Time data. Resulting file in $DATADEST/Pyro_$FILENAME"
awk -F'[:,]' '{printf $1 * 60 * 60 + $2 * 60 + $3","; for (i=4; i<=NF; i++) printf $i","; print $NF}' $DATALOC/temp_$FILENAME > $DATADEST/Pyro_$FILENAME

echo "Removing temporary files."
rm -r $DATALOC/temp_$FILENAME $DATALOC/*.tmp
echo "Done."
