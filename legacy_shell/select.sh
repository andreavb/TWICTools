#!/bin/bash
# Author: Andrea Vidigal Bucci
# Date: Apr 07 2010
# Version: 1.0

usage () {
echo "Usage: $0 <firstTWIC> <lastTWIC> <opening>" 1>&2
}

i=$1 ; test -z "$i" && {
  usage
  exit 1
}

f=$2 ; test -z "$f" && {
  usage
  exit 1
}

opening=$3 ; test -z "$opening" && {
  usage
  exit 1
}

# The format of the file is twicXXX.pgn
# You can change the lines below to use your own formats
prelink="twic"
poslink=".pgn"
# Iterate through the files $i to $f
while [ $i -le $f ]
do
  # We get the name of the file
  link=${prelink}${i}${poslink}
  # Does the file exist?
  # Let's just ignore it if it doesn't...
  if [ -e $link ] ; then
    # And select the interesting games!
    awk '/\[Event \"/{ i++; } { print >> "split_" i;}' $link
    # Moving them to a single file
    cat $(grep -lF "${opening}" split_*) >> interestinggames.pgn
    # Let's clean up the environment
    rm split*
  fi
  let "i = i + 1"
done
exit 0
