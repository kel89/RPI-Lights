# Raspberry Pi RGB Light Controller

This repo contains code to setup a basic RGB light controller with a raspberry pi, the documentation is laid out as follows:

- [RPI Setup](#rpi-setup)
- [Python Code](#python-code)
- [Front-end Code](#font-end-code)
- [Running](#running)

## RPI Setup
This section will focus on the hardware setup of the RPI. I will skip the obvious stuff (e.g., power cord, HDMI cord, keyboard, etc.) and focus on how we wire it up to the lights and the light power. 

Gear:

- RGB Light strip
	- must have four pins to connect, one for each of the RGB colors as well as for power (this is standard)
- Mosfet (X3)
	- N-Channel MOSFET (I used IRLZ34N per some tutorial I found), apparently it is key that they have a threshold voltage max of 3.3V (I actually think I ignored this when I bought mine, and it has worked)
	- My understanding is that these control the power that comes from the socket into the lights, and meshes that with the control inputs sent by the RPI
- Power Source
	- This is the power source for the lights, *not the RPI*. It is important to use a seperate sourece because if we have a lot of lights they will draw a lot of power. 
	- You need a 12V power supply that plugs into the wall
	- You will also need something that takes the end of that cable and can transfer it to two jumpers--called something like "DC Power Cable Female Connector Plug"
- Breadboard
	- This is pretty much required to connect the wires with the MOSFETs
- Jumpers
	- You will need wires that connect to the RPI pins and the lights/power source (probably came with your RPI if you bought a kit)

Now that you have all the harware you need to wire it up. The diagram below should explain what needs to be connected where:

![Diagram](https://github.com/kel89/RPI-Lights/blob/master/RPi%20LED%20Circuit.png)

## Python Code
Lets start by getting all the dependencies we need before jumping in and understanding a little bit about how the code works. Per a tutorial I think it is best to install the following:
```
sudo apt-get install build-essential unzip wget
```
```
wget http://abyz.me.uk/rpi/pigpio/pigpio.zip && unzip pigpio.zip && cd PIGPIO && sudo make install
```
Honestly, not sure if I ended up using them, but can't hurt. 

In terms of other packages, everything should already be there with your stsandard Python 3 distro. **This only works with Python 3**. Packages used:

- RPi.GPIO
- pigpio (this is the less flickery way to have the lights)
- time
- random
- threading
- flask
- ast

There are two main files of python code, `controller.py` handles the server. This sets up a super basic flask server (making sure to have threading setup correclty) and handles really basic GET commands from the site. These commands are parsed and sent to the `LightThread`.

`LightThread2.py` houses the main `LightThread` class which does the heavy lifting of controlling the lights. This is a sub class of `Thread` so it can operate in the background of the server and take commands on the fly. On initialization it setsup the lights, pins, powers, and paramets. Then it takes calls from the controller to change the color, brightness, speed, or turn off. The high-level interface functions use helper methods to translate RGB's into frequencies for the LED's.

## Front-end Code
This was built for mobile--so it will look a bit funny on a large display window. The centerpiece is a big color where made with D3.js and stored in the `static` directory. The sliders are made with NoUISliders, which is a nifty little JS package that I have downloaded and served without a CDN. jQuerry and Bootstrap are also used. 

`lights.html` is the main page, which houses the bones, styles, as well as the JavaSciprt for everything but the `ColorWheel` prototype. The color commands all go through a `maste` function which updates the visuals (the wheel and sliders) as well as sends a command to the server. Because the button, brightness, and speed commands are so simple they are handled directly in the definitions of those elements. 

The only issue that may be encountered is if you go to change the `ColorWheel.js` file. You may not notice the updated version being servered up because your browser will Cache it. What I have been doing is just clearing the browser history for that site durring development, or you could start time-stamping the file name. 

## Running
This is setup in such a way that if you clone the repo onto your RPI, follow the two install steps outline at the top of the Python section, you should be able to just run this without tweaking any code. Opening the terminal you should only need to do the following (given that you are in the correct directory):

- `sudo pigpiod`
	- to setup the pins (required on startup of the pi)
- `python3 controller.py`
