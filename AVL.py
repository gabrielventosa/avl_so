#
#AVL MAIN PROGRAM
import MDM
import MOD
import GPS


import Chat
import Log
import timers
import SMS
import scmd
import utils
import gpsinfo
import wd
import netcfg
import printdbg
import CmdMnger
import SER
import DelSMS


################## timeout definitions #######################
TIMEOUT_DWNLD = 180
TIMEOUT_CONNECT = 100
TIMEOUT_REG = 100

# timeout for CGDCONT command = 20ms
TIMEOUT_CXT = 20

TIMEOUT_MINIMUM = 5
######################################################


def Mainloop():
	MAX_ERRORS = 3
	UPDATE_TIME = 3600
	TIMEOUT_CMD = 500

	wd.feed()
	
	numrep = '5539099305'
	res = SER.set_speed('115200')
	imei = utils.getimei()
	time = Log.uptime()
	smsmsg = time + ' Starting Unit: ' + imei
#	res = SMS.sendSMS(numrep,smsmsg)
	res = MDM.receive(20)
#	res = MDM.send('atd5539099305;\r',0)
#	res = MDM.receive(50)
#	res = MDM.send('ATH\r',0)
#	res = MDM.receive(50)
	res = scmd.sendCmd('AT+CMGF', '1', 50)
	res = 1
	
	if(res != 1):
		Log.ReportError('Error Sending Init MSG')
	else:
		msg= 'Starting Unit:' + imei
		Log.appendLog(msg)
		printdbg.printSER(msg)
		

	res = scmd.sendCmd('at+cfun','5',10)
	serv_data = -1
	
	while 1:
		hname = gethname()
		printdbg.printSER(hname)
		NUpdate = timers.timer(0)
		NUpdate.start(3)
		Mto = timers.timer(0)
		Mto.start(120)
		
		while 1:
			wd.feed()
			printdbg.printSER("Doing GPS")
			data =gpsinfo.gpsData() 
			if data == -1:
				errmsg = "GPS Error"
				printdbg.printSER("GPS ERROR")
				#Log.ReportError(errmsg)
###############################################################################
###########STATIC UPDATE ROUTINE###############################################
###############################################################################
			try:
				if (NUpdate.isexpired() and data != -1):
					Log.ReportError('Doing timeout Update')
					data["dyn"] = "0"
					res = updateloop(hname,data,MAX_ERRORS)
					gp = disGPRS()
					NUpdate.start(30)
					if res == -1:
						break
					serv_data = data
			except (Exception, StandardError, SystemError, RuntimeError):
				msg = 'Expception in Static Update: '
				Log.appendLog(msg)
				

###############################################################################
############END OF STATIC UPDATE ROUTINE#######################################
###############################################################################				
				
			data = gpsinfo.gpsData()
			if data == -1:
				errmsg = "GPS Error"
				#Log.ReportError(errmsg)
###############################################################################
###############DYNAMIC UPDATE ROUTINE##########################################
###############################################################################
			try:
				if serv_data != -1 and data!= -1 and \
				    utils.dist(serv_data["latitud"],data["latitud"],serv_data["longitud"],data["longitud"]) > 5000:
					Log.ReportError('Dynamic Routine Update')
					data["dyn"] = "1"
					res = updateloop(hname,data,MAX_ERRORS)
					if res == -1:
						Log.ReportError('Error in updateloop')
						break
					serv_data = data
					NUpdate.start(300)

			except (Exception, StandardError, SystemError, RuntimeError):
				msg = 'Expception in Dynamic Update '
				Log.appendLog(msg)
				
##############################################################################
##############END OF DYNAMIC UPDATE ROUTINE###################################
##############################################################################

##############################################################################
###############SMS CHECK######################################################
			try:
				msg = SMS.check4SMS()
				if(msg != -1):
					data = {}
					data = SMS.ReadMessage(msg)
					SER.send('New message from:')
					SER.send(data['phn'])
					SER.send('\r\n')
					SER.send('SMS Contents:')
					SER.send(data['sms'])
					SER.send('---END OF SMS\r\n')
					SMS.DelMessage(msg)
					CmdMnger.ProcessCMD(data['sms'],data['phn'])
					
			except (Exception, StandardError, SystemError, RuntimeError):
				msg = 'Expception in SMS'
				Log.appendLog(msg)


