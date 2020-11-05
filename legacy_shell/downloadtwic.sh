#!/bin/bash

usage () {
  echo "Usage: $0 <firstTWIC> <lastTWIC>" 1>&2
}

limits () {
  echo "Use numbers between 400 and $1" 1>&2
}

i=$1 ; test -z "$i" && {
  usage
  exit 1
}

f=$2 ; test -z "$f" && {
  usage
  exit 1
}

# TWICs are available from 211 to x
# Lets calculate the upper limit
ly=790
x=`date +%U`
let "x = x + ly"

[ $i -lt 211 ] && {
  limits $x
  exit 1
}

[ $f -gt $x ] && {
  limits $x
  exit 1
}

# Compose the link
prelink="http://www.chess.co.uk/twic/zips/twic"
poslink="g.zip"
# Iterate through downloadable TWICs
while [ $i -le $f ]
do
  link=${prelink}${i}${poslink}
  # Get it!
  wget $link
  let "i = i + 1"
done
exit 0
