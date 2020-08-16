#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
//monitor_speed = 115200
/**
 * @brief Contains WiFi name
 * 
 */
const char* ssid = "CBA";
/**
 * @brief Contains WiFi password
 * 
 */
const char *password = "szybkiinternet";
/**
 * @brief Wifi comunication object
 * 
 */
WiFiUDP Udp;
/**
 * @brief Buffer for recived data from serial port
 * 
 */
char recDataUart[255];
/**
 * @brief Setup function. Starts serial cominication. Starts WiFi comunication.
          Waits for correct conection with WiFi network
 * 
 */
void setup()
{
  Serial.begin(115200);
  Serial.printf("Connecting to %s ", ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" connected");
}
/**
 * @brief Contains numer of received characters from serial port
 * 
 */
uint8_t i = 0;
/**
 * @brief Main function. Reads data from serial port and resends it via UDP.
 * 
 */
void loop()
{ 
  if(Serial.available() > 0)
  {
    recDataUart[i] = Serial.read();
    if (recDataUart[i] == '\n') 
    {
      ++i;
      recDataUart[i] = '\0';
      i = 0;
      Serial.print(recDataUart);
      Udp.beginPacket("raspoka.ddns.net", 32998);
      Udp.write(recDataUart);
      Udp.endPacket();
    }
    else
      ++i;
  }
}
