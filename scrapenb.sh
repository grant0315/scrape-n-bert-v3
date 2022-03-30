#!/bin/bash

helpFunction()
{
    echo ""
    echo "Usage: $0 -c config file"
}

while getopts "c:h" opt
do
    case "$opt" in
        c ) config_file="$OPTARG" ;;
        h ) helpFunction ;;
        ? ) helpfunction ;;
    esac
done

# Print helpFunction if parameters is missing
if [ -z "$config_file"]
then
    echo "Some or all parameters are empty";
    helpFunction
else # Actual meat of the bash file
    # Print config file path
    echo "$config_file"

    # Run spider from config file
    python3 config_parser.py config_file
fi