---
layout: default
title: "Minimal TV IR Decoder and Motor Driver using ATTiny mpc without library"
permalink: /TV_IR_Motor_tiny/
---

```
// TV Remote Vol up / Vol down decoder and motor driver
// for motorised volume control using ATTiny88
// and LG Magic Remote (note that the LG remote may refuse to send
// codes when external speakers are used, so it may be necessary to program
// an alternative remote to send the usual codes)
//
// (C) 2025 Alan Robinson G1OJS 

#define IR_PIN 24  // A5 on my board with DrAzzy core
#define LED_PIN 0  // Built in LED
#define MOTORPOS_PIN 10
#define MOTORNEG_PIN 11
#define VOL_UP 0xFA
#define VOL_DOWN 0xF8
#define LEFT 2
#define RIGHT 1
#define OFF 0
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
    }   while ((millis()-lastPulseDetected_ms) < 200);
  }  
}

// This is for debugging and working out codes only.
// Blinks on a regular 'beat' (400ms) with 300ms flash = 1, 100ms flash = 0
// First delay() sets the duration, second delay pads to 400ms
void blinkLED_bits(unsigned long bits) {
  for (int i = 0; i < 8; i++) {
    digitalWrite(LED_PIN, HIGH);
    delay((bits & 255)? 300:100);
    digitalWrite(LED_PIN, LOW);
    delay((bits & 255)? 100:300);
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
//  blinkLED_bits(cmd);
  if (cmd == VOL_UP)   motorDrive(RIGHT);
  if (cmd == VOL_DOWN) motorDrive(LEFT);
  motorDrive(OFF);
}

```
