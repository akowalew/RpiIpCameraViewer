import time
import os
import RPi.GPIO as GPIO
from subprocess import Popen, call, PIPE
import subprocess
import thread
import sys

# Leds pins. Active by HIGH state
# GPIO26 - LED1
# GPIO19 - LED2
# GPIO13 - LED3

LED1 = 26;
LED2 = 19;
LED3 = 13;

def setLed1State(state) :
	GPIO.output(LED1, state);

def setLed2State(state) :
	GPIO.output(LED2, state);

def setLed3State(state) :
	GPIO.output(LED3, state);

# Buttons pins. There is a pullup resistor. Pushed
# GPIO10 - BTN1
# GPIO09 - BTN2
# GPIO11 - BTN3 

BTN1 = 10;
BTN2 = 9;
BTN3 = 11;

def getBtn1State() :
	return GPIO.input(BTN1);

def getBtn2State() :
	return GPIO.input(BTN2);

def getBtn3State() :
	return GPIO.input(BTN3);

def configurePinout() :
	GPIO.setmode(GPIO.BCM);
	GPIO.setwarnings(False);

	GPIO.setup(LED1, GPIO.OUT);
	GPIO.setup(LED2, GPIO.OUT);
	GPIO.setup(LED3, GPIO.OUT);

	GPIO.setup(BTN1, GPIO.IN) ;
	GPIO.setup(BTN2, GPIO.IN) ;
	GPIO.setup(BTN3, GPIO.IN) ;


programToKill = False

def checkButtons(nameThread):
    while True :
        # check in the loop the state of buttons
	if not getBtn1State() :
	    # First, red button. We want to kill this script
	    setLed1State(True) 			
            time.sleep(1) # wait for debounce and be sure of user decision
	    if not getBtn1State() :
		setLed1State(False)
		subprocess.call("sudo shutdown now", shell=True)
		#wait until OS will kill this script
		while True :
		    continue
            setLed1State(False)

	if not getBtn2State() :
	    # Second, yellow button. Restart needed
	    setLed2State(True)
            time.sleep(1)
	    if not getBtn2State() :
		setLed2State(False)
		subprocess.call("sudo shutdown -r now", shell=True)
		#wait until OS will kill this script	
		while True :
		    continue
                
	if not getBtn3State() :
	    # third, blue button. Shutdown needed
	    setLed3State(True)
            time.sleep(1)
	    if not getBtn3State() :
                print "Skrypt konczy dzialanie"
		setLed3State(False)
                subprocess.call("sudo killall python", shell=True)
                break
    
    # let the thread repeat with 1s cycle
    time.sleep(1)

def main() :
	print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
	print "$$                                               $$"
	print "$$ Witam                                         $$"
	print "$$ Zaraz zacznie sie odtwarzanie wideo.          $$"
	print "$$ Jesli to nie nastapi, prosze nacisnac         $$"
	print "$$       czerwony przycisk i przytrzymac         $$"
	print "$$                                               $$"
	print "$$ By wylaczyc urzadzenie, prosze nacisnac       $$"
	print "$$       i przytrzymac czerwony  przycisk        $$"
	print "$$ By zrestartowac urzadzenie,prosze nacisnac    $$"
	print "$$       i przytrzymac zolty przycisk            $$"
	print "$$                                               $$"
	print "$$                               Milego dnia     $$"
	print "$$                                               $$"
	print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
	
	configurePinout()
	
        returnCode = subprocess.call(["/etc/init.d/displayCameras", "stop"])
        returnCode = subprocess.call(["/etc/init.d/displayCameras", "start"])

        thread.start_new_thread(checkButtons, ("OtherThread", ) )
	while True :
                time.sleep(8)
                returnCode2 = subprocess.call(["/etc/init.d/displayCameras", "repair"])

if __name__ == "__main__" :
	main()
