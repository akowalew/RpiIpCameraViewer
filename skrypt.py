import time
import os
import RPi.GPIO as GPIO
from subprocess import Popen, call, PIPE
import subprocess

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



def main() :
	print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
	print "$$                                               $$"
	print "$$ Witam                                         $$"
	print "$$ Zaraz zacznie sie odtwarzanie wideo.          $$"
	print "$$ Jesli to nie nastapi, prosze nacisnac         $$"
	print "$$       czerwony przycisk i przytrzymac         $$"
	print "$$                                               $$"
	print "$$ By wylaczyc urzadzenie, prosze nacisnac       $$"
	print "$$       i przytrzymac niebieski przycisk        $$"
	print "$$ By zrestartowac urzadzenie,prosze nacisnac    $$"
	print "$$       i przytrzymac zolty przycisk            $$"
	print "$$                                               $$"
	print "$$                               Milego dnia     $$"
	print "$$                                               $$"
	print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
	
	configurePinout()
	
        returnCode = subprocess.call(["./displayCameras", "stop"])
        returnCode = subprocess.call(["./displayCameras", "start"])

	while True :
                returnCode = subprocess.call(["./displayCameras", "test"])
                if returnCode == 1:
                    returnCode2 = subprocess.call(["./displayCameras", "repair"])
                
                time.sleep(5)

		if not getBtn1State() :
			# First, red button. We want to re-play camera
			setLed1State(True) 			
			i = 0;
			while (not getBtn1State()) and (i < 100) :
				i = i + 1
				time.sleep(0.01)
			if i == 100 :
				setLed1State(False)
                                print "Proba ponownego uruchomienia kamery..."
                                myProc = Popen(["./displayCameras", "repair"], stdout=PIPE)
                                procOut = myProc.communicate()[0]
                                if myProc.returncode == 1 :
                                    print "Nie moge uruchomic kamery!"
                                else:
                                    print "Kamera jest uruchamiana..."

		if not getBtn2State() :
			# Second, yellow button. Restart needed
			setLed2State(True)
			i = 0
			while (not getBtn2State()) and (i < 100) :
				i = i + 1
				time.sleep(0.01)
			if i == 100 :
				setLed2State(False)
				subprocess.call("sudo shutdown -r now", shell=True)
				#wait until OS will kill this script	
				while True :
					continue
                
		if not getBtn3State() :
			# third, blue button. Shutdown needed
			setLed3State(True)
			i = 0 
			while (not getBtn3State()) and (i < 100) :
				i = i + 1
				time.sleep(0.01)
			if i == 100 :
				setLed3State(False)
				subprocess.call("sudo shutdown now", shell=True)
				#wait until OS will kill this script
				while True :
					continue

		time.sleep(1);
		
if __name__ == "__main__" :
	main()
