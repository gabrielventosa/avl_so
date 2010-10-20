import MDM
import SER
import MOD

def check_LockFlag():
	#unlocked returns 1
	res = SER.receive(15)
	res = SER.send('GET_LOCK_FLAG\r')
	res = SER.receive(15)

	if(res.find('UNLOCKED' != -1)):
		res = 1
	# locked returns 0
	else:
		res = 0
	return res

def set_LockFlag():
	res = SER.receive(15)
	res = SER.send('SET_LOCK_FLAG\r')
	res = SER.receive(15)
	return 1

def reset_LockFlag():
	res = SER.receive(15)
	res = SER.send('RESET_LOCK_FLAG\r')
	res = SER.receive(15)
	return 1

def check_PannicFlag():
	res = SER.receive(15)
	res = SER.send('GET_PANNIC_STATUS\r')
	res = SER.receivebyte(20)

	if(res == 97):
		print 
		#nopannic returns 1
		res = 1
	#pannic returns 0
	else:	
		res = 0
	return res

def reset_PannicFlag():
	res = SER.receive(15)
	res = SER.send('RESET_PANNIC_STATUS\r')
	res = SER.receive(15)
	return 1
