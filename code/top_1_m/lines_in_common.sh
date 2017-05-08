#!/bin/bash

USAGE="usage: $0 [-p] file1 file2"
PRINT_COMMON=false

if [[ $# -lt 2 || $# -gt 3 ]]; then
    echo $USAGE
    exit 1
fi

if [[ $# -eq 3 ]]; then
    if [[ "$1" == "-p" ]]; then
        PRINT_COMMON=true
        shift
    else
        echo $USAGE
        exit 1
    fi
fi

if [[ ! -f "$1" || ! -f "$2" ]]; then
    echo "Error: inputs must be regular files"
    echo $USAGE
    exit 1
fi

L1=$(wc -l "$1" | awk '{print $1}')
L2=$(wc -l "$2" | awk '{print $1}')
if [[ $(( $L1 * $L2 )) -gt $(( 10 ** 13 )) ]]; then
    echo "Warning: input file size very large, memory exhaustion risk."
    read -r -p "         Continue (y/n)?" choice
    if [[ ! $choice =~ (y|Y|yes) ]]; then
        exit 0
    fi
fi

XOR=0
grep -qU $'\015' $1 || let "XOR+=1"
grep -qU $'\015' $2 || let "XOR+=1"
if [[ $((XOR % 2)) == 1 ]]; then
    echo "Warning: detected mixed LF and CRLF. (Use dos2unix.)"
fi

if [[ $PRINT_COMMON == false ]]; then
    LINES=$(awk 'a[$0]++' $1 $2 | wc -l)
    echo "Number of lines: " $LINES
else
    awk 'a[$0]++' $1 $2
fi

