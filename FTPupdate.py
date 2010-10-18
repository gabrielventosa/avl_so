#

# import the built-in modules
import MDM
import MOD
import SER
import md5


# ########################################################### #
# this values must be configured with valid ones..
# the one here are only for demo.
#
# this is the network name to register to
#
APN           = "internet.itelcel.com"
# this is the access point for GPRS - ask your network operator
#
HTML_ADDR     = "www.inteligenciamecanica.com"
FTP_ADDR      = "inteligenciamecanica.com"
# this is the HTML address to connect to
#
#FILE_NAME     = "HTMLupdate.pyo"
SCRIPT        = "/ubi-car/oaupd/oauget.php"
# this is the file name to save data to
#
# ########################################################### #
USERID =  "webgprs"
PASSWD = "webgprs2002"

################## timeout definitions #######################
TIMEOUT_DWNLD = 180
TIMEOUT_CONNECT = 100
TIMEOUT_REG = 100

# timeout for CGDCONT command = 20ms
TIMEOUT_CXT = 20

TIMEOUT_MINIMUM = 5
######################################################


HTML_UC_END = '</DATA>'
HTML_LC_END = '</data>'

HTML_UC_START = '<DATA>'
HTML_LC_START = '<data>'
IMEI = ''
################## FUNCTION DEFINITION ####################
#returns data downloaded in a duration of time equal to TIMEOUT_DWNLD
def GetData(FILE_NAME):

	data = ' '
	timer = MOD.secCounter()
	timeout = MOD.secCounter() + TIMEOUT_DWNLD
	datatmp = ''
	
	while ((datatmp.find(HTML_UC_END) == -1) and (datatmp.find(HTML_LC_END) == -1) and (timer > 0) ):
		data = data + datatmp
		datatmp = MDM.receive(50)
		timer = timeout - MOD.secCounter()
	if ((datatmp.find(HTML_UC_END) != -1) or (datatmp.find(HTML_LC_END) != -1)):
		data = data + datatmp
		SER.send(data)
		SER.send('\r\n')
	else:
		SER.send('No File found in data')
		SER.send('\r\n')
		data = -1
		return data

	uindx = data.find('\r\n')
	SER.send(data[:uindx])
	SER.send('\r\n')
	lindx = data.find('<ftpuser>')
	uindx = data.find('</ftpuser>')
	ftpuser = data[lindx+9:uindx]
	lindx = data.find('<ftppass>')
	uindx = data.find('</ftppass>')
	ftppass = data[lindx+9:uindx]
	lindx = data.find('<md5>')
	uindx = data.find('</md5>')
	md5sent = data[lindx+5:uindx]
	res = MDM.send('+++\r',0)
	MOD.sleep(20)
	res = MDM.receive(TIMEOUT_CONNECT)
	SER.send('Connection Closed Response:')
	SER.send(res)
	SER.send('\r\n')
	res = MDM.send('AT#SH\r',0)
	res = MDM.receive(TIMEOUT_CONNECT)
	
	res = ' '
	
	while (res.find('OK')== -1):
		res = MDM.send('AT#FTPOPEN="',0)
		res = MDM.send(FTP_ADDR,0)
		res = MDM.send('","',0)
		res = MDM.send(ftpuser,0)
		res = MDM.send('","',0)
		res = MDM.send(ftppass,0)
		res = MDM.send('",0\r',0)
		SER.send('Opening FTP connection\r\n')
		SER.send('User: ')
		SER.send(ftpuser)
		SER.send(' Password: ')
		SER.send(ftppass)
		SER.send('\r\n')
		res = MDM.receive(10*TIMEOUT_CONNECT)
		SER.send('FTP open result: ')
		SER.send(res)
		SER.send('\r\n')
		if (res.find('Already connected') >= 0):
			res = 'OK'
	MDM.send('AT#FTPTYPE=0\r',0)
	MDM.receive(TIMEOUT_MINIMUM)
	MDM.send('AT#FTPGET="',0)
	MDM.send(FILE_NAME,0)
	MDM.send('"\r',0)
	SER.send('Requesting File: ')
	SER.send(FILE_NAME)
	SER.send('\r\n')
	timer = MOD.secCounter()
	timeout = timer + 90 #secondi
	#Retrieve and save data function?
	ftpdata = ''
	while((ftpdata.find('NO CARRIER') == -1)  and (timer < timeout)):
		ftpdata = ftpdata + MDM.read()
		timer = MOD.secCounter()
		
	if(len(ftpdata) == 0):
		print "ERROR: data to save is empty \r"
		SER.send('"ERROR: data to save is empty\r\n"')
		return -1

	startIndex = 0
	endIndex = len(ftpdata)
	if(ftpdata.find('CONNECT\r\n') != -1):
		startIndex = ftpdata.find('CONNECT\r\n') + len ('CONNECT\r\n')
	if(ftpdata.find('NO CARRIER') != -1):
		endIndex = ftpdata.find('\r\nNO CARRIER')
	ftpdata= ftpdata[startIndex: endIndex]	
	SER.send('Checking for MD5\r\n')
	SER.send('MD5 sent:')
	SER.send(md5sent)
	SER.send('\r\n')
	md5calc = md5.new(ftpdata).digest()
	hexmd5 = md5ToHex(md5calc)
	SER.send('MD5 calc:')
	SER.send(hexmd5)
	SER.send('\r\n')
	if(hexmd5 != md5sent):
		SER.send('MD5 does not match')
		SER.send('\r\n')
		data = -1
		return data
	
	return ftpdata
    
