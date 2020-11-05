#!/bin/bash

i=755
prelink="tw/twic"
poslink="g.zip"
while [ $i -lt 790 ]
do
link=${prelink}${i}${poslink}
mv $link /media/RA023157/Xadrez/TWIC/2009/
let "i = i + 1"
done
exit 0
