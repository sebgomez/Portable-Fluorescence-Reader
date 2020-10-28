
const int analogInPin = A0;  // ESP8266 Analog Pin ADC0 = A0
const int outputPins[] ={D0,D1,D2,D3};

int sensorValue = 0;  // lectura del potenciómetro
int outputValue = 0;  // value to output to a PWM pin
void setup() {
  // inicializa serial a 115200 bd
  Serial.begin(115200);
  for(int i=0;i<4;i++){
    pinMode(outputPins[i], OUTPUT);
  }
}

void loop() {
  // lee el valor del potenciómetro
  sensorValue = analogRead(analogInPin);
  
  // mapea a la salida de bits 
  outputValue = map(sensorValue, 0, 1023, 0, 15);
  
  // imprime en el monitor serial
  //  Serial.print("sensor = ");
  //  Serial.print(sensorValue);
  //Serial.print("\t output = ");
  //Serial.println(outputValue);
  //Serial.print(bitRead(outputValue,3));
  //Serial.print(bitRead(outputValue,2));
  //Serial.print(bitRead(outputValue,1));
  //Serial.println(bitRead(outputValue,0));

  //envía la lectura a través de los 4 pins   
  for(int i=0;i<4;i++){
    if(bitRead(outputValue,i)){
      digitalWrite(outputPins[i],HIGH);
    }else{
      digitalWrite(outputPins[i],LOW);
    }
  }

  delay(500);
}
