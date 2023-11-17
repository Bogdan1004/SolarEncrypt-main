import Adafruit_DHT
import paho.mqtt.client as mqtt
import psutil
import random

import time
# Specifică tipul de senzor folosit (DHT11 sau DHT22)
sensor = Adafruit_DHT.DHT11

broker_address = 'test.mosquitto.org'
broker_port = 1883
topic = 'test/sensors'

def on_connect(client, userdata, flags, rc):
    print('Connected to MQTT broker with result code ' + str(rc))
    client.subscribe(topic)
    
def on_message(client, userdata, msg):
    print('Received message servo 1: ' + str(msg.payload.decode('utf-8')))
    print(int(msg.payload.decode('utf-8')))
    target = int(msg.payload.decode('utf-8'))

# Specifică numărul pinului GPIO la care este conectat senzorul
pin = 27

#while True:
    # Încearcă să citești datele de la senzor
    #humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    # Verifică dacă datele au fost citite corect
    #if humidity is not None and temperature is not None:
        #print("Temperatură: {}°C".format(temperature))
        #client.publish(topic + '/cpu', temperature)
        #print("Umiditate: {}%".format(humidity))
        #client.publish(topic + '/voltage', humidity)
    #else:
        #print("Eroare la citirea datelor de la senzor")

    # Poți modifica intervalul de citire a datelor aici
    #time.sleep(5.0)
    
def publish_board_info():
    sensors = psutil.sensors_temperatures()
    
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    
    cpu_temp = sensors['cpu_thermal'][0].current
    formatted_cpu_temp = "{:.2f}".format(cpu_temp)
    
    voltage = 5 + random.uniform(-0.5, 0.5)
    current = 2.5 + random.uniform(-0.5, 0.5)
    
    formatted_voltage = "{:.2f}".format(voltage)
    formatted_current = "{:.2f}".format(current)

    print("CPU Temp: {}%".format(cpu_temp))
    client.publish(topic + '/cpu', str(formatted_cpu_temp) + '°C')

    print("Voltage: {}".format(voltage))
    client.publish(topic + '/voltage', str(formatted_voltage) + 'V')
    
    print("Current: {}°C".format(current))
    client.publish(topic + '/current', str(formatted_current) + 'A')  
        
    print("Temperature: {}%".format(temperature))
    client.publish(topic + '/temp', str(temperature))
    
    
client = mqtt.Client()

client.on_connect = on_connect
client.message_callback_add(topic, on_message)
client.connect(broker_address, broker_port)
client.subscribe(topic)

client.loop_start()

while True:
    publish_board_info()
    time.sleep(5)

client.disconnect()
client.loop_stop()

'''
import time
import board
import adafruit_dht
import psutil

# We first check if a libgpiod process is running. If yes, we kill it!
for proc in psutil.process_iter():
    if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
        proc.kill()
sensor = adafruit_dht.DHT11(board.D27)
while True:
    try:
        temp = sensor.temperature
        humidity = sensor.humidity
        print("Temperature: {}*C   Humidity: {}% ".format(temp, humidity))
    except RuntimeError as error:
        print(error.args[0])
        sensor.exit()
        time.sleep(30.0)
        continue
    except Exception as error:
        sensor.exit()
        raise error
    time.sleep(30.0)
'''
