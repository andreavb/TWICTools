#!/bin/bash

usage () {
  echo "Usage: $0" 1>&2
}

# Last of 2009
ly=790

# We need to know how many weeks has passed since the year has started
i=`date +%U`
# We compose the link
let "i = i + ly"
prelink="http://www.chess.co.uk/twic/zips/twic"
poslink="g.zip"
link=${prelink}${i}${poslink}
# And download it. It's really THAT simple!
wget $link
exit 0
