import FTPupdate
import MOD
import MDM

#res = -1
#while (res == -1):
#    res = FTPupdate.Main('AVL.pyo')
#    MOD.sleep(10)
#res = -1

#MOD.sleep(50)

#while (res == -1):
#    res = FTPupdate.Main('Chat.pyo')
#    MOD.sleep(10)

#res = -1

#MOD.sleep(50)

#while (res == -1):
#    res = FTPupdate.Main('gpsinfo.pyo')
#    MOD.sleep(10)

#res = -1

#MOD.sleep(50)

#while (res == -1):
#    res = FTPupdate.Main('Log.pyo')
#    MOD.sleep(10)

#res = -1

#MOD.sleep(50)

#while (res == -1):
#    res = FTPupdate.Main('main.py')
#    MOD.sleep(10)

#res = -1

#MOD.sleep(50)

#while (res == -1):
#    res = FTPupdate.Main('netcfg.pyo')
#    MOD.sleep(10)

#res = -1

#MOD.sleep(50)

#while (res == -1):
#    res = FTPupdate.Main('scmd.pyo')
#    MOD.sleep(10)

#res = -1

#MOD.sleep(50)

#while (res == -1):
#    res = FTPupdate.Main('SMS.pyo')
#   MOD.sleep(10)

#res = -1

#MOD.sleep(50)

#while (res == -1):
#    res = FTPupdate.Main('timers.pyo')
#    MOD.sleep(10)

#res = -1

#MOD.sleep(50)


#while (res == -1):
#    res = FTPupdate.Main('utils.pyo')
#    MOD.sleep(10)

#res = -1

#MOD.sleep(50)

#while (res == -1):
#   res = FTPupdate.Main('wd.pyo')
#    MOD.sleep(10)

#res = -1

#res = -1
#while (res == -1):
#    res = FTPupdate.Main('printdbg.pyo')
#    MOD.sleep(10)
#res = -1

res = -1
while (res == -1):
    res = FTPupdate.Main('CmdMnger.pyo')
    MOD.sleep(10)
res = -1

res = MDM.receive(100)
res = MDM.send('AT#ESCRIPT="main.py"\r',0)
res = MDM.receive(100)
MOD.sleep(100)
res = MDM.send('AT#REBOOT\r',0)
res = MDM.receive(100)