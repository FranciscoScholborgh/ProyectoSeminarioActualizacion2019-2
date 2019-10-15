const int ledPIN = 3;
const int magneticSensor = 4;
boolean state;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);    //iniciar puerto serie
  pinMode(ledPIN, OUTPUT);  //definir pin como salida
  pinMode(magneticSensor, INPUT_PULLUP);
  delay(250);
  Serial.println("Key;");
}

void alarma() {
    digitalWrite(ledPIN, HIGH);   // poner el Pin en HIGH
    delay(100);                   // esperar un segundo
    digitalWrite(ledPIN, LOW);    // poner el Pin en LOW
    delay(100);                   // esperar un segundo
}

void loop() {
  // put your main code here, to run repeatedly:
  state = digitalRead(magneticSensor);
  
  if (state == HIGH){
    //tone(buzzer, 400);
    alarma();
    Serial.println("BREAK IN;");
  }
  else{
    //noTone(buzzer);
    //desactivarAlarma()
    Serial.println("LOCKED;");
  }
  delay(250);
}
