#include <Adafruit_TinyUSB.h>
#include <Arduino.h>

const int POT = 26;

void setup()
{
    USBDevice.setManufacturerDescriptor("Adam Dia");
    USBDevice.setProductDescriptor("mixy Audio Dial");
    Serial.begin(9600);
    analogReadResolution(12);
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
