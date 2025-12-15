#!/bin/bash

# Ask for two numbers.
echo "Enter first number."
read a
echo "Enter second number."
read b

# Make sure something gets typed for each.
if [ -z "$a" ] || [ -z "$b" ];
then
    echo "Error: please enter two numbers."
    exit 1
fi

# Compare using the awk command.
compared=$(awk -v a="$a" -v b="$b" 'BEGIN{
if (a < b) print "less_than";
else if (a > b) print "greater_than";
else print "equal";
}')

# Show the higher number as the output.
if [ "$compared" = "less_than" ]; then
    echo "$b is the higher number."
elif [ "$compared" = "$greater_than" ]; then
    echo "$a is the higher number."
else
    echo "Both numbers ($a) are equal."
fi