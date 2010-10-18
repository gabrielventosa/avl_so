import scmd

def getimei():
	res = scmd.sendCmd('AT#CGSN','',10)
	if (res == -1):
		return -1
	index = res.find(':')
	return str(res[index+2:index+17])

def getBattery():
	res = scmd.sendCmd('AT+CBC','',10)
	if (res == -1):
		return -1
	batt = res.split(',')
	battlife = batt[1]
	return battlife[0:3]

def dist(lati,latf,longi,longf):
	dlat = abs(lati-latf)
	dlong = abs(longi-longf)
	dd = dlat+dlong
	return dd
