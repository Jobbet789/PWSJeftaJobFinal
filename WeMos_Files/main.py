
#main v2.0


# imports
import socket
import sys
from machine import Pin, I2C
import time
import machine
import math


class Car(): # main class
	def __init__(self):
		
		# Pin numbers
		self.analoogPin = machine.Pin(0) #D3
		self.snelheidPinA = machine.Pin(15) #D8
		self.richtingPinA = machine.Pin(12, Pin.OUT) #D6
		self.snelheidPinB = machine.Pin(13) #D7
		self.richtingPinB = machine.Pin(14, Pin.OUT) #D5
		
		
		# var
		# motor 
		self.maxDutyMotor = 1023
		self.dutyClimbMotor = 20
		self.minDutyMotor = 300
		self.dutyAmount = 0

		# servo of wheels
		self.wheelRightDuty = 25 
		self.wheelLeftDuty = 125 
		self.wheelMiddleDuty = 75

		# networking
		self.port = 42069
		self.computerIp = '192.168.1.146' 

		self.deadzone = 20




		# servo pins and pwms
		self.pwmServo = machine.PWM(self.analoogPin)
		self.pwmServo.freq(50)


		# motor pins and pwms

		self.snelheidPWMA = machine.PWM(self.snelheidPinA)

		self.snelheidPWMA.freq(50)


		# richtingPinA.value(0)

		self.snelheidPWMB = machine.PWM(self.snelheidPinB)

		self.snelheidPWMB.freq(50)


		# joystick axes
		self.axes = [0, 0, 0, 0]


	# functions

	def speed(self, valueX, valueY):
		valueX, valueY = int(valueX), int(valueY)

		# speed and direction of motors
		if valueY > 0: # go backwards
			self.richtingPinA.value(0)
			self.richtingPinB.value(0)

		elif valueY < 0: # go forwards

			self.richtingPinA.value(1)
			self.richtingPinB.value(1)


		if valueX > self.deadzone:
			self.pwmServo.duty(int(self.wheelMiddleDuty+(self.wheelRightDuty - self.wheelMiddleDuty)*(valueX/100)))
		elif valueX < -self.deadzone:
			self.pwmServo.duty(int(self.wheelMiddleDuty-(self.wheelMiddleDuty-self.wheelLeftDuty)*(valueX/100)))
		else:
			self.pwmServo.duty(self.wheelMiddleDuty)



		# make the variables positive
		if valueX < 0:
			valueX = valueX * -1

		if valueY < 0:
			valueY = valueY * -1


		speedPercent = valueX**2 + valueY**2

		speedPercent = math.sqrt(speedPercent)

		if not speedPercent == 0:
			self.snelheidPWMA.duty(int(self.maxDutyMotor*speedPercent/100))
			self.snelheidPWMB.duty(int(self.maxDutyMotor*speedPercent/100))
		else:
			self.snelheidPWMA.duty(0)
			self.snelheidPWMB.duty(0)




			



	def main_loop(self):
		# decoding the message
		message = self.s.recv(1024).decode().split()

		for i in range(len(message)-4): message.pop()

		print('>', message, '<')

		self.axes = message


		self.speed(self.axes[0], self.axes[1])


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


		while True:
			self.main_loop()


if __name__ == '__main__':
	car = Car()
	car.on_execute()


