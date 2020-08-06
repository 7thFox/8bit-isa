CHIP=AT28C64B

[ -z "$1" ] && echo "No chip # passed" && exit

FILE="rom$1.bin"
([ -f $FILE ] || (echo "File '$FILE' not found" && exit)) && minipro -p $CHIP -w $FILE
