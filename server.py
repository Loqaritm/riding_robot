import serial
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from time import sleep

try:
    arduinoSerialData = serial.Serial('/dev/ttyUSB0',9600) #komunikacja z arduino
except:
    print("cos nie poszlo z serialem")
MQTT_SERVER = "localhost"
MQTT_PATH = "client_server_communication"
MQTT_PATH_BACK = "server_client_communication"
 
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    temp = str(msg.payload)
    #print(temp)
    if (temp == "up"):
        print("received up from client")
        arduinoSerialData.write('up')
        sleep(0.1)
    elif (temp == "down"):
        print("received down from client")
        arduinoSerialData.write('down')
        sleep(0.1)
    elif (temp == "left"):
        print("received left from client")
        arduinoSerialData.write('left')
        sleep(0.1)
    elif (temp == "right"):
        print("received right from client")
        arduinoSerialData.write('right')
        sleep(0.1)


    # more callbacks, etc
 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect(MQTT_SERVER, 1883, 60)
 
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
#client.loop_forever()
# powinno byc loop start

while 1:
    client.loop()
    #arduinoSerialData.write('up')
    sleep(0.1)
    if (arduinoSerialData.inWaiting()>0):
        myData = arduinoSerialData.readline()
        print(myData)
        publish.single(MQTT_PATH_BACK, "temperatura / myData", hostname="localhost" )
    


    

