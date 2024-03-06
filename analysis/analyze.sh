#!/bin/bash

FILENAME=$1

if [ ! -f "$FILENAME" ]; then
	echo "$FILENAME: no such file, pass a valid input file as a first argument." 	
	exit 1
fi

TESTCASE_SPLIT_PATTERN="Running testcase Cycle:"

csplit -sk "$FILENAME" "/$TESTCASE_SPLIT_PATTERN/" {*}

TESTCASE_FILES=($(ls xx* | sort -V))

for ((i=0; i<${#TESTCASE_FILES[@]}; i++)); do
    #do something to each element of array
    TESTCASE_FILE="${TESTCASE_FILES[$i]}"
    CYCLE="$(grep --binary-files=text "$TESTCASE_SPLIT_PATTERN" $TESTCASE_FILE |  sed -E -n "s/^.*Cycle: ([0-9]*); Test ([0-9]*).../\1/p")"
    TEST_NO="$(grep --binary-files=text "$TESTCASE_SPLIT_PATTERN" $TESTCASE_FILE |  sed -E -n "s/^.*Cycle: ([0-9]*); Test ([0-9]*).../\2/p")"
    #echo "CYCLE: $CYCLE, TEST_NO: $TEST_NO"
    grep --binary-files=text "BATCH [0-9]* SUMMARY" $TESTCASE_FILE | sed -E 's/\[([0-9]*)\]: <info> app: \[BATCH ([0-9]*) SUMMARY\]: ESPAR CHAR: ([0-9]*), BPER: ([0-9]*\.[0-9]*), RSSI: (-?[0-9]*\.[0-9]*)/\1;\2;\3;\4;\5/' > "data_cycle_${CYCLE}_TEST_${TEST_NO}.csv"
#    echo "TESTCASE $i file: $TESTCASE_FILE"
#    cat $TESTCASE_FILE | sed -n -e '/Starting espar.../,$p;/Testcase passed./q'
done

