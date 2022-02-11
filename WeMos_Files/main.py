
# WASD main v1.0

'''
you get four splits in the message: direction of motor, speed of motor, servo direction
'''


# imports
import socket
import sys
from machine import Pin, I2C
import time
import machine
import math


class Car():
	def __init__(self):
		# motor 
		self.maxDutyMotor = 1023
		self.dutyClimbMotor = 20
		self.minDutyMotor = 300
		self.dutyAmount = 0

		# networking
		self.port = 12347
		self.computerIp = '192.168.1.146'

		# servo pins and pwms
		self.analoguePin = machine.Pin(0) #D3
		self.pwmServo = machine.PWM(self.analoguePin)
		self.pwmServo.freq(50)

		self.analoguePin1 = machine.Pin(2) #D4
		self.pwmServo1 = machine.PWM(self.analoguePin1)
		self.pwmServo1.freq(50) 


		# motor pins and pwms
		self.speedPinA = machine.Pin(15) #D8

		self.speedPWMA = machine.PWM(self.speedPinA)

		self.speedPWMA.freq(50)

		self.directionPinA = machine.Pin(12, Pin.OUT) #D6

		# richtingPinA.value(0)

		self.speedPinB = machine.Pin(13) #D7
		self.speedPWMB = machine.PWM(self.speedPinB)

		self.speedPWMB.freq(50)

		self.directionPinB = machine.Pin(14, Pin.OUT) #D5


	def motor(self, direction, speedPercent):
		direction, speedPercent = int(direction), int(speedPercent)
		# set directions
		if not direction == 2:
			self.directionPinA.value(direction)
			self.directionPinB.value(direction)

		# set speeds
		speed = self.maxDutyMotor * speedPercent # calc speed

		if speedPercent == 0: # if the speedPercent is 0 then the motor stops.
			speed = 0
		elif speed < self.minDutyMotor: # if speed is under the min duty it gets the min
			speed = self.minDutyMotor

		# set speeds
		if direction == 2:
			self.speedPWMA.duty(0)
			self.speedPWMB.duty(0)
		else:
			self.speedPWMA.duty(speed)
			self.speedPWMB.duty(speed)


	def servo(self, degrees):
		'''
		Pulse range = maximum pulse width - minimum pulse width (2 - 1 = 1)
		Pulse width per degree = pulse range / 181. (1/181)
		For a specified angle, the pulse width = minimum pulse width + (angle * pulse width per degree) (1 + (90 * (1/181)) = 1,4972)
		'''


		'''degrees = int(degrees)
								# set directions
								direction = (degrees/18.0) + 2.5
						
								pulse_width_per_degree = (1/181)
								pulde_width = 1 + (degrees * pulse_width_per_degree)
								percent_duty = pulde_width - 1
								duty = int(percent_duty * self.maxDuty) 
								if duty < self.minDuty:
									duty = self.minDuty
								print(duty)
								
								direction = int(direction)
								# self.pwmServo.duty(direction)
								# self.pwmServo.duty(direction)
								self.pwmServo.duty(duty)'''

		degrees = int(degrees)
		self.pwmServo.duty(degrees)

	def main_loop(self):
		# decoding the message
		message = self.s.recv(1024).decode()
		print('>', message, '<')
		if message == 'close':
			self.s.close()
		else:
			info = []
			counter = 0
			for i in message.split():
				info.append(i)
				counter += 1

			# call functions
			self.motor(info[0], info[1])
			self.servo(info[2])




	def on_execute(self):
		# connecting
		# try creating the socket
		try:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print ("Socket successfully created")
		except socket.error as err:
			print ("socket creation failed with error %s" %(err))

		# connecting to the server
		
		self.s.connect((self.computerIp, self.port))


		while True: # call main loop
			self.main_loop()

if __name__ == '__main__':
	car = Car()
	car.on_execute()
