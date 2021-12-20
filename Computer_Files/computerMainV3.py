"""
axis 0 = x, -1: naar links, 1: naar rechts
axis 1 = y, -1: naar voren, 1: naar achteren
axis 2 = draaien, 1: naar rechts, -1: naar links
axis 3 = throttle, 1: -, -1: +
"""



import pygame, time, socket


class App(): # main app
	def __init__(self): # init
		pygame.init() # init pygame
		self.screen = pygame.display.set_mode((500, 500)) # define the screen
		self.run = True # run = True for the main loop

		# some colors
		self.color_dark = (100, 100, 100)
		self.color_light = (200, 200, 200)

		# x, y, width, height, text, command
		self.buttonConnect = [50, 250, 90, 30, "Connect", self.buttonConnect] 
		self.buttons = [self.buttonConnect] # list with all the buttons
		# some font(s)
		self.smallFont = pygame.font.SysFont('Corbel', 16)

		self.connected = False



	def joystick_init(self): 
		pygame.joystick.init() # init the joystick
		self.joystick_count = pygame.joystick.get_count() # gets the joystick count
		self.joystick = pygame.joystick.Joystick(0) # defines joystick var
		self.joystick.init() # init joystick

		self.axes = self.joystick.get_numaxes() # count of axes

		self.axess = [0, 0, 0, 0]



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
		elif event.type == pygame.MOUSEBUTTONDOWN: # when lmb gets pressed
			for button in self.buttons: # for every button there is
				if button[0] <= pygame.mouse.get_pos()[0] <= (button[0] + button[2]) and button[1] <= pygame.mouse.get_pos()[1] <= (button[1] + button[3]): # check if the mouse pos is on a button
					button[5]() # calls the assigned function for a specific button
					


	def on_loop(self): # loop for calc
		for i in range(self.axes):
			self.axess[i] = int(self.joystick.get_axis(i)*100)

		if self.connected:
			car.send_axes(self.axess, self.cList)


		# check direction
		if self.axess[1] > 20:
			self.backwards = True
			self.forwards = False
		elif self.axess[1] < -20:
			self.backwards = False
			self.forwards = True
		else:
			self.backwards = False
			self.forwards = False

		if self.axess[0] > 20:
			self.right = True
			self.left = False
		elif self.axess[0] < -20:
			self.right = False
			self.left = True
		else:
			self.right = False
			self.left = False



	def on_render(self): # loop for render

		for button in self.buttons: # render all buttons

			pygame.draw.rect(self.screen, self.color_dark, pygame.Rect(button[0], button[1], button[2], button[3])) # draw the rectangle

			self.screen.blit(self.smallFont.render(button[4], True, self.color_light), ((button[0] + 10), (button[1] + 10))) # draw the text

			counter = 1

			for axes in self.axess:
				self.screen.fill(pygame.Color("black"), (250, (100*(counter+1)-100), 400, 40))
				self.screen.blit(self.smallFont.render("Axis {} value: {}".format(str(counter-1), self.axess[counter-1]), True, self.color_light), ((250), ((100*(counter+1)-100))))
				counter += 1



		# directions
		if self.backwards == True:

			pygame.draw.rect(self.screen, pygame.Color('red'), pygame.Rect(0, 480, 500, 20))
		else:
			pygame.draw.rect(self.screen, pygame.Color('black'), pygame.Rect(0, 480, 500, 20))

		if self.forwards == True:
			pygame.draw.rect(self.screen, pygame.Color('red'), pygame.Rect(0, 0, 500, 20))
		else:
			pygame.draw.rect(self.screen, pygame.Color('black'), pygame.Rect(0, 0, 500, 20))

		if self.left == True:
			pygame.draw.rect(self.screen, pygame.Color('red'), pygame.Rect(0, 20, 20, 460))
		else:
			pygame.draw.rect(self.screen, pygame.Color('black'), pygame.Rect(0, 0, 20, 500))

		if self.right == True:
			pygame.draw.rect(self.screen, pygame.Color('red'), pygame.Rect(480, 20, 20, 460))
		else:
			pygame.draw.rect(self.screen, pygame.Color('black'), pygame.Rect(480, 0, 20, 500))




		pygame.display.flip() # finally, render everything
	def on_cleanup(self): # cleanup 
		pygame.quit()

	def on_execute(self): # on execute
		self.joystick_init()

		while self.run: # main loop that calls the other loops
			for event in pygame.event.get(): # gets the events
				self.on_event(event) # calls on_event with the event
			self.on_loop()
			self.on_render()

		self.on_cleanup() # when the main loop stops



class Car(): # everything related to the car

	def __init__(self): # init
		self.port = 42069

	def disconnect(self, cList): # disconnect
		for c in cList:
			c.close()

	def connect(self): # connect
		print("connect")
		s = socket.socket()
		s.bind(('', self.port))
		s.listen(5)
		c, addr = s.accept()
		#c1, addr1 = s.accept()
		cList = [c]
		print('connected')

		return cList

	def send_message(self, message, cList):
		for i in cList:
			i.send(message.encode())

	def send_axes(self, axes, cList):
		
		self.send_message('{} {} {} {} '.format(axes[0], axes[1], axes[2], axes[3]), cList)

		time.sleep(0.1)








if __name__ == '__main__': 
	app = App() 
	car = Car()
	app.on_execute() # calls on_execute function

