# LightThread2.py
# Kenneth Lipke
# July 2018

"""
This is (at first) the psuedo code and planning for an updated
light thread object, which is created in the Flask web app.
It handles *ALL* the GPIO setup (note, you may desire to change this as more
total web functionality is added).


Main Components/Functionality:
- Color Selector (with predefined colors)
- RGB Sliders for user created colors
- Dimmer (controls overall brightness)
- Commands (jump, fade, on/off)


I think the best way to handlingt he dimming is with an ultimate changer, 
i.e., every ligth change at all has to go through an ultimate function that
applies the dimmer. Into this is fed the full color, and the dimmer is
applied only there. This is also the only place that rPwr, gPwr, and bPwr 
can be touched. In their place have fields rSet, gSet, bSet, which are the
0 to 255.

For the sliders, the app can direclty call set_red, etc. They have the command
and the value, and this will take care of the dimmer.

Next, we have to thinking about jumping (fading will come next). Here is the order
to thinking about jumping:
	- Define a kill switch
	- Define a speed setting
	- Randomize colors, and change them according to time
	- If another button hit, (like a color, or fade), stop the jumping
	- When, stopped, determine how to send RGB code back to app, and through
		to the html so it shows up in the slider
Now, if the user selects a new color, or moves the slider, before hitting
the stop jump button, we need to stop the jumping, withough adjusting the sliders.
with the `keep_jumping` options, we can simply OMIT them in the call from the 
app. This way, if a slider is adjusted, or a button pressed in the app, automatically
keep_jumping will be False, and the jumping will stop. (We can do something
similar for the fading when we get that figured out)

For fading, we first define an order list of colors, this is simply the color
names in strings, that MUST be in the `COLORS` dictionary. We also need a 
`fade` boolean switch. Similary, we need to add `keep_fading` arguments
to the color and slider functions (Just as with the jumping). Now thinking
about how the fading function will work, inside the while loop we will call
a function that fades between two colors. This fade_between function will take
two colors, and it will use the `speed` attribute; 

"""


import RPi.GPIO as GPIO
import pigpio # superior as uses better timing (no flicker)
import time
import random
import threading

