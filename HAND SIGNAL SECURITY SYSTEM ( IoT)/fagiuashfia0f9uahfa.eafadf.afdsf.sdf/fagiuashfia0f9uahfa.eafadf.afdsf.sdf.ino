const int ledPins[] = {8, 9, 10, 11};
const int buzzerPin = 2;
char cmd[20];
int index = 0;

void setup() {
  Serial.begin(9600);
  for(int i=0;i<4;i++) pinMode(ledPins[i],OUTPUT);
  pinMode(buzzerPin,OUTPUT);
}

void loop() {
  while(Serial.available()){
    char c = Serial.read();
    if(c=='\n'){
      cmd[index]='\0';
      processCommand(cmd);
      index=0;
    }else if(index<19){
      cmd[index++]=c;
    }
  }
}

void processCommand(char* cmd){
  if(strncmp(cmd,"FINGERS:",8)==0){
    for(int i=0;i<4;i++){
      if(i<strlen(cmd+8) && cmd[8+i]=='1') digitalWrite(ledPins[i],HIGH);
      else digitalWrite(ledPins[i],LOW);
    }
  }
  else if(strcmp(cmd,"BUZZER_WRONG")==0) tone(buzzerPin,1000,200);
  else if(strcmp(cmd,"BUZZER_SUCCESS")==0){
    tone(buzzerPin,1000,200);
    delay(250);
    tone(buzzerPin,1200,200);
    delay(250);
    tone(buzzerPin,1500,400);
  }
  else if(strcmp(cmd,"BUZZER_CRITICAL")==0){
    // Critical beep for 2 seconds
    tone(buzzerPin, 2000); // continuous 2kHz beep
    delay(2000);
    noTone(buzzerPin);
  }
}
