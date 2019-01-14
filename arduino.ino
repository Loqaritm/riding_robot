#include <DallasTemperature.h>
#include <OneWire.h>

#define trigPin 12
#define echoPin 9
int dcLeft = 10;
int dcRight = 11;
short int leftMotor;
short int rightMotor;
bool moving = false;
bool idle = true;

OneWire oneWire(2); 
DallasTemperature sensors(&oneWire);

void setup() {
  Serial.begin(9600);
  String readString;
//  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(dcLeft, OUTPUT);
  pinMode(dcRight, OUTPUT);
  pinMode(trigPin, OUTPUT); //Pin, do którego podłączymy trig jako wyjście
  pinMode(echoPin, INPUT); //a echo, jako wejście
  sensors.begin();
}

int zmierzOdleglosc() {
  long czas, dystans;
   digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  czas = pulseIn(echoPin, HIGH);
  dystans = czas / 58;
  return dystans;
}

void loop() {
  String readString;
  String servo1;
  String servo2;

  long dyst = zmierzOdleglosc();
    //Serial.println(zmierzOdleglosc());
    if (dyst < 10){
      leftMotor = 0;
      rightMotor = 0;
      analogWrite(dcRight, 0);
      delay(50);
      analogWrite(dcLeft, 0);
      delay(50);
      idle = true;
    }
    delay(50);
    sensors.requestTemperatures();
    Serial.println(sensors.getTempCByIndex(0));
  
  while (Serial.available() > 0) {
    delay(3);  //delay to allow buffer to fill 
    if (Serial.available() >0) {
      char c = Serial.read();  //gets one byte from serial buffer
      readString += c; //makes the string readString
    } 
  }

  if (readString.length() >0) {
      
      if(readString == "up"){
//        Serial.println("received up");
//        digitalWrite(LED_BUILTIN, HIGH);
        idle = false;
        if(leftMotor <= 245){
          if(leftMotor == 0){
            leftMotor = 100;
          }
          leftMotor +=10;
        }
        if(rightMotor <= 245){
          if(rightMotor == 0){
            rightMotor = 100;
          }
          rightMotor +=10;
        }
      }
      else if(readString == "down"){
//        Serial.println("received down");
//        digitalWrite(LED_BUILTIN, LOW);
        if(leftMotor >= 10){
          leftMotor -= 10;
        }
        else{
          leftMotor = 0;
        }
        if(rightMotor >= 10){
          rightMotor -=10;
        }
        else{
          rightMotor = 0;
        }
        if(leftMotor == 0 && rightMotor == 0){
          moving = false;
          idle = true;
        }
      }
      else if(readString == "left"){
//        Serial.println("received left");
        if(leftMotor > rightMotor && leftMotor >= 10){
          leftMotor -= 10;
        }
        else if(leftMotor < 10){
          leftMotor = 0;
          moving = false;
        }
        else if(rightMotor <= 245){
          rightMotor += 10;
        }
      }
      else if(readString == "right"){
//        Serial.println("received right");
        if(rightMotor > leftMotor && rightMotor >= 10){
          rightMotor -=10;
        }
        else if(rightMotor < 10){
          rightMotor = 0;
          moving = false;
        }
        else if(leftMotor <= 245){
          leftMotor += 10;
        }
      }
      
//      Serial.println("otrzymano wiadomosc");  //print to serial monitor to see number results
      
    readString="";
  }
  if(!idle){
    if(!moving){
      analogWrite(dcRight, 250);
      delay(50);
      analogWrite(dcLeft, 250);
      delay(50);
      moving = true;
      idle = false;
    }
    analogWrite(dcRight, rightMotor);
    delay(50);
    analogWrite(dcLeft, leftMotor);
    delay(50);         
  }
}
