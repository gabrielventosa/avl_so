import GPIO
import MOD
import Log

def feed():
    b = GPIO.setIOvalue(11, 0)
    b= GPIO.setIOvalue(12,  0)
    MOD.sleep(10)
    b = GPIO.setIOvalue(11, 1)
    b = GPIO.setIOvalue(12, 1)
    msg= 'Reseting External Watchdog'
    #Log.appendLog(msg)
    return 1
