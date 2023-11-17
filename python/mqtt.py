import paho.mqtt.client as mqtt
import psutil
import time
import subprocess
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12,GPIO.OUT)
servo1 = GPIO.PWM(12,50)
GPIO.setup(11,GPIO.OUT)
servo2 = GPIO.PWM(11,50)
GPIO.setwarnings(False)


servo1.start(7)
servo2.start(7)


broker_address = '192.168.1.132'
broker_port = 1883
topic = 'solar'

duty = 7
duty2 = 7

def on_connect(client, userdata, flags, rc):
    print('Connected to MQTT broker with result code ' + str(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    print('Received message servo 1: ' + str(msg.payload.decode('utf-8')))
    print(int(msg.payload.decode('utf-8')))
    target = int(msg.payload.decode('utf-8'))
    global duty
    while duty <= target:
        servo1.ChangeDutyCycle(duty)
        time.sleep(0.25)
        duty = duty + 0.5
    while duty > target:
        servo1.ChangeDutyCycle(duty)
        time.sleep(0.25)
        duty = duty - 0.5


def on_message1(client, userdata, msg):
    print('Received message servo 2: ' + str(msg.payload.decode('utf-8')))
    target = int(msg.payload.decode('utf-8'))
    global duty2
    while duty2 <= target:
        servo2.ChangeDutyCycle(duty2)
        time.sleep(0.25)
        duty2 = duty2 + 0.3
    while duty2 > target:
        servo2.ChangeDutyCycle(duty2)
        time.sleep(0.25)
        duty2 = duty2 - 0.3

def publish_board_info():
    sensors = psutil.sensors_temperatures()
    # if 'cpu-thermal' in sensors:
    cpu_temp = psutil.sensors_temperatures()
    client.publish(topic + '/cpu', str(cpu_temp['cpu_thermal'][0].current) + str('°C'))
    print("Published CPU Temperature:", str(cpu_temp['cpu_thermal'][0].current) + str('°C'))
    # else:
    #    print("CPU temperature sensor not found.")

    voltage = 5
    current = 2.5

    client.publish(topic + '/voltage', str(voltage) + str('V'))
    client.publish(topic + '/current', str(current) + str('A'))
    print("Published Voltage:", voltage, "V | Current:", current, "A")

    #fan = psutil.sensors_fans()
    #client.publish(topic + '/fan', str(fan['gpio_fan'][0].current) + str('RPM'))

client = mqtt.Client()

client.on_connect = on_connect
# client.on_message = on_message
# client.on_message1= on_message1
client.message_callback_add(topic + '/servo1', on_message)
client.message_callback_add(topic + '/servo2', on_message1)
client.publish_board_info = publish_board_info
client.connect(broker_address, broker_port, 60)

client.subscribe(topic + '/servo1')
client.subscribe(topic + '/servo2')

client.loop_start()

while True:
    publish_board_info()
    time.sleep(5)

client.disconnect()
client.loop_stop()
