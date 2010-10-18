import GPS
import Log

def gpsData():
	errmsg = 'Trying GPS ...Result: Fix Error'
	gpsmsg = 'GPS Fix Result: '
	pos = GPS.getActualPosition()
	res = pos.split(',')
	fix = res[5]
	if (fix== '0'):
		Log.appendLog(errmsg)
		return -1
	#Log.appendLog(gpsmsg+pos)
	gepos = GPS.getPosition()
	data = {"speed":res[7],"gpssats":res[10],"alt":res[4],"course":res[6], \
			"latitud":gepos[0],"longitud":gepos[2], \
			"latref":gepos[1],"longref":gepos[3]}
	return data
