# paho MQTT client example on Windows
# Save received message to a log_yyyy_mm_dd.txt file
# This is for paho-mqtt version 2.0.0
# 
# Modified 2/11/2023
# by Jin Zhu


import time
from datetime import datetime
import re
from os import path
import os
import paho.mqtt.client as mqtt

#Data will be save under the dirctory HOMEPATH/nodeID.
#For example, C:/Users/zhuj/Documents/workshop/node1
HOMEPATH='C:/Users/zhuj/Documents/workshop/' # modify the home path if needed

TOPIC = "workshop/bme280" # modify topic as needed.
USERNAME = "user1"        #MQTT server username, please modify
PASSWORD = "workshop"     #MQTT server password, please modify
mqtt_server = "192.168.1.2" #the IP address of the broker server, please modify

############## Modified is not needed under this line ###########################

#save the received messages to a file.
def save_tofile(nodeID,message):
    if not path.exists(HOMEPATH+nodeID):
        os.mkdir(HOMEPATH+nodeID)
    timestamp = str(datetime.now()) #obtain current time and date
    timestamp = re.sub(' ',', ', timestamp)
    logdate = timestamp.split(',')[0]
    filename = HOMEPATH+nodeID+'/log_' + re.sub('-','_',logdate)+'.txt'  #log file will be named as log_yyyy_mm_dd.txt
    print(filename)
    if path.exists(filename):  #is the log file exist?
        #if yes, append data
        with open(filename,'a', buffering=1) as f1:
            f1.write(timestamp+', '+message+'\n')
    else:
        #if no, create the file and write the message
        with open(filename,'w', buffering=1) as f1:
            f1.write(timestamp+', '+message+'\n')            

# The callback for when the client receives a CONN ACK response from the server.
def on_connect(client, userdata, flags, rc, properties):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe("$SYS/#")  #display all system messages of MQTT
    client.subscribe(TOPIC)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    print(len(msg.payload))
    message= str(msg.payload).split("'")[1] #remove b'
    nodeID = message.split(',')[0] #obtain the first item (node id)
    save_tofile(nodeID, message)


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)  #this is for paho-mqtt version 2.0
client.on_connect = on_connect   #call back function when connected
client.on_message = on_message   #call back function when receiving a message
client.username_pw_set(USERNAME,PASSWORD) #provide authentication info to connect to the broker
client.connect(mqtt_server,1883)  #default MQTT port 1883

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
