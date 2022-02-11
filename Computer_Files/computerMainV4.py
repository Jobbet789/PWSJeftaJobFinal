# computer main v4.0

import pygame, time, socket

class App():
	def __init__(self):
		pygame.init() # init pygame
		self.screen = pygame.display.set_mode((500, 500)) # define the screen
		self.run = True # run = True for the main loop

		# some colors
		self.color_dark = (100, 100, 100)
		self.color_light = (200, 200, 200)

		# x, y, width, height, text, command
		self.buttonConnect = [100, 250, 90, 30, "Connect", self.buttonConnect] 
		self.buttons = [self.buttonConnect] # list with all the buttons
		# some font(s)
		self.smallFont = pygame.font.SysFont('Corbel', 16)

		self.connected = False

		self.minDuty = 18
		self.maxDuty = 134
		self.middleDuty = int((134-18)/2+(18/2))

		self.move_input = 2 # 1 = backwards, 2 = stop, 3 = forwards
		self.speedPercent = 0 # percent of speed
		self.servo_input = 90 # 0 = left, 90 = middle, 180 = right

		self.increase_SP = False
		self.decrease_SP = False


		self.delta = 0

	def buttonConnect(self): # connect button
		self.cList = car.connect()
		self.connected = True
		self.buttonConnect[4], self.buttonConnect[5] = "Disconnect", self.buttonDisconnect

	def buttonDisconnect(self): # disconnect button
		car.disconnect(self.cList)
		self.connected = False
		self.buttonConnect[4], self.buttonConnect[5] = "Connect", self.buttonConnect # changes the list

	def on_event(self, event): # when an event occurs
		if event.type == pygame.QUIT:
			self.run = False # quit app
		else:
			if event.type == pygame.MOUSEBUTTONDOWN: # when lmb gets pressed
				for button in self.buttons: # for every button there is
					if button[0] <= pygame.mouse.get_pos()[0] <= (button[0] + button[2]) and button[1] <= pygame.mouse.get_pos()[1] <= (button[1] + button[3]): # check if the mouse pos is on a button
						button[5]() # calls the assigned function for a specific button


			# all key presses

			if event.type == pygame.KEYDOWN: # when pressing a key
				if event.key == pygame.K_w:
					self.move_input = 3
				elif event.key == pygame.K_s:
					self.move_input = 1

				if event.key == pygame.K_a:
					self.servo_input = self.minDuty
				elif event.key == pygame.K_d:
					self.servo_input = self.maxDuty

				if event.key == pygame.K_q:
					self.decrease_SP = True
				elif event.key == pygame.K_e:
					self.increase_SP = True

			if event.type == pygame.KEYUP: # when releasing a key
				if event.key == pygame.K_w:
					self.move_input = 2
				elif event.key == pygame.K_s:
					self.move_input = 2

				if event.key == pygame.K_a or event.key == pygame.K_d:
					self.servo_input = self.middleDuty

				if event.key == pygame.K_q:
					self.decrease_SP = False
				elif event.key == pygame.K_e:
					self.increase_SP = False



	def on_loop(self):
		# make list and send message
		message = [self.move_input, round(self.speedPercent), self.servo_input]
		message = ' '.join([str(item) for item in message])
		if self.connected:
			car.send_message(message, self.cList)




		if self.increase_SP == True and self.speedPercent < 100:
			self.speedPercent += (self.delta*100)
		if self.decrease_SP == True and self.speedPercent >= 0 :
			self.speedPercent -= (self.delta*100)




	def on_render(self): # loop for render

		for button in self.buttons: # render all buttons

			pygame.draw.rect(self.screen, self.color_dark, pygame.Rect(button[0], button[1], button[2], button[3])) # draw the rectangle

			self.screen.blit(self.smallFont.render(button[4], True, self.color_light), ((button[0] + 10), (button[1] + 10))) # draw the text

			counter = 1

		
		if self.move_input == 3:
			pygame.draw.rect(self.screen, pygame.Color('red'), pygame.Rect(0, 0, 500, 20))
		else:
			pygame.draw.rect(self.screen, pygame.Color('black'), pygame.Rect(0, 0, 500, 20))

		if self.move_input == 1:
			pygame.draw.rect(self.screen, pygame.Color('red'), pygame.Rect(0, 480, 500, 20))
		else:
			pygame.draw.rect(self.screen, pygame.Color('black'), pygame.Rect(0, 480, 500, 20))

		if self.servo_input == self.minDuty:
			pygame.draw.rect(self.screen, pygame.Color('red'), pygame.Rect(0, 20, 20, 460))
		else:
			pygame.draw.rect(self.screen, pygame.Color('black'), pygame.Rect(0, 0, 20, 500))

		if self.servo_input == self.maxDuty:
			pygame.draw.rect(self.screen, pygame.Color('red'), pygame.Rect(480, 20, 20, 460))
		else:
			pygame.draw.rect(self.screen, pygame.Color('black'), pygame.Rect(480, 0, 20, 500))


		if self.increase_SP:
			pygame.draw.rect(self.screen, pygame.Color('red'), pygame.Rect(400, 20, 20, 460))
		else:
			pygame.draw.rect(self.screen, pygame.Color('black'), pygame.Rect(400, 20, 20, 460))

		if self.decrease_SP:
			pygame.draw.rect(self.screen, pygame.Color('red'), pygame.Rect(40, 20, 20, 460))
		else:
			pygame.draw.rect(self.screen, pygame.Color('black'), pygame.Rect(40, 20, 20, 460))


		# text
		self.screen.fill(pygame.Color('black'), (250, 400, 60, 50))
		self.screen.blit(self.smallFont.render("Speed: {}".format(round(self.speedPercent)), True, self.color_light), (250, 400))


		pygame.display.flip() # finally, render everything


		

	def on_cleanup(self): # cleanup 
		pygame.quit()

	def on_execute(self): # on execute
		

		while self.run: # main loop that calls the other loops
			self.start = time.time() # gets start time
			for event in pygame.event.get(): # gets the events
				self.on_event(event) # calls on_event with the event
			self.on_loop() # call on loop function
			self.on_render() # call on render function
			self.end = time.time() # gets end time
			self.delta = (self.end-self.start) # calculate time it took for the past frame

		self.on_cleanup() # when the main loop stops 
class Car():
	def __init__(self):
		self.port = 12347

	def disconnect(self, cList): # disconnect
		self.send_message('close', cList)
		for c in cList:
			c.close()
		self.s.close()

	def connect(self): # connect
		print("connect")
		self.s = socket.socket()
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.s.bind(('', self.port))
		self.s.listen(5)
		c, addr = self.s.accept()
		#c1, addr1 = self.s.accept()
		cList = [c]
		print('connected')

		return cList

	def send_message(self, message, cList):
		for i in cList: # loops through cList to send the message
			i.send(message.encode()) 
		time.sleep(0.3)

if __name__ == '__main__':
	app = App()
	car = Car()

	app.on_execute()
