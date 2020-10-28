/*********
  Rui Santos
  Complete project details at http://randomnerdtutorials.com  
*********/

const int analogInPin = A0;  // ESP8266 Analog Pin ADC0 = A0
const int outputPins[] ={D0,D1,D2,D3};

int sensorValue = 0;  // value read from the pot
int outputValue = 0;  // value to output to a PWM pin
void setup() {
  // initialize serial communication at 115200
  Serial.begin(115200);
  for(int i=0;i<4;i++){
    pinMode(outputPins[i], OUTPUT);
  }
}

void loop() {
  // read the analog in value
  sensorValue = analogRead(analogInPin);
  
  // map it to the range of the PWM out
  outputValue = map(sensorValue, 0, 1023, 0, 15);
  
  // print the readings in the Serial Monitor
//  Serial.print("sensor = ");
//  Serial.print(sensorValue);
  Serial.print("\t output = ");
  Serial.println(outputValue);
//  analogWrite(D0, sensorValue);
  Serial.print(bitRead(outputValue,3));
  Serial.print(bitRead(outputValue,2));
  Serial.print(bitRead(outputValue,1));
  Serial.println(bitRead(outputValue,0));

  for(int i=0;i<4;i++){
    if(bitRead(outputValue,i)){
      digitalWrite(outputPins[i],HIGH);
    }else{
      digitalWrite(outputPins[i],LOW);
    }
  }

  delay(500);
}
