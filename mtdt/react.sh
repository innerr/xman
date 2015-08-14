mac=`cat ble.mac | grep SensorTag | tail -n 1 | awk '{print $1}'`

if [ -z "$mac" ]; then
	echo "no mac address, run scan.sh first" >&2
	exit
fi

gatttool -b $mac --interactive
