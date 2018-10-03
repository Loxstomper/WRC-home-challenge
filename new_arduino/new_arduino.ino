#include <string.h>

#define NUMBER_US 1
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

// -- GLOBALS -- //

Ultrasonic_Sensor us[] = {
                          {"left", 53, 51, 0},
                          {"centre", 49, 47, 0},
                          {"right", 45, 43, 0}
                         };

Colour_Sensor cs[] = {
                          {"left", A0, 0},
                          {"centre", A1, 5},
                          {"right", A2, 8}
                         };

Motor motors[] = {
                          {"left", 2, 52, 50, 0},
                          {"right", 3, 48, 46, 0},
                          {"first", 4, 44, 42, 0},
                          {"second", 5, 40, 38, 0},
                          {"claw", 6, 36, 34`, 0}
                         };

Wheels wheels;
Arm arm;

void setup_pins()
{
    /* iterate over motors */
//    for (int i = 0; i < NUMBER_MOTORS; i ++)
//    {
//      pinMode(motors[i].enable, OUTPUT);
//      pinMode(motors[i].a, OUTPUT);
//      pinMode(motors[i].b, OUTPUT);
//
//      motors[i].value = 0;
//      analogWrite(motors[i].enable, 0);
//      digitalWrite(motors[i].a, 0);
//      digitalWrite(motors[i].b, 0);
//    }
    /* iterate over colour sensors */
    for (int i = 0; i < NUMBER_CS; i ++)
    {
      pinMode(cs[i].pin, INPUT);
      cs[i].value = 0;
    }
    /* interate over ultrasonic sensors */
//    for (int i = 0; i < NUMBER_US; i ++)
//    {
//      pinMode(us[i].trig, OUTPUT);
//      pinMode(us[i].echo, INPUT);
//      digitalWrite(us[i].trig, 0);
//      us[i].value = 0;
//    }
}

void setup_motors()
{
    for (int i = 0; i < NUMBER_MOTORS; i ++)
    {
        // digital write a and b to be 0
        motors[i].value = 0;
        analogWrite(motors[i].enable, motors[i].value);
    }
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

    for (i = 0; i < NUMBER_US; i ++)
    {
        /* just randomly generating */
        //us[i].value = rand() % 100;
        digitalWrite(us[i].trig, LOW);
        delayMicroseconds(2);
        digitalWrite(us[i].trig, HIGH);
        delayMicroseconds(10);
        digitalWrite(us[i].trig, LOW);

        us[i].value = (pulseIn(us[i].echo, HIGH)) * 0.034/2;
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
    digitalWrite(wheels.left.a, HIGH);
    digitalWrite(wheels.left.b, HIGH);
    digitalWrite(wheels.right.a, HIGH);
    digitalWrite(wheels.right.b, HIGH);

    /* analogwrite on the pins */
    analogWrite(wheels.left.enable, speed);
    analogWrite(wheels.right.enable, speed);
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

}

void loop() 
{
  char x;
  String str;
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0)
  {
    //x = Serial.read();
    str = Serial.readString();
    // GET US [NAME]
    // GET CS [NAME]
    // SET M [NAME] [F/B]
    if (str == "GET")
    {
      Serial.println("GETTING");
      print_cs();
    }
    else if (str == "SET")
    {
      Serial.println("SETTING");
    }
    else if (str == "FORWARD")
    {
      Serial.println("MOVING FORWARD");
      move_forward(200);
    }
    
    
    Serial.println(str);
    
    
  }

  Serial.println("US");
  Serial.println(us[0].value);
  
  poll_cs();
  poll_us();
  

}