##############################################################################
###############SMS Delete######################################################
			try:
				if (Mto.isexpired()):
					res = DelSMS.delAll()
					Mto.start(432000)
				
			except (Exception, StandardError, SystemError, RuntimeError):
				msg = 'Expception in SMS'
				Log.appendLog(msg)
				
	return
	
def Update(hname,data):
###############################################
	printdbg.printSER("Attemping Update")
	Log.appendLog("Attemping Update")
	
###############################################
		
###############################################
	res = utils.getBattery()
	if (res == -1):
		errmsg = "Battey Read Error"
		Log.ReportError(errmsg)
		return -1
	else:
		data["batt"]=res
	data["imei"] = utils.getimei()
###############################################
	
	
	
###############################################
	printdbg.printSER("Checking GPRS")
	if (is_gprs() == -1):
		printdbg.printSER('GPRS OFF')
		printdbg.printSER("Doing GPRS")
		res = connectGPRS()
		if (res == -1):
			errmsg ='Error Connecting to GPRS'
			Log.ReportError(errmsg)
			return -1

	printdbg.printSER("Dialing Server")
	led = scmd.sendCmd('AT#SLED','3,1,1',10)
	res = dial_serv()
	if (res == -1):
		errmsg = 'No server'
		Log.ReportError(errmsg)
		return -1
		
################################################
	printdbg.printSER("Doing Chat")
	res = Chat.updchat(hname, data)
	led = scmd.sendCmd('AT#SLED','2',10)
	if (res == -1):
		errmsg = "Sever Response Error"
		Log.ReportError(errmsg)
		return -1
	
	return 1


#established a GPRS connection
def connectGPRS():
	printdbg.printSER('connect GPRS')
	numCheck = 4
	TIMEOUT_CMD = 50
	CGDCONT = netcfg.CGDCONT
	USERID = netcfg.USERID
	PASSW = netcfg.PASSW

	#################################################
	#############Set user and password###############
	res = scmd.sendCmd('AT#USERID',USERID,10)
	res = scmd.sendCmd('AT#PASSW',PASSW,10)
	
	############# define the PDP context #############
	##########################################
	res = scmd.sendCmd('AT+CGDCONT',CGDCONT,10)
	res = res.find ('OK')
	if (res == -1):
		printdbg.printSER('Error setting PDP context')
		SER.send('Error setting PDP context')
		SER.send('\r\n')
		return -1
	else:
		res = ' '
		while (res.find('#SGACT:')== -1 and res.find('already activated') == -1):
			SER.send('Opening WEB connection\r\n')
			res = MDM.send('AT#SGACT=1,1\r',0)
			res = MDM.receive(2*TIMEOUT_CONNECT)
			SER.send(res)	

	return 1

#######################################

	




def is_gprs():
	res = scmd.sendCmd('AT#GPRS?','',10)
	if(res.find('#GPRS: 1') == -1):
		return -1
	return 1

def dial_serv():
	res = MDM.send('AT#SD=1,0,80,"',0)
	res = MDM.send(netcfg.hname,0)
	res = MDM.send('"\r',0)
############ open the connection with the internet host
	timer = MOD.secCounter()
	timeout = MOD.secCounter() + TIMEOUT_CONNECT
	res = MDM.receive(TIMEOUT_MINIMUM)
	res = res.find('CONNECT')
############# wait for connect ############
	while ((res == -1)and (timer > 0) ):
		res = MDM.receive(TIMEOUT_MINIMUM)
		res = res.find('CONNECT')
		timer = timeout - MOD.secCounter()
	if ( res != -1 ):
		print 'CONNECTED'
		SER.send('CONNECTED')
		SER.send('\r\n')
		return 1
	else:
		resturn -1


def gethname():
	hname = -1
	wd.feed()
	hname = netcfg.hname
	return hname

def updateloop(hname,data,MAX_ERRORS):
	for i in range(MAX_ERRORS):
		res = Update(hname,data)
		if res == 1:
			break
	if (res == -1):
		gp = disGPRS()
		res = Update(hname,data)
		gp = disGPRS()
	return res

def disGPRS():
	if(is_gprs != -1):
		res = scmd.sendCmd('AT#SGACT','1,0',50)

	return res
