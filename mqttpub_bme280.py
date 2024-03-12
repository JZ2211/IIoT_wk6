"""
 paho MQTT client - a publisher example
 
 BME280 is assumed interfacing with Raspberry Pi via I2C.
 Data from the BME280 are save in a log file named after
 the date i.e. log_yyyy_mm_dd.txt, in the Raspberry pi
 under HOMEPATH/nodeID directory locally.  The message of
 the sensor data is published via a mosquitto broker. 

 Modified 3/8/2024 by Jin Zhu
 
"""

import time
from datetime import datetime
import re
import sys
import board
from adafruit_bme280 import basic as BME280
from savedata import savedata_locally as document
import paho.mqtt.client as mqtt

#Data will be save under the dirctory HOMEPATH/nodeID. For example, /home/pi/node1
HOMEPATH='/home/pi/' #modify if needed

TOPIC = "workshop/bme280" #TOPIC name, please modify
USERNAME = "user1"        #MQTT server username, please modify
PASSWORD = "workshop"     #MQTT server pasword, please modify
nodeID = "sensor516"      #indicate the node ID (hostname), please modify
TIME_INTERVAL = 10        #Sensor data are collected every TIME_INTERVAL seconds, modify as needed
mqtt_server = "127.0.0.1" #use localhost since it is in the same broker server
#if not, please use the IP address of the broker server, e.g. mqtt_server = "192.168.1.2"

#data fields for BME280 sensor
datatype = "Date, Time, Temperature(C), Pressure(hPa), Humidity(%)"

################ NO CHANGE IS NEEDED UNDER THIS LINE ##############################

#BME280 setup
i2cbus = board.I2C() #use default raspberry pi board SCL and SDA for I2C
mybme280=BME280.Adafruit_BME280_I2C(i2cbus,0x77)  #the default I2C address is 0x77 for adafruit BME280 board.
#use BME280(i2cbus, 0x76) instead if the I2C address is 0x76 
currenttime=time.time() #obtain the current time in seconds
try: 
     client = mqtt.Client()
     client.username_pw_set(USERNAME,PASSWORD)
     client.connect(mqtt_server,1883)  #default MQTT port 1883

     print("Start reading data from BME280......\n")
     client.publish(TOPIC, payload=datatype, qos=1, retain=True)
     print(datatype)
     while True:
       start = currenttime
       temp = time.time()
       if (temp-start)> TIME_INTERVAL:  #if TIME_INTERVAL passed, collect and publish data
        currenttime = temp
        timestamp = str(datetime.now()) #obtain current time and date

        #BME280 results
        temperature = mybme280.temperature #obtain the ambient temprature in Celsius degree
        pressure = mybme280.pressure  #obtain the pressure in hPa
        humidity = mybme280.humidity  #obtain the relative humidity in percentage
        timestamp = re.sub(' ',', ', timestamp) 
        output = timestamp + ", {0:.2f}, {1:.2f}, {2:.2f}".format(temperature, pressure, humidity)
        document(output, datatype)  #save data into a local text file
        output = nodeID + ', '+ output #add nodeID for publishing message
        client.publish(TOPIC, payload=output, qos=0, retain=True)  #publish message
        print(f"send data to "+TOPIC+": "+output) #display results in the terminal

except KeyboardInterrupt:
      print("Interrupted by User")
      sys.exit(0)

