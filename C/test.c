#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

#define NUMBER_US 3
#define NUMBER_CS 3
#define NUMBER_MOTORS 5

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

} typedef Colour_Sensor;

struct Motor
{
    char* name;
    int enable;
    int a;
    int b;
    int value;

} typedef Motor;

struct Wheels
{
    Motor left;
    Motor right;

} typedef Wheels;

struct Arm
{
    Motor first;
    Motor second;
    Motor claw;

} typedef Arm;

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

Motor motors[] = {
                          {"left", 5, 1, 2, 0},
                          {"right", 6, 7, 8, 0},
                          {"first", 7, 1, 2, 0},
                          {"second", 8, 1, 2, 0},
                          {"claw", 9, 1, 2, 0}
                         };

Wheels wheels;
Arm arm;

void setup_pins()
{
    /* iterate over motors */
    /* iterate over colour sensors */
    /* interate over ultrasonic sensors */
}

void setup_motors()
{
    for (int i = 0; i < NUMBER_MOTORS; i ++)
    {
        // digital write a and b to be 0
        motors[i].value = 0
        /* analogWrite(motors[i].enable,motors[i].value); */
    }
}


void print_cs()
{
    static int i;

    for (i = 0; i < NUMBER_CS; i ++)
    {
        printf("NAME: %s PIN: %d VALUE: %d \n", cs[i].name, cs[i].pin, cs[i].value);
    }
}

void print_us()
{
    static int i;

    for (i = 0; i < NUMBER_US; i ++)
    {
        printf("NAME: %s ECHO: %d TRIG: %d VALUE: %d \n", us[i].name, us[i].echo, us[i].trig, us[i].value);
    }
}

// -- POLL SENSORS -- //

void poll_cs()
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
    static int i;

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
    static int i;

    for (i = 0; i < NUMBER_CS; i ++)
    {
        if (strcmp(cs[i].name, name) == 0)
        {
            return cs[i].value;
        }
    }

    return -1;
}

int get_button()
{
    return 1;
}

void drop_arm()
{
    /* full extend te motors, for the second motor wait until button is pressed */

}

void raise_arm()
{

}

/* sets motor speed and a/b pins */
void set_motor()
{

}

void move_forward(int speed)
{
    /* make a and b high for both motors */

    /* analogwrite on the pins */
}


int main(int argc, char** argv)
{
    /* seed RNG */
    srand(time(0));
    char buffer[1024];

    wheels.left = motors[0];
    wheels.right = motors[1];

    arm.first = motors[2];
    arm.second = motors[3];
    arm.claw = motors[4];

    poll_cs();

    while (1)
    {
        poll_us();
        poll_cs();

        printf("> ");
        fgets(buffer, 1024, stdin);

        if ((strcmp(buffer, "ultra\n") == 0))
        {
            print_us();
        }
        else if ((strcmp(buffer, "colour\n") == 0))
        {
            print_cs();
        }
        else if ((strcmp(buffer, "motor\n") == 0))
        {

        }
    }


    return 0;
}

