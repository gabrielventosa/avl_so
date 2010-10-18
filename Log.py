import MDM
import scmd

def appendLog(data):
	file = "Events.log"
	if ((data != "") and (data != -1)):
		f = open(file,'a')
		time = uptime()
		data = time + ' ' + data + '\n \r'
		f.write(data)
		f.close()
		return 1
	else:
		return -1

def uptime():
	res = scmd.sendCmd('AT+CCLK?','',10)
	if (res == -1):
		return -1
	res = res.split(',')
	res = str(res[1])
	return res[0:8]


def ReportError(data):
	print data
	appendLog(data)
	return

