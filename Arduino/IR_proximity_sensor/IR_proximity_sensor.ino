#include "IRremote.h"

int IRpin = A0;               // IR photodiode on analog pin A0
int LEDpin = 12;
// IR emitter LED on digital pin 3

unsigned long IRtimer = millis();
boolean IRtoggle = false;
byte IRbuffer = 0;

IRsend irsend;
void setup(){
  Serial.begin(9600);         // initializing Serial monitor
  pinMode(LEDpin,OUTPUT);  // IR emitter LED on digital pin 2
  digitalWrite(LEDpin, LOW);
  irsend.enableIROut(38);
  irsend.mark(0);
}

void loop(){
    /* Update IR */
  if (IRtimer + 10 < millis()) {
    IRtimer = millis();
    
    if (IRtoggle) {
      IRbuffer += readIR();
      IRbuffer <<= 1;
      irsend.space(0);
      
    } else {
      readIR();
      irsend.mark(0);
    }
    
    IRtoggle = !IRtoggle;
    
    if (IRbuffer)
      digitalWrite(LEDpin, HIGH);
    else
      digitalWrite(LEDpin, LOW);
  }

}

int readIR(){
  int out = analogRead(IRpin);  // storing IR coming from the obstacle
  
  Serial.println(out);
  
  // possitive if IR connection
  return out < 100;
}