class LightThread(threading.Thread):
	"""
	Fields
	------
	rPwr - [0,100] controlls power of red light
	gPwr - ^^ green
	bPwr - ^^ blue
	rSet - [0, 255] indicates current setting of red light
	gSet - ^^ green
	bSet - ^^ blue
	COLORS - Dictionary mapping string color names to [R, G, B]
	ORDERED_COLORS - list of color names ordered for fading
	dim - dim setting [0,1] (brightness)
	jump - Boolean, True if should be jumping
	fade - Boolean, True if should be fading
	speed - [0,1] denotes how fast should be fading/jumping
	"""

	def __init__(self):
		# Super class init
		threading.Thread.__init__(self)
		
		# GPIO initialization
		self.RPIN = 18
		self.GPIN = 23
		self.BPIN = 24

		# Setup GPIO
		#GPIO.setmode(GPIO.BCM)
		#GPIO.setup(RPIN, GPIO.OUT)
		#GPIO.setup(GPIN, GPIO.OUT)
		#GPIO.setup(BPIN, GPIO.OUT)
		self.pi = pigpio.pi()

		## Set frequency
		#self.rPwr = GPIO.PWM(RPIN, 300)
		#self.bPwr = GPIO.PWM(BPIN, 300)
		#self.gPwr = GPIO.PWM(GPIN, 300)

		## Start lights off
		#self.rPwr.start(0)
		#self.bPwr.start(0)
		#self.gPwr.start(0)
		
		# set colors to 0 to start
		self.pi.set_PWM_dutycycle(self.RPIN, 0)
		self.pi.set_PWM_dutycycle(self.GPIN, 0)
		self.pi.set_PWM_dutycycle(self.BPIN, 0)

		# Initialize 0-255 light attributes
		self.rSet = 0
		self.gSet = 0
		self.bSet = 0

		# Define the color dictionary: COLORS
		# Note: we want to match this to the html file for the page
		self.COLORS = {
			"blue" : [0,0,255],
			"red" : [255, 0, 0],
			"green" : [0, 255, 0],
			"yellow" : [255, 255, 0],
			"orange" : [255, 13, 0],
			"purple" : [138, 43, 226],
			"pink" : [255, 0, 200],
			"springgreen" : [0, 255, 127],
			"turquoise" : [64, 224, 208],
			"off" : [0,0,0]
		}

		# Define the order colored names: ORDERED_COLORS
		# this is used for the fading, to go from color to color in order
		self.ORDERED_COLORS = [
			"blue", "turquoise", "springgreen", "green",
			"yellow", "red", "pink", "purple"
		]
		
		# For test with smaller set of colors
		# self.ORDERED_COLORS = ["red", "pink", "blue"]

		# define dimming constrol
		# initiliaze to 0.75
		self.dim = 0.75

		# initliaze for jump and fade
		self.jump = False
		self.fade = False
		self.speed = 0.5 # play with this <----------
		self.last_jump = None # color of last jump

	def set_red(self, r, keep_jumping=False, keep_fading=False):
		"""
		Changes the red color -- Ultimate function

		Parameters
		----------
		`r` - is the [0,256] RGB value for the red component
		keep_jumping - Boolean denoting if this setting is part of jump
		keep_jumping - ^^ for fade
		"""
		# If this change is not associated with a jump change
		if (not keep_jumping) and (self.jump is True):
			# Stop jumping
			self.jump = False 

		# If this change is not associated with a fade change
		if (not keep_fading) and (self.fade is True):
			print("flipping fade switch in red")
			# Stop fading
			self.fade = False

		# save r as rSet (as still RGB number)
		self.rSet = r

		# map [0,100] -> [0,255]
		#rgb_val = int((r/255)*100)
		
		# Set light power (including dimmer)
		#self.rPwr.ChangeDutyCycle(self.dim*rgb_val)
		
		# Change red duty cycle
		self.pi.set_PWM_dutycycle(self.RPIN, self.dim*r)
		
	def set_green(self, g, keep_jumping=False, keep_fading=False):
		"""
		Changes the red color -- Ultimate function

		Parameters
		----------
		`r` - is the [0,256] RGB value for the red component
		keep_jumping - Boolean denoting if this setting is part of jump
		keep_jumping - ^^ for fade
		"""

		# If this change is not associated with a jump change
		if (not keep_jumping) and (self.jump is True):
			# Stop jumping
			self.jump = False 

		# If this change is not associated with a fade change
		if (not keep_fading) and (self.fade is True):
			print("flipping fade switch in green")
			# Stop fading
			self.fade = False

		# save r as rSet (as still RGB number)
		self.gSet = g

		# map [0,100] -> [0,255]
		#rgb_val = int((g/255)*100)
		
		# Set light power (including dimmer)
		#self.gPwr.ChangeDutyCycle(self.dim*rgb_val)
		
		# Set green duty cycle
		self.pi.set_PWM_dutycycle(self.GPIN, self.dim*g)

	
	def set_blue(self, b, keep_jumping=False, keep_fading=False):
		"""
		Changes the red color -- Ultimate function

		Parameters
		----------
		`b` - is the [0,256] RGB value for the red component
		keep_jumping - Boolean denoting if this setting is part of jump
		keep_jumping - ^^ for fade
		"""

		# If this change is not associated with a jump change
		if (not keep_jumping) and (self.jump is True):
			# Stop jumping
			self.jump = False 

		# If this change is not associated with a fade change
		if (not keep_fading) and (self.fade is True):
			print("flipping fade switch in blue")
			# Stop fading
			self.fade = False

		# save r as rSet (as still RGB number)
		self.bSet = b

		# map [0,100] -> [0,255]
		#rgb_val = int((b/255)*100)
		
		# Set light power (including dimmer)
		#self.bPwr.ChangeDutyCycle(self.dim*rgb_val)
		
		# Set blue duty cycle
		self.pi.set_PWM_dutycycle(self.BPIN, self.dim*b)
		
		
	def set_dim(self, new_dim):
		"""
		Updates the new dim settings, which requires updating the current colors
		"""
		# update value
		self.dim = new_dim
		
		# update colors to reflect this:
		self.set_red(self.rSet)
		self.set_green(self.gSet)
		self.set_blue(self.bSet)

	def to_color(self, color, keep_jumping=False, keep_fading=False):
		"""
		Changes the lights to `color`, where `color` is a string
		that *Must* be in COLORS
		"""
		# print("at top of to_color, keep_fading is", keep_fading, "and fade is", self.fade)
		
		# If this change is not associated with a jump change
		if (not keep_jumping) and (self.jump is True):
			# Stop jumping
			self.jump = False 

		# If this change is not associated with a fade change
		if (not keep_fading) and (self.fade is True):
			# Stop fading 
			print("Flipping fade switch")
			self.fade = False

		# Change color
		vals = self.COLORS[color]
		self.set_red(vals[0], keep_jumping, keep_fading)
		self.set_green(vals[1], keep_jumping, keep_fading)
		self.set_blue(vals[2], keep_jumping, keep_fading)
		
	def set_speed(self, new_speed):
		"""
		Updates the speed parameter
		"""
		if 0 <= new_speed and new_speed <= 1:
			self.speed = float(new_speed)
		else:
			print("New speed value is not in [0,1]")

	def start_jump(self):
		"""
		Starts and controls jumping for lights
		-------
		UPDATE THIS WHEN IT IS WRITTEN/PSUEDO CODE DONE
		"""

		# set swtich to on
		self.jump = True
		self.fade = False

		# Start jumping loop
		while self.jump:
			# choose a random color from the dictionary
			new_color = random.choice(list(self.COLORS.keys()))
			
			# Make sure not going to 'off'
			while new_color == "off" or new_color == self.last_jump:
				new_color = random.choice(list(self.COLORS.keys()))
			
			# change to that color with to_color (with keep_jumping=True)
			self.to_color(new_color, keep_jumping=True)
			self.last_jump = new_color
			
			# Pause based on speed parameter
			time.sleep(.2/self.speed) # so 1 second pause with default speed=2


	def stop_jump_and_fade(self):
		"""
		Stops the jumping -- to be called when the button is explicitly
		hit to stop the jumping
		-------
		UPDATE THIS WHEN IT IS WRITTEN/PSUEDO CODE DONE
		"""

		# flip the jump switch
		self.jump = False 
		self.fade = False
		self.last_jump = None

		# Now get the current color, in RGB form and return it as a dictionary
		# so that it can be sent JQURY style to update the sliders
		current = {
			"red":str(self.rSet),
			"green":str(self.gSet),
			"blue":str(self.bSet)
		}
		return current
		# TODO-----------------------------------------------------------
		# Note, this will require the html/js to be updated so that the jump
		# button is bound to a getJSON
		

	def fade_between(self, c1, c2):
		"""
		Takes in c1 and c2, which are strings, these must correspond to colors
		in the COLORS dictionary, i.e. COLORS[c1] will return a list of 
		three elements for [R,G,B].
		Makes small adjustments to fade gently between these two colors, 
		starting at c1, and moving to c2. It finds the max difference in R,B,G
		and adjusts to take one step for the max
		"""

		# ensure at correct starting point
		self.to_color(c1, keep_fading=True)

		# find max number of steps
		r_steps = self.COLORS[c2][0] - self.COLORS[c1][0]
		# print("red steps:", r_steps)
		g_steps = self.COLORS[c2][1] - self.COLORS[c1][1]
		# print("green steps:", g_steps)
		b_steps = self.COLORS[c2][2] - self.COLORS[c1][2]
		# print("blue_steps:", b_steps)
		max_steps = max(max(abs(r_steps), abs(g_steps), abs(b_steps)), 1) # no division by 0 later
		# print("Max steps are:", max_steps)

		# get time between each step
		time_between = (10/max_steps)*(.1/self.speed) # gives 10 seconds per fade
		# print("Total time for fade should be", time_between*max_steps)

		# set step sizes for each color
		r_delta = r_steps/max_steps
		# print("r delta", r_delta)
		g_delta = g_steps/max_steps
		# print("g delta", g_delta)
		b_delta = b_steps/max_steps
		# print("b delta", b_delta)

		# Start the fade loop
		i = 0
		# print("value of fade switch in fade function is", self.fade)
		while i < max_steps and self.fade is True:
			i += 1 # increment loop

			# change color
			self.set_red(self.rSet + r_delta, keep_fading=True)
			self.set_green(self.gSet + g_delta, keep_fading=True)
			self.set_blue(self.bSet + b_delta, keep_fading=True)

			# pause
			time.sleep(time_between)


	def start_fade(self):
		"""
		Starts fading between colors
		-------
		Update this when done
		"""

		# flip fade switch
		self.fade = True
		self.jump = False

		# Create loops that, while self.fade is True we iterate through 
		# self.ORDERED_COLORS
		num_colors = len(self.ORDERED_COLORS)
		i = 0
		while self.fade:
			# choose colors
			c1 = self.ORDERED_COLORS[i]
			c2 = self.ORDERED_COLORS[(i+1)%(len(self.ORDERED_COLORS))]
			print("Fading between", c1, "and", c2, "\nIndicies", i, ", ", (i+1)%(len(self.ORDERED_COLORS)))
			
			# fade between them
			self.fade_between(c1, c2)

			# increment loop
			i = (i + 1) % len(self.ORDERED_COLORS)







