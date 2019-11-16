# controller3.py
# Kenneth Lipke
# July 2018

"""
New in v3: using the new LightThread2 file with updated lightThread,
also using slightly updated lightPage.html as the main page. 
"""

from flask import Flask, render_template, flash, request, sessions, abort
import RPi.GPIO as GPIO
import time
import random
import threading
import ast

from LightThread2 import * 

########################################################################
#								Setup
########################################################################

# Create the app
app = Flask(__name__)

def get_cmd():
	"""
	returns the GET command sent via Jquery from the page
	"""
	a = request.args
	cmd = None
	try:
		cmd = a['command']
	except:
		cmd = None
	return cmd


# Create light thread
lt = LightThread() # from LightThread2 (updated)


########################################################################
#								Controller
########################################################################
@app.route("/", methods=["GET"]) # get so it can handle jquery
def light_controls():
	# Retrieve jQuerry command
	cmd = get_cmd()
	print(cmd) # show command for debugging
	
	# To prevent NoneType errors when string slicing
	if cmd is None:
		cmd = ""
	
	# Command for color change based on preset button
	# if cmd[0:6] == "Color:":
	# 	color = cmd[6:]
	# 	if color in lt.COLORS:
	# 		lt.to_color(color)
	# 	else:
	# 		print("ERROR: the color '" + color + "' is not defined")
			
	# # Command for slider color change
	# if cmd[0:2] == "R:":
	# 	lt.set_red(int(cmd[2:]))
	# elif cmd[0:2] == "G:":
	# 	lt.set_green(int(cmd[2:]))
	# elif cmd[0:2] == "B:":
	# 	 lt.set_blue(int(cmd[2:]))
	
	if cmd[0:6] == "Color:":
		# Parse the color code
		vals = ast.literal_eval(cmd[6:])
		
		# Send to lights
		lt.to_code(vals)

	
			
	# Slider for dimming (brightness)
	if cmd[0:7] == "Bright:":
		dim = cmd[7:]
		lt.set_dim(float(dim))
		
	# Jump button
	if cmd == "jump":
		lt.start_jump()
		
	# Fade button
	if cmd == "fade":
		lt.start_fade()
	
	# Stop button
	if cmd == "stop":
		lt.stop_jump_and_fade()
		
	# Set speed with slider
	if cmd[0:6].lower() == "speed:":
		lt.set_speed(float(cmd[6:]))


	return render_template("lights.html")

########################################################################
#								Main & Run
########################################################################
if __name__ == "__main__":
	# Run the app
	app.run(debug=True, host="0.0.0.0", use_reloader=False, threaded=True)
	

	# Runs when the server is stopped (ctr + c)
	print("\n\n")
	print(80*"-")
	print("Quitting") 
	
	# Put GPIO cleanup here
	GPIO.cleanup()
	print("GPIO cleaned")
