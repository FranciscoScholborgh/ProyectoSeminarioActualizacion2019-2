int x = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  delay(1000);
  Serial.println("Key;");
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("Hola Python, Yo Arduino te saludo :v" + String(++x) +";");
  delay(1000);
}