def Main(FILE_NAME):
	
	res = SER.set_speed('115200')
	res = MDM.send('AT+CMEE=2\r',0)
	SER.send('Starting Update Script')
	SER.send('\r\n')
	res = MDM.receive(TIMEOUT_MINIMUM)
	IMEI = getimei()
	
	# check for SIM registration on a network 
	#res = MDM.send('AT+COPS\r',0)
	#res = MDM.receive(TIMEOUT_REG)
	#while ( res.find(',') == -1):
	#	res = MDM.send('AT+COPS\r',0)
	#	res = MDM.receive(TIMEOUT_REG)


	# wait until SIM is registered
	#while ( res.find(',') == -1):
	#	res = MDM.send('AT+COPS\r',0)
	#	res = MDM.receive(TIMEOUT_REG)

	#################################################
	#############Set user and password###############
	res = MDM.send('AT#USERID="',0)
	res = MDM.send(USERID,0)
	res = MDM.send('"\r',0)
	res = MDM.receive(TIMEOUT_MINIMUM)
	res = MDM.send('AT#PASSW="',0)
	res = MDM.send(PASSWD,0)
	res = MDM.send('"\r',0)
	res = MDM.receive(TIMEOUT_MINIMUM)
	############# define the PDP context #############
	##########################################
	res = MDM.send('AT+CGDCONT=1,"IP","',0)
	res = MDM.send(APN,0)
	res = MDM.send('"\r',0)
	res = MDM.receive(TIMEOUT_CXT)
	res = res.find ('OK')
	if (res == -1):
		print 'Error setting PDP context'
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
		res = MDM.send('AT#SD=1,0,80,"',0)
		res = MDM.send(HTML_ADDR,0)
		res = MDM.send('"\r',0)
	############# open the connection with the internet host
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
			
	############# send the command of getting data
			res = MDM.send('GET ',0)
			res = MDM.send(SCRIPT,0)
			res = MDM.send('?device=',0)
			res = MDM.send(IMEI,0)
			res = MDM.send('&file=',0)
			res = MDM.send(FILE_NAME,0)
			res = MDM.send(' HTTP/1.0\r\n',0)
			res = MDM.send('Host: ',0)
			res = MDM.send(HTML_ADDR,0)
			res = MDM.send('\r\n',0)
			res = MDM.send('\r\n\r\n\r\n\r\n',0)
			data = ' '
	############ get data
			print 'GETTING DATA'
			SER.send('GETTING DATA')
			SER.send('\r\n')

			response = -1			
			data = GetData(FILE_NAME)
			if (data!= -1):
				SER.send('DOWNLOAD COMPLETE --- SAVING DATA')
				SER.send('\r\n')
				print 'DOWNLOAD COMPLETE --- SAVING DATA'
				f = open(FILE_NAME, 'w')
				f.write(data)
				f.close()
				response = 1
			else:
				print 'ERROR GETTING DATA'
				SER.send('ERROR GETTING DATA')
				SER.send('\r\n')
			
		else:
			SER.send('NO CONNECT')
			SER.send('\r\n')
			response = -1
	############# return to OnLineCommandMode
		MDM.send('AT#FTPCLOSE\r',0)
		MDM.receive(TIMEOUT_CONNECT)
		#MDM.send('AT#SGACT=1,0\r',0)
		MDM.receive(TIMEOUT_CONNECT)
		SER.send('END of Program\r\n')
		
		return response

def md5ToHex(md5string):
	ret=[]
	hexstring=''
	hexmd5 = ''
	for c in md5string:
		ret.append("%02X" % ord(c))
	hexmd5 = hexstring.join(ret)
	return hexmd5

def getimei():
	res = MDM.send('AT#CGSN\r',0)
	res = MDM.receive(TIMEOUT_MINIMUM)
	SER.send('Device: ')
	SER.send(res)
	SER.send('\r\n')
	if (res.find(':') == -1):
		return -1
	index = res.find(':')
	return str(res[index+2:index+17])
	
	