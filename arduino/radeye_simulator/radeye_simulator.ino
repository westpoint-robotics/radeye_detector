void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);           // set up Serial library at 9600 bps
  randomSeed(analogRead(0));

}

void loop() {
  int num = getValue02();
  // put your main code here, to run repeatedly:
  //Serial.print(" ");
  Serial.println(num);
  //Serial.print(" 599 0 544 00  GN+ 09 \r\n");
  
  delay(1000);
}

int getValue01(){
  return random(30);  
}

int getValue02(){
  //=ROUND(SIN(C1/5000)*15+15,0)
  //int val = (sin(millis() / 5000.0) * 15 + 15);
  int val = (sin(millis() / 5000.0) * 15 + 15);
  return sin(millis()/5000) *15 + 15;  
}
