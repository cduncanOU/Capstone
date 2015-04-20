
import serial
import time
import RPi.GPIO as GPIO

TIMEOUT = 1.0
BAUD_RATE = 9600

ready_pin = 2

def update_display(b,w,h,a):
	if b:
		print "WT: " + str(w)
	else:
		print "HD: " + str(h)
		print "AVG: " + str(a)
	return
		

def main():
	weight = 0.0
	head = 0
	avg = 0.0
		
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(ready_pin, GPIO.IN)
			
	uart = serial.Serial("/dev/ttyAMA0", baudrate=BAUD_RATE, timeout=TIMEOUT)
	uart.open()
	
	b_Oklahoma = check_mode()
	update_display(b_Oklahoma, weight, head, avg)
	uart.write(transfer_string(b_Oklahoma, weight_prev, head_prev, avg_prev))
	
	while True:			
		input = uart.readline()
		
		if input != '':
			if 't' in input:
				b_Oklahoma = False
			elif 'o' in input:
				b_Oklahoma = True
			else:
				weight = float(input)
				input = uart.readline()
				head = int(input)
				input = uart.readline()
				avg = float(input)
				
	return
		
main()
