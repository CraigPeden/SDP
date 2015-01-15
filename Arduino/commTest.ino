//
// Turn on/off the LED on pin 13 by command received from the radio
//  0 turns the LED off
//  1 turns the LED on
//  any other character sent has no effect
//
byte msg;  // the command buffer
void setup()
{
  pinMode(13, OUTPUT);   // initialize pin 13 as digital output (LED)
  pinMode(8, OUTPUT);    // initialize pin 8 to control the radio
  digitalWrite(8, HIGH); // select the radio
  Serial.begin(115200);    // start the serial port at 115200 baud (correct for XinoRF and RFu, if using XRF + Arduino you might need 9600)
  
  Serial.print("STARTED");
}
void loop()
{
  if (Serial.available()>=1) // character received
  {
    msg = (char)Serial.read();
    if (msg == '0')  // turn LED off
    {
      digitalWrite(13, LOW);
      Serial.print("  LED OFF  ");
    }
    else if (msg == '1')  // turn LED on
    {
      digitalWrite(13, HIGH);
      Serial.print("  LED ON   ");
    }  
  }
}


