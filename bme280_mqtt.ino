/*
  NodeMCU MQTT Demo Code

  Read temperature, pressure, and humidity data from an BME280 via I2C 
  and publish messages using a MQTT client via a MQTT broker. 

  Modified July 24 2023 by Jin Zhu

  This example code is under MIT license and available at 
  https://github.com/JZ2211/IIoT_wk6/bme280_mqtt.ino

*/

#include <ESP8266WiFi.h>        // Include the Wi-Fi library
#include <PubSubClient.h>       // Include the Pub Sub Client library
#include <include/WiFiState.h> // WiFiState structure details

//libraries for BME280
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

#define NOT_CONNECTED 0
#define CONNECTED 1
#define DURATION 15000 //the duration in milliseconds between two sensor data messages. 
//For example, 5000 means there is 5 second delay between messaages

//Modify WiFi configuration as needed
const char* ssid     = "wifi_name";         // The SSID (name) of the Wi-Fi network you want to connect to
const char* password = "wifi_password";     // The password of the Wi-Fi network

//Modify the following for the MQTT settings
const char* mqtt_server = "192.168.1.2";       // IP of the MQTT broker
const char* mqtt_username = "user1";           // MQTT username
const char* mqtt_password = "workshop";     // MQTT password
const char* pubTopic = "workshop/bme280";
const char* clientID = "nodeMCU1";           // MQTT client ID, change this per node

//counter used to control the number of milliseconds passed before next message is published
unsigned long lastMsg = 0; 

int count; 

WiFiClient wifiClient;   //declare the WiFiClient object
PubSubClient client(mqtt_server, 1883, wifiClient);   //Sets up mqtt client with WiFi information, mqtt server IP, and default mqtt port: 1883
Adafruit_BME280 bme280;  //declare the BME280 object

void setup() {
  Serial.begin(115200);         // Start the Serial communication to send messages to the computer
  while (!Serial) {} //wait till serial is connected  
  delay(10);  //delay 10 milliseoncds to make sure serial port is connected
  Serial.println("start...."); // for debugging

  //Connection Wi-Fi network
  WiFi.begin(ssid, password);             // Connect to the network
  Serial.print("Connecting to ");
  Serial.print(ssid); Serial.println(" ...");

  int i = 0; // Displays the number very 0.5 seconds while the mcu connecting
  while (WiFi.status() != WL_CONNECTED) { // Wait for the Wi-Fi to connect
      delay(500);
      Serial.print(++i); Serial.print(' ');
  }
  Serial.println("WiFi conected!!");
  Serial.print("IP address:\t");
  Serial.println(WiFi.localIP());  // check the IP address of the ESP8266 and send it to the serial monitor

  char status=bme280.begin();
  while (!status){
        Serial.println("Could not find a valid BME280 sensor, check wiring, address, sensor ID!");
        Serial.print("SensorID was: 0x"); 
        Serial.println(bme280.sensorID(),16);
        Serial.print("        ID of 0xFF probably means a bad address, a BMP 180 or BMP 085\n");
        Serial.print("        ID of 0x56-0x58 represents a BMP 280,\n");
        Serial.print("        ID of 0x60 represents a BME 280.\n");
        Serial.print("        ID of 0x61 represents a BME 680.\n");
        while (1) delay(10);  //stop the code here if BME280/680 is not found
  }
}

// Method to connect to the broker
bool connect_MQTT(){
  Serial.print("attempting MQTT connection... ");
  if (client.connect(clientID, mqtt_username, mqtt_password)) {
    Serial.println("Connected to MQTT Broker!");
    return CONNECTED; //connected sucessfully
  }
  else {
    Serial.println("Connection to MQTT Broker failed...");
    return NOT_CONNECTED; //failed to connect
  }
}


//the loop() function will repeat running forever
void loop() {
  //unsigned int temperature, pressure, humidity;
  float temperature, pressure, humidity; 

  if ((WiFi.status() == WL_CONNECTED) && WiFi.localIP())
  {
    bool connection;
    while (!client.connected()) 
    {  //if client is not connected yet
      Serial.print("client not connected yet. ");
      connection = connect_MQTT(); // call the connect_MQTT method to connect to the broker
      if (!connection) //if still do not success, try again in 5 seconds
          {  
            Serial.println(client.state());
            Serial.println("try again in 5 seconds");
            delay(5000); 
          }
    } //only continue when MQTT is connected sucessfully
    client.loop();

    unsigned long now = millis(); 
    if (now - lastMsg > DURATION)  //data are updated periodically with DURATION milliseconds
    {
      lastMsg = now; 
      
      temperature = bme280.readTemperature(); 
      pressure = bme280.readPressure();
      humidity = bme280.readHumidity();
      
      String message = String(clientID) + ", Temperature (degC), " + String(temperature) +",  Humidity (%), " + String(humidity) + ",  Pressure (Pa), "+String(pressure);
      //send the data updates to the serial monitor along with the time stamps
      Serial.print("Time Stamp(s)");
      Serial.println(millis()/1000);
      Serial.print(message); 
      count++;

      if (client.publish(pubTopic,message.c_str()))
      {
        Serial.println(" bme280 data sent!");
      }
      else
      {
        Serial.println("Failed to send....");  //it should not fail in general since we only continue to data transfer when MQTT is connected
      }
    }    
  }
  else 
  {
    Serial.println("Wi-Fi connection is lost...");
  }  

}
