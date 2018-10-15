from RPi import GPIO
import time

clk = 22
dt  = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt,  GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

counter = 0
clkLastState = GPIO.input(clk)

try:
	while True:
		clkState = GPIO.input(clk)
		dtState  = GPIO.input(dt)
		if clkState != clkLastState:
			if dtState != clkState:
				counter += 1
			else:
				counter -= 1
			print counter
		clkLastState = clkState
#		time.sleep(0.01)
finally:
	GPIO.cleanup()
