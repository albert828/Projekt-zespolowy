#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <SoftwareSerial.h>

#define KOMPILACJA 0
#define PRINT_TIME 500

const char* ssid = "Papa Smerf";
const char* password = "szybkiinternet";

WiFiUDP Udp;

char incomingPacket[255];  // buffer for incoming packets
char recDataUart[255];
void setup()
{
  Serial.begin(115200);
  Serial.println();

  Serial.printf("Connecting to %s ", ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" connected");
}

uint32_t actualTime, previousTime;
uint16_t counter = 0;
uint8_t i = 0;
void loop()
{
  #if KOMPILACJA == 1
  actualTime = millis();
  int packetSize = Udp.parsePacket();
  if (packetSize)
  {
    // receive incoming UDP packets
    Serial.printf("Received %d bytes from %s, port %d\n", packetSize, Udp.remoteIP().toString().c_str(), Udp.remotePort());
    int len = Udp.read(incomingPacket, 255);
    if (len > 0)
    {
      incomingPacket[len] = 0;
    }
    Serial.printf("UDP packet contents: %s\n", incomingPacket);

    // send back a reply, to the IP address and port we got the packet from
    Udp.beginPacket("127.0.0.1", 5005);
    Udp.write("Test");
    Udp.endPacket();
  }
  if((actualTime - previousTime) > PRINT_TIME)
  {
    previousTime = actualTime;
    Udp.beginPacket("192.168.137.1", 5005);
    Udp.write("Test ");
    Udp.write(counter);
    Udp.endPacket();
    ++counter;
  }
  Serial.println("Nie powinienem tu byc");
  #endif
  
  if(Serial.available() > 0)
  {
    recDataUart[i] = Serial.read();
    //++i;
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
    //Udp.beginPacket("192.168.137.1", 5005);
    //Udp.write("Resending by ESP : ");
    //Udp.write(Serial.read());
    //Udp.endPacket();
  }
}
