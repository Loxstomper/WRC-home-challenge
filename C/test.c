#include <stdio.h>
#include <stdlib.h>
#include <time.h>


#define NUMBER_US 3

struct Ultrasonic_Sensor
{
    char* name;
    int echo;
    int trig;
    int value;

} typedef Ultrasonic_Sensor;

Ultrasonic_Sensor us[] = {
                          {"left", 1, 2, 3},
                          {"centre", 4, 5, 6},
                          {"right", 7, 8, 9}
                         };


void print_us()
{
    for (int i = 0; i < NUMBER_US; i ++)
    {
        printf("NAME: %s ECHO: %d TRIG: %d VALUE: %d \n", us[i].name, us[i].echo, us[i].trig, us[i].value);
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
