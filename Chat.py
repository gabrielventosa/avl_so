import MOD
import MDM
import Log
import netcfg
import wd
import SER

def chat(Host,Script,data):

    SER.send('Ready to negotiate with server\r')    
    HTTP_ver = " HTTP/1.0"
    

    res = MDM.send('GET ',0)
    #res = MDM.send(Host,0)
    res = MDM.send(Script,0)
    res = MDM.send(data,0)
    res = MDM.send(HTTP_ver,10)
    res = MDM.sendbyte(0x0d,10)
    res = MDM.sendbyte(0x0a,10)
    res = MDM.send('Host: ',0)
    res = MDM.send(Host,0)
    res = MDM.sendbyte(0x0d,10)
    res = MDM.sendbyte(0x0a,10)
    res = MDM.sendbyte(0x0d,10)
    res = MDM.sendbyte(0x0a,10)

    resc = GetData(180)
    res = MDM.receive(30)
    return resc

def updchat(Host,data):

    Script = netcfg.Script
    updata = 'imei=' + data["imei"] + \
    '&latitud=' + str(data["latitud"])+ \
    '&longitud='+ str(data["longitud"])+ \
    '&latref='+ data["latref"]+ \
    '&longref='+ data["longref"]+ \
    '&speed=' + data["speed"]+ \
    '&course='+ data["course"]+ \
    '&gpssats=' + data["gpssats"]+ \
    '&alt=' + data["alt"]+ \
    '&batt='+ data["batt"]+ \
    '&dyn='+ data["dyn"]
    resc = chat(Host,Script,updata)
    return resc



def GetData(TIMEOUT_DWNLD):
    SER.send('Ready to wait for response\r')
    timeout = MOD.secCounter() + TIMEOUT_DWNLD
    timer = timeout - MOD.secCounter()
    HTML_UC_END = '</RESPONSE>'
    HTML_LC_END = '</response>'
    data = ''
    mesg = ''
    while ((data.find('NO CARRIER') == -1) and (timer >0) ):
        SER.send('...Downloading\r')
        datatmp = MDM.receive(5)
        data = data + datatmp
        timer = timeout - MOD.secCounter()
        wd.feed()

    if(data.find('HTTP/1.1 200') == -1):
        mesg = 'Update server ERROR: ' + data[0:12]
        SER.send(mesg)
        SER.send('\r')
        SER.send(data)
        SER.send('\r')
        data = -1

    else:
        mesg = 'Update server SUCCEFULL: ' + data[0:12]
        SER.send(mesg)
        SER.send('\r')

    Log.appendLog(mesg)        
    return data
