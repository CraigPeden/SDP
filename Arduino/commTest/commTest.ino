/*      Command byte:
	|  2 bits  |  2 bits  |  4 bits  |
	|   SIG    |  OPCODE  | ARGUMENT |

	SIG is the signature for the communication.
	OPCODE is a 2 bit unsigned int.
	ARGUMENT is a 4 bit unsigned int.

	OPCODES
	0 | Left Power Motor  | Arguments = 0-15 (7-8: STOP)|
	1 | Right Power Motor | Arguments = 0-15 (7-8: STOP)|
	2 | Rotational Motor  | Arguments = 0-14      	    |
	3 | Kicker            | Arguments = 1 to fire 	    |
*/

#include "SDPArduino.h"
#include <Wire.h>

byte msg;  // the command buffer
byte SIG = 0b11000000;

/* BIT MASKS FOR OPCODES */
byte KICKER_MASK = 0b00110000;
byte ROT_MASK = 0b00100000;
byte RIGHT_MOTOR_MASK = 0b00010000;
byte LEFT_MOTOR_MASK = 0b00000000;

void setup()
{
  SDPsetup(); 
  Serial.println("Robot started");
}

int get_arg(byte msg)
{
  return (int)(msg & 0b00001111);
}

void loop()
{

}

void controlMotor(int motor, byte msg)
{
  int motorGear = get_arg(msg);
  
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
      motorForward(motor, motorSpeed);
    }
    else    
    {
      int motorSpeed = 100 - ((motorGear * 100) / 7);
      motorBackward(motor, motorSpeed);
    }
  }
}

void serialEvent() {
 if (Serial.available()>0) // character received
  {
    msg = Serial.read();
    
    //check if it's our message
    if((msg & SIG) == SIG)
    {
      Serial.write(msg);
      //Serial.println(KICKER_MASK, BIN);
      //Serial.println((msg & KICKER_MASK), BIN);
     
     if((msg & KICKER_MASK) == KICKER_MASK)
     {
      // Serial.println("KICKER");
     }
     else if((msg & ROT_MASK) == ROT_MASK)
     {
       //Serial.println("ROTATION");
     }
     else if((msg & RIGHT_MOTOR_MASK) == RIGHT_MOTOR_MASK)
     {        
       //Serial.println("MOTOR");
       controlMotor(0, msg);
     }   
     else if((msg & LEFT_MOTOR_MASK) == LEFT_MOTOR_MASK)
     {
       //Serial.println("LED");
       controlMotor(1, msg);
     }
    }
  }
}


