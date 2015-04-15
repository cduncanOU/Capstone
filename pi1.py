"""This code is for the Maverick Auction Box Capstone Project
This file is for Raspberry Pi 1 of 2 where the scale input is read through this Pi.
Pi 1 reads in serial data from the scale that has been run through a MAX3232 then displays
the current value of the scale in either Oklahoma or Texas mode. When new values come in, the
previous values are passed on to the 2nd Pi using a UART connection.

Written by Cooper Duncan"""

import serial
import time
import RPi.GPIO as GPIO

TIMEOUT = 1.0 # 1 second timeout for reading UART
BAUD_RATE = 9600

mode_pin = 17 # Pin 11 on Pi. Used for Texas/Oklahoma selection
ready_pin = 2 # Pin 3 on Pi. Used to tell when 2nd Pi is ready

def transfer_string(b,w,h,a):
	s = ""
	if b == True:
		s = "o"
	else:
		s = "t"
	s = s + str(w) + "!"
	s = s + str(h) + "$"
	s = s + str(a) + "\n"
	print s
	return s
	
def check_mode():
	if GPIO.input(mode_pin):
		return True
	else:
		return False
	return

def update_display(b,w,h,a):
	if b:
		print "WT: " + str(w)
	else:
		print "HD: " + str(h)
		print "AVG: " + str(a)
	return
		

def main():
	weight_current = 0.0
	weight_prev = 0.0
	head_current = 0
	head_prev = 0
	avg_current = 0.0
	avg_prev = 0.0
		
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(mode_pin, GPIO.IN)
	GPIO.setup(ready_pin, GPIO.IN)
	
	while GPIO.input(ready_pin) == 0:
		time.sleep(1)
		
	uart = serial.Serial("/dev/ttyAMA0", baudrate=BAUD_RATE, timeout=TIMEOUT)
	uart.open()
	
	b_Oklahoma = check_mode()
	update_display(b_Oklahoma, weight_current, head_current, avg_current)
	uart.write(transfer_string(b_Oklahoma, weight_prev, head_prev, avg_prev))
	
	while True:
		mode = check_mode()
		if b_Oklahoma != mode :
			b_Oklahoma = mode
			update_display(b_Oklahoma, weight_current, head_current, avg_current)
			uart.write(transfer_string(b_Oklahoma, weight_prev, head_prev, avg_prev))
			
		input = uart.readline()
		
		if input != '':
			if 'a' in input:
				input = uart.readline()
				input = input[0:len(input)-1]
				weight_prev = weight_current
				weight_current = float(input)
				update_display(b_Oklahoma, weight_current, head_current, avg_current)
				uart.write(transfer_string(b_Oklahoma, weight_prev, head_prev, avg_prev))
			
			elif 'b' in input:
				input = uart.readline()
				input = input[0:len(input)-1]
				head_prev = head_current
				head_current = int(input)
				input = uart.readline()
				avg_prev = avg_current
				avg_current = float(input)
				update_display(b_Oklahoma, weight_current, head_current, avg_current)
				uart.write(transfer_string(b_Oklahoma, weight_prev, head_prev, avg_prev))
				
	return
		
main()
