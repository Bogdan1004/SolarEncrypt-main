import paho.mqtt.client as mqtt
import psutil
import time

broker_address = 'test.mosquitto.org'
broker_port = 1883
topic = 'test/solar'

def on_connect(client, userdata, flags, rc):
    print('Connected to MQTT broker with result code ' + str(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    print('Received message servo 1: ' + str(msg.payload.decode('utf-8')))
    print(int(msg.payload.decode('utf-8')))
    target = int(msg.payload.decode('utf-8'))

def on_message1(client, userdata, msg):
    print('Received message servo 2: ' + str(msg.payload.decode('utf-8')))
    target = int(msg.payload.decode('utf-8'))

def publish_board_info():

    cpu_temp = 50.0
    voltage = 5.0 
    current = 2.0 
    fan_speed = 1500 

    # client.publish(topic + '/current', 'CPU ' + str(cpu_temp) + '°C')
    # print("Published CPU Temperature: ", str(cpu_temp) + '°C')

    # client.publish(topic + '/current', 'voltage '+str(voltage) + 'V')
    # client.publish(topic + '/current', 'current '+str(current) + 'A')
    # print("Published Voltage: ", voltage, "V | Current: ", current, "A")

    # client.publish(topic + '/current', 'rpm '+str(fan_speed) + 'RPM')
    # print("Published Fan Speed: ", fan_speed,'RPM')

    client.publish(topic, 'w')
    print("w added")

client = mqtt.Client()

client.on_connect = on_connect
client.message_callback_add(topic, on_message)
client.message_callback_add(topic + '/servo2', on_message1)
client.connect(broker_address, broker_port, 60)

client.subscribe(topic)
client.subscribe(topic + '/servo2')

client.loop_start()

while True:
    publish_board_info()
    time.sleep(5)

client.disconnect()
client.loop_stop()
