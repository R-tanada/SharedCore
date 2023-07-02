#include <Adafruit_NeoPixel.h>

const int LED_PIN = 2;
const int LED_COUNT = 4;

int OP1Flag = 0;
int OP2Flag = 0;

Adafruit_NeoPixel pixels(LED_COUNT * 2, LED_PIN, NEO_GRB + NEO_KHZ800);

void setup()
{
    pixels.begin();
    Serial.begin(115200);
}

void loop()
{
    int inputmode = Serial.read();
    if (inputmode != -1)
    {
        Serial.println(inputmode);
        if (inputmode == 49)
        {
            OP1Flag = 0;
            OP2Flag = 0;
        }
        else if (inputmode == 50)
        {
            OP1Flag = 1;
            OP2Flag = 0;
        }
        else if (inputmode == 51)
        {
            OP1Flag = 0;
            OP2Flag = 1;
        }
        else if (inputmode == 52)
        {
            OP1Flag = 1;
            OP2Flag = 2;
        }

        for (int i = 0; i < LED_COUNT; i++)
        {
            pixels.setPixelColor(i, pixels.Color(255 * OP1Flag, 100 * OP1Flag, 0));
            pixels.show();
        }
        for (int i = 4; i < LED_COUNT + 4; i++)
        {
            pixels.setPixelColor(i, pixels.Color(0, 255 * OP2Flag, 255 * OP2Flag));
            pixels.show();
        }
    }
}
