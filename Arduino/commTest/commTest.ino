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

byte msg;  // the command buffer
void setup()
{
  pinMode(13, OUTPUT);   // initialize pin 13 as digital output (LED)
  pinMode(8, OUTPUT);    // initialize pin 8 to control the radio
  digitalWrite(8, HIGH); // select the radio
  Serial.begin(9600);    // start the serial port at 115200 baud (correct for XinoRF and RFu, if using XRF + Arduino you might need 9600)
  
  Serial.print("STARTED");
}

void blinkLED(int n)
{
  while(n--)
  {
    digitalWrite(13, HIGH);
    delay(100);
    digitalWrite(13, LOW);
  }
}

void loop()
{
  if (Serial.available()>=1) // character received
  {
    msg = (char)Serial.read();
    Serial.print((char)msg);
    if (msg == '0')  // turn LED off
    {
      blinkLED(1);
    }
    else if (msg == '1')  // turn LED on
    {
      blinkLED(2);
    }  
  }
}


