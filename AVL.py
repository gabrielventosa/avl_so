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
import Chronos
import gprs


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
	
	res = SER.set_speed('9600')
	imei = utils.getimei()
	time = Log.uptime()
	smsmsg = time + ' Starting Unit: ' + imei
	res = MDM.receive(20)
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
		hname = gprs.gethname()
		printdbg.printSER(hname)
		NUpdate = timers.timer(0)
		NUpdate.start(3)
		print "Ready to start main loop"
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
					print "ready to static update"
					Log.ReportError('Doing timeout Update')
					data["dyn"] = "0"
					Chronos.set_LockFlag()
					res = gprs.updateloop(hname,data,MAX_ERRORS)
					gp = gprs.disGPRS()
					NUpdate.start(3600)
					if res == -1:
						break
					serv_data = data
			except (Exception, StandardError, SystemError, RuntimeError):
				msg = 'Expception in Static Update: '
				Log.appendLog(msg)
				print "exception in static update"

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
					res = gprs.updateloop(hname,data,MAX_ERRORS)
					if res == -1:
						Log.ReportError('Error in updateloop')
						break
					serv_data = data
					NUpdate.start(300)

			except (Exception, StandardError, SystemError, RuntimeError):
				msg = 'Expception in Dynamic Update '
				Log.appendLog(msg)
				print "exception in dynamic update"
				
##############################################################################
##############END OF DYNAMIC UPDATE ROUTINE###################################
##############################################################################
##############################################################################
##############Start revision of wireless alert##		
			try:
				SER.send('SWICHT_LED\r')
				if(Chronos.check_PannicFlag() == 1):
					print 'Doing Pannic Update'
					data["dyn"] = "2"
					res = gprs.updateloop(hname,data,MAX_ERRORS)
					if res == -1:
						Log.ReportError('Error in updateloop')
						break
					else:
						Chronos.reset_PannicFlag()
					serv_data = data
					NUpdate.start(10)

				if(Chronos.check_LockFlag() == 0 and serv_data["dyn"] == "1"):
					data["dyn"] = "3"
					res = gprs.updateloop(hname,data,MAX_ERRORS)
					if res == -1:
						Log.ReportError('Error in updateloop')
						break
					serv_data = data
					NUpdate.start(10)
				

			except (Exception, StandardError, SystemError, RuntimeError):
				msg = 'Expception in Dynamic Update '
				Log.appendLog(msg)

##############################################################################
###############SMS CHECK######################################################
			try:
				msg = SMS.check4SMS()
				if(msg != -1):
					data = {}
					data = SMS.ReadMessage(msg)
					SER.send('New message from:')
					SER.send(data['phn'])
					SER.send('\r')
					SER.send('SMS Contents:')
					SER.send(data['sms'])
					SER.send('---END OF SMS\r')
					SMS.DelMessage(msg)
					CmdMnger.ProcessCMD(data['sms'],data['phn'])
					
			except (Exception, StandardError, SystemError, RuntimeError):
				msg = 'Expception in SMS'
				Log.appendLog(msg)
				print "exception in SMS check"

##############################################################################
###############SMS Delete######################################################
			try:
				if (Mto.isexpired()):
					res = DelSMS.delAll()
					Mto.start(432000)
				
			except (Exception, StandardError, SystemError, RuntimeError):
				msg = 'Expception in SMS'
				Log.appendLog(msg)
				print "exception in SMS delete"
				
	return
	
