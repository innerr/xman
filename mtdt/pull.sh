mac=`cat ble.mac | grep SensorTag | tail -n 1 | awk '{print $1}'`

if [ -z "$mac" ]; then
	echo "no mac address, run scan.sh first" >&2
	exit
fi

cmd="gatttool -i hci0 -b $mac"

$cmd --char-write -a 0x34 -n 01

$cmd --char-write -a 0x37 -n 0a
$cmd --char-write -a 0x37 -n 09
$cmd --char-write -a 0x37 -n 08
$cmd --char-write -a 0x37 -n 07
$cmd --char-write -a 0x37 -n 06
$cmd --char-write -a 0x37 -n 05
$cmd --char-write -a 0x37 -n 04
$cmd --char-write -a 0x37 -n 03
$cmd --char-write -a 0x37 -n 02
$cmd --char-write -a 0x37 -n 01

$cmd --char-write-req -a 0x31 -n 0100 --listen
