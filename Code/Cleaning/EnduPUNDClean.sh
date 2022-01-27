#/bin/bash

usage(){
    echo -e "To call EnduClean please use:"
    echo -e "$0 <DataDir Path> <Destination Path>"
    echo -e "-----"
}

OIFS="$IFS"
IFS=$'\n'
FILEPATHS=$(find $1 -type f -name 'Flash*')
DATADEST=${2}Endu

if [[ "x$DATADEST" == "x" ]]; then
    DATADEST=./
fi

if [[ "x$FILEPATHS" == "x" ]]; then
    echo "No files were found in the DataDir Path. Exiting."
    usage
    exit 1
fi

TOTFILES=$(find $1 -type f -name 'Flash*' | wc -l)
NUMFILES=$((0))
echo "Found $TOTFILES matching files. Cleaning data.."
for FILEPATH0 in $FILEPATHS; do

    if [[ "x$FILEPATH0" == "x" ]]; then
        echo "Error in file listing. Exiting."
        usage
        exit 1
    fi
    
    FILENAME=$(basename "$FILEPATH0")
    DATALOC=$(dirname "$FILEPATH0")

    cp -a $FILEPATH0 $DATALOC/temp_$FILENAME

    MAXVOLTAGE=$(cut -f 2 -d',' $DATALOC/temp_$FILENAME | sort -n | tail -1 | awk '{printf "%.1f", $1}')

    SAMPLENUM=$(echo $FILENAME | cut -f 2 -d'_')
    CONDENNUM=$(echo $FILENAME | cut -f 3 -d'_')

    NEWFILENAME1=$(echo $FILENAME | cut -f 2 -d'=' | sed 's/.csv//g') 
    NEWFILENAME2=$(echo $FILENAME | cut -f 1-2,4 -d'_')
    NEWFILENAME3=$(echo $FILENAME | cut -f 3 -d'_')
    NEWFILENAME=$(echo "EnduranceP_${MAXVOLTAGE}V_10kHz_${NEWFILENAME1}_Cycles_${NEWFILENAME2}_${NEWFILENAME3}")

    mkdir -p $DATADEST/$SAMPLENUM/$CONDENNUM

    #echo "Removing spaces in data. Resulting file in $DATADEST/$SAMPLENUM/$CONDENNUM/${NEWFILENAME}.csv"
    sed 's/ //g' $DATALOC/temp_$FILENAME > $DATADEST/$SAMPLENUM/$CONDENNUM/$NEWFILENAME.csv

    rm -r $DATALOC/temp_$FILENAME
    #echo "Done."
    NUMFILES=$((NUMFILES + 1))
    echo "$NUMFILES / $TOTFILES files cleaned."

done

