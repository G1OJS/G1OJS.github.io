---
layout: default
title: "Minimal TV IR Decoder and Motor Driver using ATTiny mpc without library"
permalink: /TV_IR_Motor_tiny/
---

```
// TV Remote Vol up / Vol down decoder and motor driver
// for motorised volume control using ATTiny88
// and LG Magic Remote
//
// (C) 2025 Alan Robinson G1OJS 

// Code readability constants
#define LEFT 2
#define RIGHT 1
#define OFF 0
#define IR_PIN 24  // A5 on my board with DrAzzy core
#define LED_PIN 0  // Built in LED
#define MOTORPOS_PIN 10
#define MOTORNEG_PIN 11
// Magic Remote Vol+ / Vol -
#define MRtx_VOL_UP 0xFA    
#define MRtx_VOL_DOWN 0xF8
// 'Device Connector' codes (LG Sound Sync off)
#define TVtx_VOL_UP 0xE8     
#define TVtx_VOL_DOWN 0xE9
#define TVtx_MUTE 0xE0

unsigned long lastPulseDetected_ms=0;  // to decide if button is held down

void motorDrive(unsigned char state){
  digitalWrite(MOTORPOS_PIN,(state==RIGHT));
  digitalWrite(MOTORNEG_PIN,(state==LEFT));
  digitalWrite(LED_PIN, (state!=OFF));
  // if motor drive is on, pause here until most recent IR activity is > ~ 0.2 seconds
  // (i.e. wait for button release)
  if (state!=OFF) {
    do {
      if (digitalRead(IR_PIN)==LOW) lastPulseDetected_ms=millis();
      bool inactive = (millis()-lastPulseDetected_ms) > 200; 
      if (inactive) break;
    }   while (1);
  }  
}

// This is for debugging and working out codes only.
// Blinks out 8 bits MSB to LSB, long flash = 1, short flash = 0.
void blinkLED_bits(unsigned long bits) {
  for (int i = 0; i < 8; i++) {
    digitalWrite(LED_PIN, HIGH);
    delay((bits & 128)? 400:100);
    digitalWrite(LED_PIN, LOW);
    delay((bits & 128)? 100:400);
    bits *=2; // used * rather than bit shift to be absolutely sure I'm shifting the right way!
  }
  digitalWrite(LED_PIN, LOW);
  delay(200);
}

// This is the core of the code, waiting for IR activity and then timing pulses to decide
// whether a 0 or 1 was transmitted and packing these bits into the 32 bit control word 
// It uses the NEC Protocol. Note that IR module ouitput is HIGH when IR remote is OFF, 
// and LOW when IR remote is transmitting IR. Code could be made more readable by adding 
// something to make this explicit.
// https://wiki.keyestudio.com/052035_Basic_Starter_V2.0_Kit_for_Arduino#Project_14:_IR_Remote_Control
unsigned long getAddrAndCmdWord(){
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

// helper function to check that the received word is valid
// by checking that the inverted repeat of the command matches the first transmitted command
unsigned char validCmd(unsigned long addrAndCmdWord){
  byte cmd    = (addrAndCmdWord >> 16) & 0xFF;
  byte cmdInv = (addrAndCmdWord >> 24) & 0xFF;
  if ((cmd ^ cmdInv) == 0xFF) {return cmd;} else {return 0;}
}

// the usual stuff to set up pins ...
void setup() {
  pinMode(IR_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
  pinMode(MOTORPOS_PIN, OUTPUT);
  pinMode(MOTORNEG_PIN, OUTPUT);  
}

// get the command word, pull out commands if valid, drive the motor.
// Readability again - need to make the "wait until IR is quiet again"
// more explicit here (it's hidden above in motorDrive())
void loop() {
  unsigned long addrAndCmdWord = getAddrAndCmdWord();
  unsigned char cmd = validCmd(addrAndCmdWord);
  if ((cmd == MRtx_VOL_UP) || (cmd == TVtx_VOL_UP) )  { motorDrive(RIGHT); }
  else if ((cmd == MRtx_VOL_DOWN) || (cmd == TVtx_VOL_DOWN) ) { motorDrive(LEFT); }
  else {blinkLED_bits(cmd);}
  motorDrive(OFF);
}



```
