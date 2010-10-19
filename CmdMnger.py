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
import SER
import FTPupdate


def ProcessCMD(cmd,number):
    SER.send('Starting remote command operations\r')
    if(cmd.find('REBOOT') != -1):
        msg = 'Rebooting via SMS commnad'
        SER.send(msg)
        SER.send('\r')
        Log.appendLog(msg)
        res = MDM.send('AT#REBOOT\r',0)
        res = MDM.receive(100)
        MOD.sleep(100)

    if(cmd.find('SOFTUPD') != -1):
        res = -1
        while (res == -1):
            res = FTPupdate.Main('updapp.pyo')
            MOD.sleep(10)
        res = MDM.receive(100)
        SER.send('Enabling Script\r')
        res = MDM.send('AT#ESCRIPT="updapp.pyo"\r',0)
        res = MDM.receive(100)
        MOD.sleep(100)
        SER.send('Rebooting\r')
        res = MDM.send('AT#REBOOT\r',0)
        res = MDM.receive(100)

    if(cmd.find('SALDO') != -1):
        SER.send('Requesting SALDO from TAE\r')
        res = SMS.sendSMS('333','SALDO')
        if(res == -1):
            return
        msg = -1
        while (msg == -1):
            SER.send('...Waiting for Message\r')
            msg = SMS.check4SMS()
        data = SMS.ReadMessage(msg)
        SMS.DelMessage(msg)
        if(data['phn'] == 'TAE'):
            SER.send('Message received from TAE\r')
            SER.send('Sending info to:')
            SER.send(number)
            SER.send('\r')
            res = SMS.sendSMS(number,data['sms'])

    if(cmd.find('GPSPOS') !=-1):
        data = gpsinfo.gpsData()
        if (data == -1):
            AI = MDM.send('AT$GPSAI\r',0)
            AI = MDM.receive(25)
            res = SMS.sendSMS(number,AI)
        else:
            pos = 'lat:'+str(data["latitud"])+'long:'+str(data["longitud"])+'nsats:'+data["gpssats"]
            res = SMS.sendSMS(number,pos)
            SER.send('Sending GPS info via SMS\r')
            SER.send('···:')
            SER.send(pos)
            SER.send('\r')
            
            
        
    return
