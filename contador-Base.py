#!/usr/bin/python

import RPi.GPIO as GPIO
import datetime

from string import whitespace

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_UP)

watts=1
lastpuls = datetime.datetime.now()  

debug = True
#debug = False

logfile = '/var/log/S0power'

print ("Log in " + logfile)

# give here the value of your official  meter
realmeter= 164670400

# if first start  meter is adjusted
#if meter_new < realmeter:
#    meter_new = realmeter
meter_new = 0    
meter_old = meter_new
print('Last value is '  +  str(meter_new/2000))

# write restart to logfile
logregel = str(datetime.datetime.now()) + " Restart S0 counter with value "  +  str(meter_new/1000)
l = open(logfile, 'a')
l.write (logregel + '\n')
l.close()

while True:
    GPIO.wait_for_edge(23, GPIO.RISING)
    GPIO.wait_for_edge(23, GPIO.FALLING)

    now = datetime.datetime.now()
    
    datediff= now - lastpuls
    aantalseconden = datediff.total_seconds()
    power = (meter_new - meter_old) /aantalseconden * 3600


    logregel = str(now) + ' Acumulado ' +   str(meter_new/3000) +  ' kW/h'
    #print (logregel)
    if debug == True:
        print (logregel+ " ; potencia: "  + str(power) + "; contador: " + str(meter_new))

    if meter_new % 100 == 0: 
        l = open(logfile, 'a')
        l.write (logregel + '\n')
        l.close()
        
    if (meter_new) % 3000 == 0 :   # 
        print (logregel)
        pulsmeter = str(meter_new )
        client.publish("house/power",str(power)) 
        
        print (logregel  + " ; potencia: "  + str(power) + "; contador: " + str(meter_new))
        

        lastpuls = now
        meter_old = meter_new
        
    #watts = watts + 1
    meter_new = meter_new + 1

GPIO.cleanup()
