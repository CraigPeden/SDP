//
// Turn on/off the LED on pin 13 by command received from the radio
//  0 turns the LED off
//  1 turns the LED on
//  any other character sent has no effect
//

/*	8 bit string of ASCII characters
	|	1 char	|	3 char	|
	|	OPCODE	|	Argument|

	OPCODE is 0-padded to 3 chars.
	ARGUMENT is 0-padded to 5 chars.

	OPCODES
	0 |	LED 			| Arguments = 0/1 off/on 	|
	1 | Kicker 			| Arguments = 1 to fire 	|
	2 | Left Rotational Motor	| Arguments = 0-360 degrees	|
	3 | Left Power Motor		| Arguments = 0/1 off/on 	|
	4 | Right Rotational Motor	| Arguments = 0-360 degrees	|
	5 | Right Power Motor		| Arguments = 0/1 off/on 	|
	6 | UNDEFINED 			| Arguments = UNDEFINED		|
	7 | UNDEFINED			| Arguments = UNDEFINED		|
*/

#include "SDPArduino.h"
#include <Wire.h>

byte msg;  // the command buffer
byte SIG = 0b11000000;

/* BIT MASKS FOR OPCODES */
byte KICKER_MASK = 0b00110000;
byte ROT_MASK = 0b00100000;
byte MOTOR_MASK = 0b00010000;
byte LED_MASK = 0b00000000;

/* PIN DEFINITION */
int LED_PIN = 13;

void setup()
{
  SDPsetup();
  pinMode(13, OUTPUT);   // initialize pin 13 as digital output (LED)  
  Serial.println("STARTED_OUR");
}

int get_arg(byte msg)
{
  return (int)(msg & 0b00001111);
}

void blinkLED(int n)
{
  while(n--)
  {
    digitalWrite(13, HIGH);
    delay(500);
    digitalWrite(13, LOW);
    delay(500);
  }
}

void loop()
{
 /* if (Serial.available()>0) // character received
  {
    msg = Serial.read();
    
    //check if it's our message
    if((msg & SIG) == SIG)
    {
    //  Serial.println(msg, BIN);
      //Serial.println(KICKER_MASK, BIN);
      //Serial.println((msg & KICKER_MASK), BIN);
     
     if((msg & KICKER_MASK) == KICKER_MASK)
     {
       Serial.println("KICKER");
     }
     else if((msg & ROT_MASK) == ROT_MASK)
     {
       Serial.println("ROTATION");
     }
     else if((msg & MOTOR_MASK) == MOTOR_MASK)
     {
       Serial.println("MOTOR");
     }   
     else if((msg & LED_MASK) == LED_MASK)
     {
       Serial.println("LED");
       blinkLED(get_arg(msg));
     }
    }
  }*/
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
     else if((msg & MOTOR_MASK) == MOTOR_MASK)
     {
       motorForward(0, 50);
       motorForward(1, 50);
       //Serial.println("MOTOR");
     }   
     else if((msg & LED_MASK) == LED_MASK)
     {
       //Serial.println("LED");
       blinkLED(get_arg(msg));
     }
    }
  }
}


