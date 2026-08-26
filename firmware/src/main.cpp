#include <Adafruit_TinyUSB.h>
#include <Arduino.h>
#include <cstdint>

const int POT = 26;
const uint32_t LOOP_PERIOD = 50; // 100 ms
uint32_t last_loop = 0;

void setup()
{
    USBDevice.setManufacturerDescriptor("Adam Dia");
    USBDevice.setProductDescriptor("mixy Audio Dial");
    Serial.begin(9600);
    analogReadResolution(12);
}

void loop()
{
    if (millis() - last_loop > LOOP_PERIOD)
    {
        int reading = analogRead(POT);
        int level = map(reading, 0, 4095, 0, 100);
        char buf[8] = {0};
        itoa(level, buf, 10);
        strcat(buf, "\n");
        Serial.print(buf);
        last_loop = millis();
    }
}
