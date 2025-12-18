#include <Arduino.h>

const int POT = 4;

void setup()
{
    Serial.begin(9600);
}

void loop()
{
    int reading = analogRead(POT);
    int level = map(reading, 0, 4095, 0, 100);
    char buf[8] = {0};
    itoa(level, buf, 10);
    strcat(buf, "\n");
    Serial.print(buf);
}
