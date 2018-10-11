#include "FastLED.h"

#define NUMBER_US 1
#define NUMBER_CS 3
#define NUMBER_MOTORS 5
#define NUM_LEDS 10
#define DATA_PIN 3

CRGB leds[NUM_LEDS];

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
    int enable; // pin
    int a; // pin
    int b; // pin
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

struct Button
{
    int pin;
    int value;
} typedef Button;

// -- GLOBALS -- //

Ultrasonic_Sensor us[] = {
                          {"left", 23, 22, 0},
                          {"centre", 25, 24, 0},
                          {"right", 27, 26, 0}
                         };

Colour_Sensor cs[] = {
                          {"left", A8, 0},
                          {"centre", A10, 5},
                          {"right", A12, 8}
                         };

Motor motors[] = {
                          {"left", 2, 30, 31, 0},
                          {"right", 3, 34, 35, 0},
                          {"first", 4, 40, 41, 0},
                          {"second", 5, 44, 45, 0},
                          {"claw", 6, 50, 51, 0}
                         };

Wheels wheels;
Arm arm;
Button button;

char buffer[64];
char tokens[10][10];

void setup_pins()
{
    /* iterate over motors */
    for (int i = 0; i < NUMBER_MOTORS; i ++)
    {
      pinMode(motors[i].enable, OUTPUT);
      pinMode(motors[i].a, OUTPUT);
      pinMode(motors[i].b, OUTPUT);

      motors[i].value = 0;
      analogWrite(motors[i].enable, 0);
      digitalWrite(motors[i].a, 0);
      digitalWrite(motors[i].b, 0);
    }

    /* iterate over colour sensors */
    for (int i = 0; i < NUMBER_CS; i ++)
    {
      pinMode(cs[i].pin, INPUT);
      cs[i].value = 0;
    }

    /* interate over ultrasonic sensors */
    for (int i = 0; i < NUMBER_US; i ++)
    {
      pinMode(us[i].trig, OUTPUT);
      pinMode(us[i].echo, INPUT);
      digitalWrite(us[i].trig, 0);
      us[i].value = 0;
    }

    pinMode(button.pin, INPUT);
    button.value = 0;
}

void print_cs()
{
    static int i;

    for (i = 0; i < NUMBER_CS; i ++)
    {
        Serial.println(cs[i].name);
        Serial.println(cs[i].value);
        //printf("NAME: %s PIN: %d VALUE: %d \n", cs[i].name, cs[i].pin, cs[i].value);
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
        cs[i].value = analogRead(cs[i].pin);
    }
}

void poll_us()
{
    static int i;
    static int duration;

    for (i = 0; i < NUMBER_US; i ++)
    {
        /* just randomly generating */
        //us[i].value = rand() % 100;
        digitalWrite(us[i].trig, LOW);
        delayMicroseconds(2);
        digitalWrite(us[i].trig, HIGH);
        delayMicroseconds(10);
        digitalWrite(us[i].trig, LOW);

        /* us[i].value = (pulseIn(us[i].echo, HIGH)) * 0.034/2; */
        duration = pulseIn(us[i].echo, HIGH);
        us[i].value = (duration / 2) / 29.1;
    }
}

