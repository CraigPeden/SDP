int IRpin = A0;               // IR photodiode on analog pin A0
int LEDpin = 12;
int IRemitter = 13;           // IR emitter LED on digital pin 2

void setup(){
  Serial.begin(9600);         // initializing Serial monitor
  pinMode(IRemitter,OUTPUT);  // IR emitter LED on digital pin 2
  pinMode(LEDpin,OUTPUT);  // IR emitter LED on digital pin 2
  digitalWrite(IRemitter,LOW);// setup IR LED
}

void loop(){
  
  if (Serial.available()>0) // character received
  {
    byte msg = Serial.read();
    
    if (msg == 48) {
        Serial.println("Testing...");
        if(readIR())
            digitalWrite(LEDpin,HIGH);
          else
            digitalWrite(LEDpin,LOW);
    }
    
  }    
}

int readIR(){
  digitalWrite(IRemitter,HIGH);
  delay(100);
  int out = analogRead(IRpin);  // storing IR coming from the obstacle
  Serial.println(out);
  digitalWrite(IRemitter,LOW);
  return out < 100;
}
