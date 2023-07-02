#include <Adafruit_NeoPixel.h>

const int LED_PIN = 2;
const int LED_COUNT = 38;

int CNT = 0;
int ID = 0;

Adafruit_NeoPixel pixels(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

void setup()
{
    pixels.begin();
    Serial.begin(115200);
}

void loop()
{
    Serial.println(ID);
    int serial_input = Serial.read();
    if (serial_input != -1)
    {
        if (serial_input == 49)
        {
            ID = 1;
        }
        else if (serial_input == 50)
        {
            ID = 2;
        }
    }
    else
    {
        CNT += 1;
        delay(100);
        if (CNT > 50)
        {
            ID = 0;
            CNT = 0;
        }
    }

    if (CNT == 0)
    {
        for (int i = 0; i < LED_COUNT; i++)
        {
            pixels.setPixelColor(i, pixels.Color(0, 255, 0));
            pixels.show();
        }
    }
    else if (CNT == 1)
    {
        for (int i = 0; i < LED_COUNT; i++)
        {
            pixels.setPixelColor(i, pixels.Color(255, 100, 0));
            pixels.show();
        }
    }
    else if (CNT == 2)
    {
        for (int i = 0; i < LED_COUNT; i++)
        {
            pixels.setPixelColor(i, pixels.Color(0, 255, 255));
            pixels.show();
        }
    }
}
