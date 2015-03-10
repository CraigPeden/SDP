
/*      Command byte:
	|  1 bit  |  1 bit   |  2 bits  |  4 bits  |
	|   SIG   | CHECKSUM |  OPCODE  | ARGUMENT |

	SIG is the signature of our communication, the value is 1
	CHECKSUM is number of set bits (OPCODE ARGUMENT) % 2
	OPCODE is a 2 bit unsigned int.
	ARGUMENT is a 4 bit unsigned int.

	OPCODES
	1 | Left Power Motor  | Arguments = 0-15 (7-8: STOP)|
	2 | Right Power Motor | Arguments = 0-15 (7-8: STOP)|
	3 | Kicker            | Arguments = 1 to fire 	    |
*/

#include "SDPArduino.h"
#include <Wire.h>

byte msg;  // the command buffer
byte SIG_MASK = 0b10000000;
byte CHECKSUM_MASK = 0b01000000;
byte PAYLOAD_MASK = 0b00111111;

/* BIT MASKS FOR OPCODES */
byte KICKER_MASK = 0b00110000;
byte RIGHT_MOTOR_MASK = 0b00100000;
byte LEFT_MOTOR_MASK = 0b00010000;

/* Timed action */
unsigned long kickerTime = millis();
int kickerState = 0;
boolean grabberAction = false;
unsigned long grabberTime = millis();
int grabberDown = 300;
int grabberUp = 500;
int kickerKick = 200;
int kickerRetract = 180;
int simpleKick = 500;
int simpleRetract = 500;
int kickerSleep = 100;

long readVcc() {
  long result;
  // Read 1.1V reference against AVcc
  ADMUX = _BV(REFS0) | _BV(MUX3) | _BV(MUX2) | _BV(MUX1);
  delay(2); // Wait for Vref to settle
  ADCSRA |= _BV(ADSC); // Convert
  while (bit_is_set(ADCSRA,ADSC));
  result = ADCL;
  result |= ADCH<<8;
  result = 1126400L / result; // Back-calculate AVcc in mV
  return result;
}

void setup()
{
  SDPsetup();
  Serial.println("Robot started"); 
  Serial.println( readVcc(), DEC );
}

int getArg(byte msg)
{
  return (int)(msg & 0b00001111);
}

int countSetBits(int n)
{
  int count = 0;
  while(n)
  {
    count += n & 1;
    n >>= 1;
  }
  
  return count;
}

void controlKicker(int value)
{
  if(value == 0)
  {
    /* Grabber down */
    grabberTime = millis() + grabberDown;
    grabberAction = true;
    motorForward(3,100);
  }
  else if(value == 1)
  {
    /* Grabber up */
    grabberTime = millis() + grabberUp;
    grabberAction = true;
    motorBackward(3,100);
  }
  else if(value == 2)
  {
    /* Kicker routine */
    kickerTime = millis() + kickerKick;
    kickerState = 1; //kicker is kicking
    motorBackward(2,100);
  }
  else if(value == 3)
  {
    /* Kicker simple kick */
    kickerTime = millis() + simpleKick;
    kickerState = 3;
    motorBackward(2,100);
  }
  else if(value == 4)
  {
    /* Kicker simple kick */
    kickerTime = millis() + simpleRetract;
    kickerState = 3;
    motorForward(2,100);
  }
}

void controlMotor(int motor, byte msg)
{
  int motorGear = getArg(msg);
  
  if(motorGear == 7 || motorGear == 8)
  {
     motorStop(motor);
  }
  else
  {
    if(motorGear > 7)
    {
      motorGear = 15 - motorGear;
      int motorSpeed = 100 - ((motorGear * 100) / 7);
      motorBackward(motor, motorSpeed);
    }
    else    
    {
      int motorSpeed = 100 - ((motorGear * 100) / 7);
      motorForward(motor, motorSpeed);
    }
  }
}

void loop()
{  
  /* If the kicker flag kickerAction is set,
  check if the time is reached. */
  if(kickerState != 0 && (kickerTime < millis()))
  {
    if (kickerState == 1)
    {
      // Transition from kick to sleep
      kickerTime = millis() + kickerSleep;
      kickerState = 2;
      motorStop(2);      
    }
    else if (kickerState == 2)
    {
      // Transition from sleep to retract
      kickerTime = millis() + kickerRetract;
      kickerState = 3;
      motorForward(2, 100);   
    }
    else if (kickerState == 3)
    {
      // Transition from retract to stop
      kickerState = 0;
      motorStop(2);
    }
  }
  
  /* If the grabber flag grabberAction is set,
  check if the time is reached. */
  if(grabberAction && (grabberTime < millis()))
  {
    grabberAction = false;
    motorStop(3);
  }
}

void serialEvent() {
 if (Serial.available()>0) // character received
  {
    msg = Serial.read();
    
    // Check for the signature and for the integrity of the message
    if((msg & SIG_MASK) == SIG_MASK &&
       (countSetBits((int) (msg & PAYLOAD_MASK)) % 2 == (int) ((msg & CHECKSUM_MASK) >> 6)))
    {
      Serial.write(msg);
      
      if((msg & KICKER_MASK) == KICKER_MASK)
      {
        controlKicker(getArg(msg));
      }
      else if((msg & RIGHT_MOTOR_MASK) == RIGHT_MOTOR_MASK)
      {
        controlMotor(0, msg);
      }
      else if((msg & LEFT_MOTOR_MASK) == LEFT_MOTOR_MASK)
      {
        controlMotor(1, msg);
      }
    }
  }
}


