import datetime
import requests
from pvlib import solarposition
import RPi.GPIO as GPIO
import time

# Function to get latitude and longitude from IP address (using ipinfo.io)
def get_location_from_ip():
    response = requests.get("http://ipinfo.io")
    data = response.json()
    loc = data.get("loc", "").split(",")
    if len(loc) == 2:
        return float(loc[0]), float(loc[1])
    return None

# Function to calculate solar position
def calculate_solar_position(latitude, longitude):
    tz = 'auto'  # Automatically determine the time zone
    current_time = datetime.datetime.now()
    solar_position_data = solarposition.get_solarposition(
        current_time, latitude, longitude, method='nrel_numpy')
    return solar_position_data['zenith'], solar_position_data['azimuth']

# Function to move the servo motor based on solar position
def move_motor(servo_angle):
    # GPIO setup for servo control
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(servo_pin, GPIO.OUT)
    servo = GPIO.PWM(servo_pin, 50)  # 50 Hz PWM frequency

    try:
        servo.start(0)
        duty = servo_angle / 18 + 2
        #servo.ChangeDutyCycle(duty)
        time.sleep(1)
    finally:
        servo.stop()
        GPIO.cleanup()

if __name__ == '__main__':
    servo_pin = 18  # Modify this to match your setup
    latitude, longitude = get_location_from_ip()
    
    if latitude is not None:
        zenith, azimuth = calculate_solar_position(latitude, longitude)
        zenith=zenith.astype(int)
        print(f"Zenith Angle: {zenith} degrees")
        print(f"Azimuth Angle: {azimuth} degrees")
        
        # Calculate the servo angle based on zenith and azimuth angles
        servo_angle = 90 - zenith  # Adjust as needed for your setup
        move_motor(servo_angle)
    else:
        print("Unable to determine location from IP address.")

