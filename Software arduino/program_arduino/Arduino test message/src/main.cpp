#include <Arduino.h>

#define NR_ROOMS 4
#define NR_SENSORS 9
const char *rooms[NR_ROOMS] = {"Pokoj ", "Kuchnia ", "Lazienka ", "Przedpokoj "};
const char *sensors[NR_SENSORS] = {"Temperatura ", "Cisnienie ", "Smog ", "CO2 ", "Wilgotnosc ", "Alkohol ",
                          "Halas ", "Dym ", "Swiatlo "};
const char *command[2] = {"Za malo", "Za duzo"}; 
uint16_t values[9];

void setup() {
  for(uint8_t i = 0; i < 9; ++i)
    values[i] = 0;
  Serial.begin(115200);
}

void loop() {
  for(uint8_t room_number = 0; room_number < 4; ++room_number)
  {
    for(uint8_t sensor_nr = 0; sensor_nr < NR_SENSORS; ++sensor_nr)
      Serial.println(String("") + rooms[room_number] + " " + sensors[sensor_nr] + " " + values[sensor_nr] + " " + command[1]);
      
    ++values[0]; values[0] %= 40;
    values[1] += 20;
    if(values[1] == 1100)
      values[1] = 900;
    values[2] += 5; values[2] %= 100;
    values[3] += 10; values[3] %= 2000;
    values[4] += 2; values[4] %= 100;
    ++values[5]; values[5] %= 3;
    values[6] += 4; values[6] %= 150;
    ++values[7]; values[8] %= 10;
    values[8] += 50; values[8] %= 2000;
  }
  delay(1000);
}
