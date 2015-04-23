#include "IRremote.h"

#define PIN_IR 3
#define PIN_DETECT A0
#define PIN_STATUS 12

IRsend irsend;
void setup()
{
  Serial.begin(9600);
  pinMode(PIN_STATUS, OUTPUT);
  irsend.enableIROut(38);
  irsend.mark(0);
}

void loop() {
  if (readIR()) {
    digitalWrite(PIN_STATUS, HIGH);
  }
  else {
    digitalWrite(PIN_STATUS, LOW);    
  }
}

int readIR(){
  int out = analogRead(PIN_DETECT);  // storing IR coming from the obstacle

  Serial.println(out);
  // toggle to reset the transistors value.
//  IRtoggle = !IRtoggle;
//  digitalWrite(IRemitter,IRtoggle);
  
  // possitive if IR connection
  return out < 100;
}
