import MOD
import GPIO
import MDM
import GPS
import AVL

try:
    AVL.Mainloop()
    MDM.send('AT#REBOOT\r',0)
except (Exception, StandardError, SystemError, RuntimeError):
    b = GPIO.setIOvalue(11, 0)
    MOD.sleep(10)