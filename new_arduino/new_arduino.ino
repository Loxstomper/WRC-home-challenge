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
                          {"claw", 6, 36, 34, 0}
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

void drop_arm()
{
    /* full extend te motors, for the second motor wait until button is pressed */

}

void raise_arm()
{

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
    }

    //   Serial.println("US");
    //   Serial.println(us[0].value);

    poll_cs();
    poll_us();


}
