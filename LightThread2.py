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

"""
Proposed Fields:
	+ rPwr
	+ gPwr
	+ bPwr (the above from 0 to 100, integer?) these are ONLY to be changed in ultimate changer
	+ rSet
	+ gSet
	+ bSet - these are teh RGB 0 to 256 settings for the light, these do not consider dimmer
	+ COLORS - dictionary mapping color names (str) to [r,g,b] values
	+ dim - controls brightness, serves as overall multiplier
	+ jump - boolean, serves as kill switch for light jumping
	+ spped - [0,1] multiplier controls speed of jumping and fading
"""

import RPi.GPIO as GPIO
import time
import random
import threading

class LightThread(threading.Thread):
	"""
	Put Full description here
	"""

	def __init__(self):
		# Setup GPIO:
		# define pin numbers as constants

		# Set pins as out
		# Set frequency for pins
		# Start lights at 0 (off)

		"""
		Note, here we have the following fields:
			rPwr
			gPwf
			bPwr
		These are the powers for the lights of each color, range from
		0 to 100
		"""

		# Define the color dictionary: COLORS
		# Note: we want to match this to the html file for the page

		# Define the order colored names: ORDERED_COLORS
		# this is used for the fading, to go from color to color in order

		# define dimming constrol
		# initiliaze to 0.75

		# initliaze for jump and fade
		jump = False
		fade = False
		speed = 0.5 # play with this <----------

	def set_red(self, r, keep_jumping=False, keep_fading=False):
		"""
		Changes the red color -- Ultimate function

		Parameters
		----------
		`r` - is the [0,256] RGB value for the red component
		"""
		# if not keep_jumping and jump is True
		# set jump to false (flip the switch)

		# do the same as above for fading


		# save r as rSet (as still RGB number)
		# make [0,100] with (r/255)*100
		# make rPwr = dim*^^val
	# ^^Do this for all the colors

	def set_dim(self, new_dim):
		"""
		Updates the new dim settings, which requires updating the current colors
		"""
		# dim = new_dim (update value)
		# update colors to reflect this:
		# self.set_red(self.rSet) # i.e. setting it to current value,
		# however note that this time it will have a new dim
		# Do this for all the colors

	def to_color(self, color, keep_jumping=False, keep_fading=False):
		"""
		Changes the lights to `color`, where `color` is a string
		that *Must* be in COLORS
		"""
		# if not keep_jumping AND jump is True
		# i.e. we don't want to keep jumping but we currently are
		# set jump to false

		# do the same as above for fading

		# Check that color is acceptable, if not...just print?
		vals = self.COLORS[color]
		self.set_red(vals[0], keep_jumping)
		self.set_green(vals[1], keep_jumping)
		self.set_blue(vals[2], keep_jumping)

	def start_jump(self):
		"""
		Starts and controls jumping for lights
		-------
		UPDATE THIS WHEN IT IS WRITTEN/PSUEDO CODE DONE
		"""

		# set swtich to on
		jump = True
		fade = False

		# Start jumping loop
		while jump:
			# choose a random color from the dictionary
			# change to that color with to_color (with keep_jumping=True)
			# wait according to the speed timer <-------------- requires tweaking


	def stop_jump_and_fade(self):
		"""
		Stops the jumping -- to be called when the button is explicitly
		hit to stop the jumping
		-------
		UPDATE THIS WHEN IT IS WRITTEN/PSUEDO CODE DONE
		"""

		# flip the jump switch
		jump = False 
		fade = False

		# Now get the current color, in RGB form and return it as a dictionary
		# so that it can be sent JQURY style to update the sliders
		current = {
			"red":str(self.rSet),
			"green":str(self.gSet),
			"blue":str(self.bSet)
		}
		return current
		# Note, this will require the html/js to be updated so that the jump
		# button is bound to a getJSON

	def fade_between(c1, c2):
		"""
		Takes in c1 and c2, which are strings, these must correspond to colors
		in the COLORS dictionary, i.e. COLORS[c1] will return a list of 
		three elements for [R,G,B].
		Makes small adjustments to fade gently between these two colors, 
		starting at c1, and moving to c2. It finds the max difference in R,B,G
		and adjusts to take one step for the max
		"""

		# ensure at correct starting point
		self.to_color(c1)

		# find max number of steps
		r_steps = self.COLORS[c2][0] - self.COLORS[c1][0]
		g_steps = self.COLORS[c2][1] - self.COLORS[c1][1]
		b_steps = self.COLORS[c2][2] - self.COLORS[c1][2]
		max_steps = max(r_steps, g_steps, b_steps)

		# get time between each step
		time_between = (10/max_steps)*(2*self.speed) # gives 10 seconds per fade
		# when speed = 0.5. Therefore can tweak 10 and 2 in tuning for looks

		# set step sizes for each color
		r_delta = r_steps/max_steps
		g_delta = g_steps/max_steps
		b_delta = b_steps/max_steps

		# Start the fade loop
		i = 0
		while i < max_steps:
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
			c2 = self.ORDERD_COLORS[i+1]

			# fade between them
			self.fade_between(c1, c2)

			# increment loop
			i = (i + 1)%(num_colors-2) # -2 so that we don't get error defining c2







