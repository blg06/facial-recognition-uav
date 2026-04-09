# Real-Time Facial Recognition System  

# Raspberry Pi · OpenCV · Python · PiCamera2

# 

# This facial recognition system was my final project for the UAV Technology and Operations program in 2025. It grabs a live video feed from a Raspberry Pi camera, spots faces it knows, and instantly pops up identity info right on the screen.

# 

# 

# Features  

# \- Detects and recognizes faces in real time using the Raspberry Pi camera  

# \- Spots several faces at once—doesn’t just stop at one  

# \- Shows each person’s name, age, and a masked TC (ID) number as an overlay  

# \- Boxes in green for clean records, red for flagged ones  

# \- Tweaked for Raspberry Pi: checks every 5th video frame to keep the CPU happy  

# \- Lets you watch everything remotely with RealVNC Viewer  

# \- Two parts: one for face registration (`yuz\_kaydet.py`), one for live recognition (`yuz\_tanima.py`)

# 

# Hardware  

# \- Raspberry Pi 4  

# \- Raspberry Pi Camera Module (PiCamera2)  

# \- Laptop for remote access via VNC

# 

# Software \& Libraries  

# opencv-python  

# face\_recognition  

# numpy  

# picamera2

# 

# To set up, just run:  

# pip install opencv-python face\_recognition numpy picamera2

# 

# Project Structure  

# ├── yuz\_tanima.py        # Where the live recognition runs  

# ├── yuz\_kaydet.py        # Where you snap and save everyone’s faces  

# ├── face\_data.json       # The demo’s fake ID database  

# ├── known\_faces/         # Where all the registered face images live  

# │   └── person\_name/  

# │       ├── person\_name\_0.jpg  

# │       └── ...  

# └── README.md

# 

# How It Works  

# 

# Register a Face  

# Fire up `yuz\_kaydet.py` to snap up to 20 pictures of someone. It saves them straight into `known\_faces/<name>/`.  

# python yuz\_kaydet.py

# 

# Run Live Recognition  

# Start `yuz\_tanima.py` to launch the real-time recognition.  

# python yuz\_tanima.py

# 

# The system loads all the registered faces up front. As the video rolls, it looks for faces, then matches them to the database using the dlib-based `face\_recognition` library. It pulls the rest of the info from `face\_data.json`.

# 

# Face Data Format  

# Here’s how `face\_data.json` stores fake ID info, one entry per person:

# {

# &#x20; "bilge": {

# &#x20;   "name": "Bilge",

# &#x20;   "age": "22",

# &#x20;   "tc": "12345678901",

# &#x20;   "criminal\_record": "hayir"

# &#x20; }

# }

# All the data in these examples is just for demo purposes—none of it’s real.

# 

# Motivation  

# I built this to dig into what happens when you mix computer vision with drones. Kind of a crossroads of two exciting fields.

