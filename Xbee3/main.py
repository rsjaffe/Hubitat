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
	beeTemp = x.atcmd('TP')
	print("Temperature at " + str(beeTemp))
	# convert unsigned 16-bit value to signed beeTemp
	if beeTemp > 0x7FFF:
		beeTemp = beeTemp - 0x10000
	beeTemp = beeTemp * 100
	tempStr = str(beeTemp)
	msgLen = "%0.2X" % (2 + len(tempStr))
	tx_req = ("7E"+"00"+msgLen+"2D"+"02"+tempStr)
	try:
		xbee.transmit(xbee.ADDR_COORDINATOR, binascii.unhexlify(tx_req))
	except:
		print("Error occured to send package, probably not connected to ZigBee network")
	print("going to sleep now")
	time.sleep_ms(60000)
	if x.wake_reason() is xbee.PIN_WAKE:
		print("woke early on DTR toggle")
		sys.exit()