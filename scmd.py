import MDM
import MOD

#######################################
# sends a generic AT command and waits for a response
# if value is NULL then the AT command isn't compound (it's like ATA)
# if value isn't NULL then the AT command is like AT+CMGR=1
def sendCmd(cmd,value,waitfor):
	if (value != ""):
		cmd = cmd + '='
	else:
		cmd = cmd + '\r'
	res = MDM.send(cmd, 0)
	if (value != ""):
		res = MDM.send(value, 0)
		res = MDM.send('\r', 0)
	if (waitfor > 0):
		res = MDM.receive (waitfor)
	return res

def iterateCmd(comando, parametro, TIMEOUT_CMD, numCheck):
	while( numCheck >= 0):
		numCheck = numCheck -1
		res = sendCmd(comando, parametro, TIMEOUT_CMD)
		if(res.find('OK') != -1):
			return 1
		MOD.sleep(TIMEOUT_CMD)
		if(numCheck == 0):
			return -1
