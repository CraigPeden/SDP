int IRpin = A0;               // IR photodiode on analog pin A0
int LEDpin = 12;
int IRemitter = 13;           // IR emitter LED on digital pin 2
byte buffer = 0;
unsigned long IRtimer = millis();
boolean IRtoggle = false;

void setup(){
  //Serial.begin(9600);         // initializing Serial monitor
  pinMode(IRemitter,OUTPUT);  // IR emitter LED on digital pin 2
  pinMode(LEDpin,OUTPUT);  // IR emitter LED on digital pin 2
  digitalWrite(LEDpin, LOW);
  digitalWrite(IRemitter, LOW);// setup IR LED
}

void loop(){
  
  if (IRtimer + 10 < millis()) {
    IRtimer = millis();
    
    buffer += readIR();
    buffer <<= 1;
    
    if(buffer) {
      digitalWrite(LEDpin, HIGH);
    } else {
      digitalWrite(LEDpin, LOW);
    }
  }
}

int readIR(){
  int out = analogRead(IRpin);  // storing IR coming from the obstacle
  //Serial.println(out);
  // toggle to reset the transistors value.
  IRtoggle = !IRtoggle;
  digitalWrite(IRemitter,IRtoggle);
  
  // possitive if IR connection
  return out < 100;
}
