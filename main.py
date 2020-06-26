import xbee
import time
import binascii
import sys
x = xbee.XBee() #Create an XBee object
while True:
	voltage = x.atcmd('%V')
	print("Voltage at " + str(voltage))
	tx_req = ("7E"+"00"+"05"+"2D"+"01"+str(voltage))
	try:
		xbee.transmit(xbee.ADDR_COORDINATOR, binascii.unhexlify(tx_req))
	except:
		print("Error occured to send package, probably not connected to ZigBee network")
	beacon_temperature = x.atcmd('TP')
	print("Temperature at " + str(beacon_temperature))
	# convert unsigned 16-bit value to signed beacon_temperature
	if beacon_temperature > 0x7FFF:
		beacon_temperature = beacon_temperature - 0x10000
	beacon_temperature = beacon_temperature * 100
	tempstr = str(beacon_temperature)
	msglen = "%0.2X" % (2 + len(tempstr))
	tx_req = ("7E"+"00"+msglen+"2D"+"02"+tempstr)
	try:
		xbee.transmit(xbee.ADDR_COORDINATOR, binascii.unhexlify(tx_req))
	except:
		print("Error occured to send package, probably not connected to ZigBee network")
	print("going to sleep now")
	time.sleep_ms(60000)
	if x.wake_reason() is xbee.PIN_WAKE:
		print("woke early on DTR toggle")
		sys.exit()