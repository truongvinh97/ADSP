#!/bin/python3

import RPi.GPIO as GPIO
import pyrebase
import time

# Set up GPIO pins for LIGHT1 and LIGHT2
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)

# Set up Pyrebase config and database
config = {
  "apiKey": "AIzaSyDODWGTGafsxmxwWUPL-v8pOPLqIXmdQ40",
  "authDomain": "rpi-control-4fc05.firebaseapp.com",
  "databaseURL": "https://rpi-control-4fc05-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "rpi-control-4fc05",
  "storageBucket": "rpi-control-4fc05.appspot.com",
  "messagingSenderId": "692674149716",
  "appId": "1:692674149716:web:e3f658d6654b4708f11cc1",
  "measurementId": "G-0P769E9SZ3"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

# Define a function to toggle the value of LIGHT1
def light1Toggle():
    # Get the current value of LIGHT1 from the database
    currentLight1Value = db.child("node1").child("light1").get().val()

    # Toggle the value of LIGHT1 and update the database
    newLight1Value = not currentLight1Value
    db.child("node1").update({"light1": newLight1Value})

    # Update the state of LIGHT1
    GPIO.output(17, newLight1Value)

# Define a function to toggle the value of LIGHT2
def light2Toggle():
    # Get the current value of LIGHT2 from the database
    currentLight2Value = db.child("node1").child("light2").get().val()

    # Toggle the value of LIGHT2 and update the database
    newLight2Value = not currentLight2Value
    db.child("node1").update({"light2": newLight2Value})

    # Update the state of LIGHT2
    GPIO.output(27, newLight2Value)

# Wait for events
while True:
    # Check for changes in LIGHT1 and LIGHT2 and update the states accordingly
    light1State = db.child("node1").child("light1").get().val()
    GPIO.output(17, light1State)

    light2State = db.child("node1").child("light2").get().val()
    GPIO.output(27, light2State)

    # Wait for 1 second before checking again
    time.sleep(1)
