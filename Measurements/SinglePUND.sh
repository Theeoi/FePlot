#!/bin/bash

usage(){
    echo -e "To call PUNDClean please use:"
    echo -e "$0 <File Path> <Destination Path>"
    echo -e "-----"
}

FILEPATH0=$1
DATADEST=$2

if [[ "x$DATADEST" == "x" ]]; then
    DATADEST=.
fi

if [[ "x$FILEPATH0" == "x" ]]; then
    echo "Missing input file parameter. Exiting."
    usage
fi

echo "Removing spaces in file name."
cp -a "$FILEPATH0" `echo $FILEPATH0 | tr ' ' '_'`
FILEPATH=`echo $FILEPATH0 | tr ' ' '_'`

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

##NEWFILENAME=$(echo $FILENAME | cut -f 2-3,6-9 -d'_' | sed 's/[][]//g' | sed 's/([^)]*)//g')

echo "Removing spaces in data. Resulting file in $DATADEST/$FILENAME"
sed 's/ //g' $DATALOC/temp_$FILENAME > $DATADEST/$FILENAME

echo "Removing temporary files."
rm -r $DATALOC/temp_$FILENAME $FILEPATH
echo "Done."
