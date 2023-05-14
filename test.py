import RPi.GPIO as GPIO
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Set up Firebase Realtime Database credentials
cred = credentials.Certificate('rpi-control.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://rpi-control-4fc05.firebaseapp.com/'
})

# Set up GPIO pins for LIGHT1 and LIGHT2
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)

# Define a function to toggle the value of LIGHT1 and update the database
def light1Toggle():
    # Get the current value of LIGHT1 from the database
    currentLight1Value = db.reference('/node1/light1').get() or False

    # Toggle the value of LIGHT1 and update the database
    newLight1Value = not currentLight1Value
    db.reference('/node1/light1').set(newLight1Value)

    # Update the state of LIGHT1
    GPIO.output(17, newLight1Value)

# Define a function to toggle the value of LIGHT2 and update the database
def light2Toggle():
    # Get the current value of LIGHT2 from the database
    currentLight2Value = db.reference('/node1/light2').get() or False

    # Toggle the value of LIGHT2 and update the database
    newLight2Value = not currentLight2Value
    db.reference('/node1/light2').set(newLight2Value)

    # Update the state of LIGHT2
    GPIO.output(27, newLight2Value)

# Set up a listener for the "Action" field in node2
actionRef = db.reference('/node2/Action')
def actionListener(event):
    # Get the value of the "Action" field
    action = event.data

    # Call the appropriate function based on the action
    if action == 'light1Toggle':
        light1Toggle()
    elif action == 'light2Toggle':
        light2Toggle()

# Attach the listener to the "Action" field
actionRef.listen(actionListener)

# Wait for events
while True:
    time.sleep(1)
