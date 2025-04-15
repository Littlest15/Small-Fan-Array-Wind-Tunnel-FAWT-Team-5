# Small-Fan-Array-Wind-Tunnel-FAWT-Team-5
This contains the python code used to control our fan array, as well as the instructions for how to use the code and fan array properly.


# Requirements
This code will only work with the fan array Team 5 constructed. We recommend using Thonny to run the code, as it is easy to use. Python 3.13.3 is also required, as this code uses Tkinter (Python's built in GUI).

Thonny Link: https://github.com/thonny/thonny/releases/tag/v4.1.7

Python Link: https://www.python.org/downloads/

# Setup Instructions
Step by step instructions for use of the code to control the fan array:

1) Plug in the power supply for the fan array. Do not turn it on yet.
2) Plug the usb cord for the fan array into your computer.
3) Wait about 5 seconds.
4) Run the code.
5) When the GUI appears, input the values you want the fans to run at when they are powered on.
6) Turn the power supply on (switch on side of fan array next to AC wall input). Fans will power on and operate at inputted values.
7) GUI can now be used to control fans as needed.

Between instances of running the code, the usb cord must be unplugged and steps 1-7 repeated.

# Control Instructions

All values are in percent of the fan load. 100% = max speed, 0% = lowest possible speed.

Each fan load can be inputted individually into the text boxes for each fan. The text boxes are organized by row and column, from the perspective of standing behind the fan array. 

When a value is inputted into the fan text boxes, it will turn red. This indicates that the value has changed but has not been implemented yet. To implement any changes to the fan speeds, click the "Set All" button. This will apply any changes made and the values will turn black.

There are a few presets. To implement a preset, click the preset button and then click "Set All"

Minimum: Changes all fan loads to 0%

Maximum: Changes all fan loads to 100%

Boundary Layer: Changes row 6 load to 0%, row 5 load to 50%, and rows 1-4 to 100%. This simulates boundary layer flow.

Random: Changes fan loads for each fan to a random value ranging from 0%-100%. This is ideal for simulating turbulant flows.

The live speed slider at the bottom bypasses the "Set All" button and any values currently applied to any fan. As soon as the slider is moved, it will change all values for all fans to the percentage load it indicates. 

# Electrical Inputs

Included in this repository is a spreadsheet showing which GP pins each fan is connected to for each of the 4 Raspberry Pi Pico 2's used to control the 36 fans. Each Pico's number is labeled next to them on the interior walls of the fan array. 
