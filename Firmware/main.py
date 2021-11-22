import time
import board
import paho.mqtt.client as mqtt
from bmp388 import *
from bme680 import *
from bmx055 import *
from bmx160 import *
from neo6m import *

msgV = ""
topicV = ""


def on_connect(client, userdata, rc):
    #print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("sensors-data/node1")

# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):

    global msgV, topicV
    #print(msg.topic+" "+str(msg.payload))
    topicV = str(msg.topic)
    msgV = str((msg.payload).decode('utf-8'))

    if(topicV == 'sensors-data/node1'):
        print("Settings Received: ", msgV)


clientID_prefix = ""
for i in range(0, 6):
    clientID_prefix = clientID_prefix + str(random.randint(0, 99999))


client = mqtt.Client("C1"+clientID_prefix)
#client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.hivemq.com", 1883, 60)
client.subscribe("sensors-data/node1")


client.loop_start()


def printSeparator():
    print("-"*10)


BME680_DATA = ""
BMP388_DATA = ""
BMX055_DATA = ""
BMX160_DATA = ""
NEO6M_DATA = ""


def getAllSensorsData():
    global BME680_DATA, BMP388_DATA, BMX055_DATA, BMX160_DATA, NEO6M_DATA
    printSeparator()
    printSeparator()
    print("BME680: Temperature, Gas, Humidity, Pressure, Altitude")
    print(getTempGasHumidPressAlti_BME680())
    printSeparator()

    printSeparator()
    print("BME388: Pressure, Temperature")
    print(getPressureTemp_BMP388())
    printSeparator()

    printSeparator()
    print("BMX055: Accleration(x,y,z), Rotation(x,y,z), Magnetic Sensor(x,y,z)")
    print(getAccRotationMag_BMX055())
    printSeparator()

    printSeparator()
    print("BMX160: Accleration(x,y,z), Rotation(x,y,z), Magnetic Sensor(x,y,z)")
    print(getAccelGyroMag_BMX160())
    printSeparator()

    printSeparator()
    print("NEO-6M: Latitude, Longitude")
    print(getLattLng_NEO6M())
    printSeparator()
    printSeparator()


def sendDataToServer_MQTT():
    global BME680_DATA, BMP388_DATA, BMX055_DATA, BMX160_DATA, NEO6M_DATA
    global client
    client.publish("sensor-data/data/BME680", BME680_DATA)
    client.publish("sensor-data/data/BME680", BMP388_DATA)
    client.publish("sensor-data/data/BME680", BMX055_DATA)
    client.publish("sensor-data/data/BME680", BMX160_DATA)
    client.publish("sensor-data/data/BME680", NEO6M_DATA)


oldtime = time.time()
while 1:

    if time.time() - oldtime > 2:  # get data after every 2 seconds
        oldtime = time.time()
        try:
            getAllSensorsData()
            sendDataToServer_MQTT()
        except Exception as e:
            print("e: ", e)
