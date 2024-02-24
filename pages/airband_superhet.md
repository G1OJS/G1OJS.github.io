---
layout: default
title: "VHF AM Superhet"
permalink: /VHF-AM-Superhet/
---
# G1OJS One-IC VHF Airband Superhet Receiver
Last summer I got the construction bug and wanted to build an airband receiver free from microprocessors. Something with an "analogue feel". 
So I set about Googling and found quite a few designs for superregen receivers and a particular kit that comes up very often based around
the NE602 oscillator/mixer and several op-amps, plus an "IF can" transformer. I wanted to make something that was as close to an all-transistor all-solid-state
design as I could (in other words, things I had to hand!). I ended up investigating superregen ideas too. This page is about the superhet version.

## The circuit
The circuit diagram is shown below. The only "special" components needed are:
- NE602 local oscillator / mixer IC
- Two ceramic resonator type filters 10.7MHz +/- 10 kHz e.g. TOKEN LT10.7MFP
- Varicap diode BB910 or similar
Obviously, performance isn't going to rival commercial receivers (even cheap scanner radios) but it is a fun build and sensitivity is quite reasonable
(somewhere around -110 dBm from memory). It could still do with a bit more end-to-end gain, but as it is it doesn't really need a squelch circuit
as it's very quiet on background noise only.

![Airband Superhet V1,0]({{ site.baseurl }}/assets/img/Airband Superhet Max Transistors No IF Can Narrow Filters V1.0.png)
