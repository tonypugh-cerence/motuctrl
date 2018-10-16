import sys
import logging
import time
from RPi import GPIO
sys.path.append("modules")

from motu import cMotuCtrl
from logger import cLogger

dJsonLogger = { "loggers":	{ "":		{ "handlers":["standard","socket"], "level": "ERROR" }, # Root logger
				  "cMotuCtrl":	{ "handlers":["standard","socket"], "level": "ERROR", "propogate": False}}}

myLog = cLogger(dJsonLogger)

# Set up GPIO for the Rotary Encoder
clk = 22
dt  = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt,  GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Use a counter variable to keep track of knob rotation
counter = 0

# Set up MOTU
sDeviceIpAddress = '169.254.157.88'
oMotu001 = cMotuCtrl(sDeviceIpAddress)
iMixChannelList = [16, 17, 18]
lastGain = oMotu001.getMixerInFaderDb(16)

def volChange(gain):
	global lastGain
	if lastGain:
		gain += lastGain
		if gain >= -40 and gain <= -10:
			for iMixChannel in iMixChannelList:
				oMotu001.setMixerInFaderDb(iMixChannel, gain)
			lastGain = gain

# Get current state of the clk pin
clkLastState = GPIO.input(clk)

try:
	while True:
		# Get current state of clk and dt pins
		clkState = GPIO.input(clk)
		dtState  = GPIO.input(dt)

		if clkState != clkLastState:
			if dtState != clkState:
				counter += 1
			else:
				counter -= 1
			#print counter

		if counter > 3:
			volChange(2)
			counter = 0
			#print "vol up"
			time.sleep(0.05)
		elif counter < -3:
			volChange(-2)
			counter = 0
			#print "vol down"
			time.sleep(0.05)

		clkLastState = clkState
		#time.sleep(0.01)
finally:
	GPIO.cleanup()
