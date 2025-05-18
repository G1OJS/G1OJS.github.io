---
layout: default
title: "Minimal TV IR Decoder and Motor Driver using ATTiny mpc without library"
permalink: /TV_IR_Motor_tiny/
---

// TV Remote Vol up / Vol down decoder and motor driver
// for motorised volume control using ATTiny88
// and LG Magic Remote, without needing IR library

```
#define IR_PIN 24  // A5 on my board with DrAzzy core
#define LED_PIN 0  // Built in LED
#define MOTORPOS_PIN 10
#define MOTORNEG_PIN 11
#define VOL_UP 0xFA
#define VOL_DOWN 0xF8
unsigned long lastPulseDetected_ms=0;

void blinkLED_bits(unsigned long bits) {
  // blink out 8 bits for debugging, finding codes etc
  for (int i = 0; i < 8; i++) {
    digitalWrite(LED_PIN, HIGH);
    delay((bits & 255)? 300:100);
    digitalWrite(LED_PIN, LOW);
    delay((bits & 255)? 100:300);
    bits *=2;
  }
  digitalWrite(LED_PIN, LOW);
  delay(200);
}

unsigned long getAddrAndCmdWord(){
  // NEC Protocol: see https://wiki.keyestudio.com/052035_Basic_Starter_V2.0_Kit_for_Arduino#Project_14:_IR_Remote_Control
  // and note that IR module ouitput is HIGH when IR remote is OFF, and LOW when IR remote is transmitting IR
  unsigned long cmdWord;
  unsigned char i=0;
  while (digitalRead(IR_PIN)==HIGH) {};
  cmdWord=0;
  do {
    cmdWord >>= 1;
    if(pulseIn(IR_PIN, HIGH, 5000) < 1250) 
      cmdWord |=0x80000000;
  } while (i++ < 32);
  return cmdWord;
}

void motorStartRight(){
  digitalWrite(MOTORPOS_PIN,HIGH);
  digitalWrite(MOTORNEG_PIN,LOW);
  digitalWrite(LED_PIN, HIGH);  
}
void motorStartLeft(){
  digitalWrite(MOTORPOS_PIN,LOW);
  digitalWrite(MOTORNEG_PIN,HIGH);
  digitalWrite(LED_PIN, HIGH);  
}
void motorStop(){
  digitalWrite(MOTORPOS_PIN,LOW);
  digitalWrite(MOTORNEG_PIN,LOW);
  digitalWrite(LED_PIN, LOW);  
}

unsigned char validCmd(unsigned long addrAndCmdWord){
  byte cmd    = (addrAndCmdWord >> 16) & 0xFF;
  byte cmdInv = (addrAndCmdWord >> 24) & 0xFF;
  if ((cmd ^ cmdInv) == 0xFF) {return cmd;} else {return 0;}
}

void setup() {
  pinMode(IR_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  pinMode(MOTORPOS_PIN, OUTPUT);
  pinMode(MOTORNEG_PIN, OUTPUT);  
}

void loop() {
  unsigned long addrAndCmdWord = getAddrAndCmdWord();
  unsigned char cmd = validCmd(addrAndCmdWord);
//  blinkLED_bits(cmd);
  if (cmd == VOL_UP) motorStartRight();
  if (cmd == VOL_DOWN) motorStartLeft();
  do {
    if (digitalRead(IR_PIN)==LOW) lastPulseDetected_ms=millis();
  } while ((millis()-lastPulseDetected_ms) < 200);
  motorStop();
}
```
