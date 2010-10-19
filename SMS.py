import MDM
import MOD
import SER
import scmd
import wd

def sendSMS(NUMBER, SMSText):
	TIMEOUT_CMD = 50
	res = scmd.sendCmd('AT+CMGF', '1', TIMEOUT_CMD) # select text format type
	res = scmd.sendCmd('AT+CNMI', '2,1', TIMEOUT_CMD) # alarm indicators
	res = scmd.sendCmd('AT+CSMP', '17,167,0,0', TIMEOUT_CMD) # select message parameter
	res = scmd.sendCmd('AT+CMGS', NUMBER, TIMEOUT_CMD) # send the message without storing it
	if (res.find('>') == -1):
		return -1
	else:
		res = MDM.send(SMSText, 0)
		res = MDM.sendbyte(0x1a, 0)
		for i in range(6):
			res=MDM.read()
			if(res.find("OK")!=-1):
				return 1
			else:
				MOD.sleep(300)
		return -1

def check4SMS():
	res = scmd.sendCmd('AT+CMGF', '1', 50)
	TIMEOUT_CMD = 20
	timeout = MOD.secCounter() + TIMEOUT_CMD
	timer = timeout - MOD.secCounter()
	data = ''
	MDM.send('AT+CMGL="REC UNREAD"\r',0)
	while ((data.find('OK') == -1) and (timer >0) and (data.find('+CMS ERROR')==-1)):
		SER.send('...Listing SIM UNREAD MESAGESS\r')
		datatmp = MDM.receive(5)
		data = data + datatmp
		timer = timeout - MOD.secCounter()
		wd.feed()

	if (data.find('+CMGL:') == -1):
		SER.send('No new messages\r')
		return -1
	else:
		lindx = data.find('+CMGL: ')
		uindx = data.find(',"REC')
		slot = data[lindx+7:uindx]
		msg = 'New message received and stored on slot: ' + slot + '\r'
		SER.send(msg)
		return slot

def ReadMessage(number):
	res = scmd.sendCmd('AT+CMGF', '1', 10)
	res = scmd.sendCmd('AT+CMGR', number, 5)
	msg = res.split(',')
	phn_len = len(msg[1])
	phn = msg[1]
	data = {}
	data['phn'] = phn[1:phn_len-1]
	res = res[2:]
	sms_start = res.find('\r\n')
	sms_end = res.rfind('OK')
	data['sms'] = res[sms_start+2:sms_end-2]
	return data

def DelMessage(number):
	SER.send('Deleting Message on slot: ')
	SER.send(number)
	SER.send('\r')
	res = scmd.sendCmd('AT+CMGF', '1', 10)
	res = scmd.sendCmd('AT+CMGD', number, 10)
	return

	
	

	
	
