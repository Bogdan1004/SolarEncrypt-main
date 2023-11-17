import RPi.GPIO as GPIO 
import paho.mqtt.client as mqtt
import time


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

motor1A = 21
motor1B = 18

GPIO.setup(motor1A, GPIO.OUT)
GPIO.setup(motor1B, GPIO.OUT)


motor2A = 23
motor2B = 25

GPIO.setup(motor2A, GPIO.OUT)
GPIO.setup(motor2B, GPIO.OUT)


mqtt_broker = "test.mosquitto.org"
mqtt_topic = "test/solar"


def stop():
    GPIO.output(motor1A, GPIO.LOW)
    GPIO.output(motor1B, GPIO.LOW)
    GPIO.output(motor2A, GPIO.LOW)
    GPIO.output(motor2B, GPIO.LOW)

def on_message(client, userdata, message):
    command = message.payload.decode()
    if command == "w":
        print('W primit')
        # Move both motors forward
        GPIO.output(motor1A, GPIO.HIGH)
        GPIO.output(motor1B, GPIO.LOW)
        GPIO.output(motor2A, GPIO.LOW)
        GPIO.output(motor2B, GPIO.LOW)
        time.sleep(0.2)
        stop()

    elif command == "s":
        print('S primit')
        # Move both motors backward
        GPIO.output(motor1A, GPIO.LOW)
        GPIO.output(motor1B, GPIO.HIGH)
        GPIO.output(motor2A, GPIO.LOW)
        GPIO.output(motor2B, GPIO.LOW)
        time.sleep(0.2)
        stop()
    elif command == "a":
        print('A primit')
        # Turn left
        GPIO.output(motor1A, GPIO.LOW)
        GPIO.output(motor1B, GPIO.HIGH)
        GPIO.output(motor2A, GPIO.LOW)
        GPIO.output(motor2B, GPIO.LOW)
        time.sleep(0.3)
        stop()
    elif command == "d":
        print('D primit')
        # Turn right
        GPIO.output(motor1A, GPIO.HIGH)
        GPIO.output(motor1B, GPIO.LOW)
        GPIO.output(motor2A, GPIO.LOW)
        GPIO.output(motor2B, GPIO.LOW)
        time.sleep(0.3)
        stop()
        

client = mqtt.Client()
client.connect(mqtt_broker)
client.subscribe(mqtt_topic)
client.on_message = on_message

client.loop_start()

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
    client.disconnect()
    client.loop_stop()