float get_us(char* name)
{
    /* sequential search */
    static int i;

    for (i = 0; i < NUMBER_US; i ++)
    {
        if ((strcmp(us[i].name, name)) == 0)
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
        if ((strcmp(cs[i].name, name)) == 0)
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

/* sets motor speed and a/b pins */
void set_motor(char* name, int a_val, int b_val, int val)
{
    //Serial.print(name);
    //Serial.print(a_val);
    //Serial.print(b_val);
    //Serial.print(speed);

    static int i;

    // searches for the correct motors based off the name
    for (i = 0; i < NUMBER_MOTORS; i ++)
    {
      if ((strcmp(motors[i].name, name)) == 0)
      {
        // update the hbridge
        digitalWrite(motors[i].a, a_val);
        digitalWrite(motors[i].b, b_val);
        // set the speed
        analogWrite(motors[i].enable, val);

        motors[i].value = val;

        return;
      }
    }

}

void move_forward(int speed)
{
    set_motor("left", 1, 0, speed);
    set_motor("right", 0, 1, speed);
}

void move_backwards(int speed)
{
    set_motor("left", 0, 1, speed);
    // right motor is flipped
    set_motor("right", 1, 0, speed);
}

void turn_left(int speed)
{
    set_motor("left", 0, 0, 0);
    set_motor("right", 0, 1, speed);
}

void turn_right(int speed)
{
    set_motor("left", 1, 0, speed);
    set_motor("right", 0, 0, 0);
}

void move_back(int speed)
{
    /* make a and b high for both motors */
    digitalWrite(wheels.left.a, LOW);
    digitalWrite(wheels.left.b, HIGH);
    digitalWrite(wheels.right.a, LOW);
    digitalWrite(wheels.right.b, HIGH);

    /* analogwrite on the pins */
    analogWrite(wheels.left.enable, speed);
    analogWrite(wheels.right.enable, speed);
}

void stop_all_motors()
{
    for (int i = 0; i < NUMBER_MOTORS; i ++)
    {
        // first stop movement
        analogWrite(motors[i].enable, 0);
        motors[i].value = 0;
        // set dir pins to low
        digitalWrite(motors[i].a, LOW);
        digitalWrite(motors[i].b, LOW);
    }
}

void extend_claw(int speed)
{
    set_motor("claw", 0, 1, speed);
}

void bend_claw(int speed)
{
    set_motor("claw", 1, 0, speed);
}

void extend_elbow(int speed)
{
    set_motor("second", 1, 0, speed);
}

void bend_elbow(int speed)
{
    set_motor("second", 0, 1, speed);
}

void extend_arm(int speed)
{
    set_motor("first", 1, 0, speed);
}

void bend_arm(int speed)
{
    set_motor("first", 0, 1, speed);
}

void drop_arm()
{
    set_motor("first", 1, 0, 200);
    delay(1700);
    set_motor("first", 0, 0, 0);
    set_motor("second", 1, 0, 200);
    delay(2100);
    set_motor("second", 0, 0, 0);
    //delay(500);
    set_motor("second", 0, 1, 100);
    delay(1000);
    set_motor("second", 0, 0, 0);
}

void open_claw()
{
  set_motor("claw", 1, 0, 200);
  delay(1000);
  set_motor("claw", 0, 0, 0);
}

void alarm_leds()
{
  for (int i = 0; i < 10; i ++)
  {
      for (int j = 0; j < NUM_LEDS; j ++)
      {
        leds[j] = CRGB::Red;
      }
      
      FastLED.show();
      delay(250);

      for (int j = 0; j < NUM_LEDS; j ++)
      {
        leds[j] = CRGB::Blue;
      }
      
      FastLED.show();
      delay(250);    
  }

  FastLED.clear();
  FastLED.show();

}


void setup()
{
    Serial.begin(9600);

    // put your setup code here, to run once:
    wheels.left = motors[0];
    wheels.right = motors[1];

    arm.first = motors[2];
    arm.second = motors[3];
    arm.claw = motors[4];

    setup_pins();
    FastLED.addLeds<WS2812B, DATA_PIN, GRB>(leds, NUM_LEDS);
    FastLED.setBrightness(32);
    FastLED.clear();
    FastLED.show();
}

void get_args()
{
    static int position;
    static char temp[64];
    char* arg;

    position = 0;

    /* probably dont need to conserve the buffer */
    /* strcpy(temp, buffer); */

    /* Serial.print("SOURCE: "); */
    /* Serial.println(buffer); */

    arg = strtok(buffer, ":");

    while (arg != NULL)
    {
        strcpy(tokens[position], arg);
        position ++;
        arg = strtok(NULL, ":");
    }

    /* tokens[position + 1] = '\0'; */

    /* for (int i = 0; i < position; i ++) */
    /* { */
    /*     Serial.println(tokens[i]); */
    /* } */
}


void loop()
{
    char x;
    int arg_count;
    int pos;
    // put your main code here, to run repeatedly:
    if (Serial.available() > 0)
    {
        pos = 0;

        while (Serial.available())
        {
           buffer[pos] = Serial.read();
           pos ++;
           delay(5);
        }

        buffer[pos + 1] = '\0';

        get_args();



        if ((strcmp("GET", tokens[0])) == 0)
        {
            if ((strcmp("US", tokens[1])) == 0)
            {
                Serial.println(get_us(tokens[2]));
            }
            else if ((strcmp("CS", tokens[1])) == 0)
            {
                Serial.println(get_cs(tokens[2]));
            }
        }
        else if ((strcmp("SET", tokens[0])) == 0)
        {
            if ((strcmp("M", tokens[1])) == 0)
            {
                // name, a, b, speed
                set_motor(tokens[2], atoi(tokens[3]), atoi(tokens[4]), atoi(tokens[5]));
            }

        }
        else if ((strcmp("FORWARD", tokens[0])) == 0)
        {
            move_forward(atoi(tokens[1]));
        }
        else if ((strcmp("BACKWARDS", tokens[0])) == 0)
        {
            move_backwards(atoi(tokens[1]));
        }
        else if ((strcmp("LEFT", tokens[0])) == 0)
        {
            turn_left(atoi(tokens[1]));
        }
        else if ((strcmp("RIGHT", tokens[0])) == 0)
        {
            turn_right(atoi(tokens[1]));
        }
        // STOP:ALL:
        else if ((strcmp("STOP", tokens[0])) == 0)
        {
            if ((strcmp("ALL", tokens[1])) == 0)
            {
                stop_all_motors();
            }
        }
        // CLAW MESSAGES
        else if((strcmp("E", tokens[0])) == 0)
        {
            if((strcmp("C", tokens[1])) == 0)
            {
                extend_claw(atoi(tokens[2]));
            }
            else if((strcmp("E", tokens[1])) == 0)
            {
                extend_elbow(atoi(tokens[2]));
            }
            else if((strcmp("A", tokens[1])) == 0)
            {
                extend_arm(atoi(tokens[2]));
            }
        }
        else if((strcmp("B", tokens[0])) == 0)
        {
            if((strcmp("C", tokens[1])) == 0)
            {
                bend_claw(atoi(tokens[2]));
            }
            else if((strcmp("E", tokens[1])) == 0)
            {
                bend_elbow(atoi(tokens[2]));
            }
            else if((strcmp("A", tokens[1])) == 0)
            {
                bend_arm(atoi(tokens[2]));
            }
        }
        else if ((strcmp("S", tokens[0])) == 0)
        {
            drop_arm();
        }
        else if ((strcmp("Z", tokens[0])) == 0)
        {
            open_claw();
        }
        else if ((strcmp("L", tokens[0])) == 0)
        {
            alarm_leds();
        }
    }

    //   Serial.println("US");
    //   Serial.println(us[0].value);

    poll_cs();
    poll_us();
}
