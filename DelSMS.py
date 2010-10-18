# import the built-in modules
import MDM
import MOD

# Initialize
def delAll():
    
    res = MDM.send('AT+CMGF=1\r', 0)
    res = MDM.receive(3)
    res = MDM.send('AT+CNMI=2,1\r', 0)
    res = MDM.receive(3)
    if(res.find('OK') != -1):
        print 'OK for AT+CNMI=2,1'
    else:
        print 'ERROR for AT+CNMI=2,1'

    #SIM status control - to avoid the 'sim busy' error
    print 'SIM Verification Cycle'
    a = MDM.send ('AT+CPBS?\r', 0)
    SIM_status = MDM.receive(10)
    if SIM_status.find("+CPBS")<0:
    	print 'SIM busy! Please wait!\n'
    while SIM_status.find("+CPBS:")< 0 :
        a = MDM.send ('AT+CPBS?\r', 0)
        SIM_status = MDM.receive(10)
        MOD.sleep(2)
    print 'SIM Ready'
    
    #receive the list of all sms
    MDM.send('AT+CMGL="ALL"\r', 0)
    smslist = ''
    MemSMS = MDM.receive(20)
    smslist = MemSMS
    while MemSMS != '':
        MemSMS = MDM.receive(20)
        smslist = smslist + MemSMS
    
    #listsms = MemSMS.splitlines()
    listsms = smslist.split('\n')
    listIndex = []  #the list of index to delete
    for string in listsms:
        if(string.find("+CMGL:") != -1):    #find the index of each sms
            start = string.find(":")
            end = string.find(",")
            myindex = string[(start+1):end]
            myindex = myindex.strip()
            listIndex.append(myindex)       
        print string
    
    if listIndex == []:
        print "No SMS in SIM"
    
    #delete all sms
    for index in listIndex:
        print "Deleting sms index: " + index
        MDM.send('AT+CMGD=', 0)
        MDM.send(index, 0)
        MDM.send('\r',0)
        res = MDM.receive(20)
        res = res.replace("\r\n", " ")
        print res


    return 1
