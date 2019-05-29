#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
//monitor_speed = 115200
const char* ssid = "Papa Smerf", *password = "szybkiinternet";
WiFiUDP Udp;
char recDataUart[255];

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

uint8_t i = 0;
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
      Udp.beginPacket("192.168.137.1", 5005);
      Udp.write(recDataUart);
      Udp.endPacket();
    }
    else
      ++i;
  }
}
