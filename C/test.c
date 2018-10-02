#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define NUMBER_US 3
#define NUMBER_CS 3

struct Ultrasonic_Sensor
{
    char* name;
    int echo;
    int trig;
    float value; // cm

} typedef Ultrasonic_Sensor;

struct Colour_Sensor
{
    char* name;
    int pin;
    int value;

} typedef Ultrasonic_Sensor;

Ultrasonic_Sensor us[] = {
                          {"left", 1, 2, 3},
                          {"centre", 4, 5, 6},
                          {"right", 7, 8, 9}
                         };

Colour_Sensor cs[] = {
                          {"left", 1, 0},
                          {"centre", 4, 5},
                          {"right", 7, 8}
                         };


void print_cs()
{
    static i;

    for (i = 0; i < NUMBER_CS; i ++)
    {
        printf("NAME: %s PIN: %d VALUE: %d \n", cs[i].name, us[i].pin, us[i].value);
    }
}

void print_us()
{
    static i;

    for (i = 0; i < NUMBER_US; i ++)
    {
        printf("NAME: %s ECHO: %d TRIG: %d VALUE: %d \n", us[i].name, us[i].echo, us[i].trig, us[i].value);
    }
}

void poll_us()
{
    static int i;

    for (i = 0; i < NUMBER_CS; i ++)
    {
        /* just randomly generating */
        us[i].value = rand() % 1000;
    }
}

void poll_us()
{
    static int i;

    for (i = 0; i < NUMBER_US; i ++)
    {
        /* just randomly generating */
        us[i].value = rand() % 100;
    }
}

float get_us(char* name)
{
    /* sequential search */
    static i;

    for (i = 0; i < NUMBER_US; i ++)
    {
        if (strcmp(us[i].name, name) == 0)
        {
            return us[i].value;
        }
    }

    return -1;
}

int get_cs(char* name)
{
    /* sequential search */
    static i;

    for (i = 0; i < NUMBER_CS; i ++)
    {
        if (strcmp(cs[i].name, name) == 0)
        {
            return cs[i].value;
        }
    }

    return -1;
}


int main(int argc, char** argv)
{
    /* seed RNG */
    srand(time(0));
    char buffer[1024];

    while (1)
    {
        poll_us();

        printf("> ");
        fgets(buffer, 1024, stdin);

        if (buffer[0] == 'u')
        {
            print_us();
        }
    }



    


    return 0;
}
