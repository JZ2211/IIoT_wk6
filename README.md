# IIoT workshop - week 6
## Project: Publish/Subscribe Protocol MQTT Implementation for IoT Applications
**System Overview**

<img src="https://github.com/JZ2211/IIoT_wk6/assets/100505718/c60ae3bb-a8b9-4eb0-84a6-13098ee19640" width="600">

## Mosqitto broker setup in Raspberry Pi

## MQTT publish client in Raspberry Pi
1. Connect a BME280 to the Raspberry Pi via I2C.
2. Install paho-mqtt package by running the command in ssh terminal:
   ```
   pip install paho-mqtt
   ```
3. download example code:
   ```
   wget https://raw.githubusercontent.com/JZ2211/IIoT_wk6/main/mqttpub_bme280.py
   wget https://raw.githubusercontent.com/JZ2211/IIoT_wk6/main/savedata.py
   ```
4. Modify the configuration related to the MQTT brokers at the top of the program: ```nano mqttpub_bme280.py```
5. Save the file. Test the mqtt client:
   ```
   python mqttpub_bme280.py
   ```
   If it runs sucessfully, you should observe a directory named as your hostname is created and files named after the date are saved under the directory.
6. If you want to run the program in background, you can use ```crontab -e``` to configure.

## MQTT subscribe client on a Windows computer :
1. Install paho-mqtt by running the command under the Windows Powershell:
   ```
   pip install paho-mqtt
   ```
3. Download the example code: ```mqttsub_4windows.py```
4. Modify the ***HOMEPATH*** (where you want to save the data to) and the configurations related to the MQTT broker at the top the code.
5. Run the python program. If it runs sucessfully, it will save received messaged in files under ***HOMEPATH***.

## NodeMCU MQTT Client
1. Connect a BME280 board to the NodeMCU via I2C.  
2. Download Arduino IDE if you haven't done so from https://www.arduino.cc/en/software
3. Download the example code: ```bme280_mqtt.ino```
4. Open the example file in Arduino IDE. Choose the correct COM port and board NodeMCU 1.0.
5. Modify the wifi configuration and also the configurations related to MQTT server at the top of the program.
6. Save the file and upload. You can use the serial monitor to observe if the program publish sensor data correctly. 
