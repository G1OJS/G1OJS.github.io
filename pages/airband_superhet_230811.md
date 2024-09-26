---
layout: default
title: "G1OJS VHF Airband Superhet Receiver"
permalink: /VHF-AM-Superhet/
---
Last summer (2023) I got the construction bug and wanted to build an airband receiver free from microprocessors. Something with an "analogue feel". 
So I set about Googling and found quite a few designs for superregen receivers and a particular superhet kit that comes up very often based around
the NE602 oscillator/mixer and several op-amps, plus an "IF can" transformer. I wanted to make something that was as close to an all-transistor all-solid-state
design as I could (in other words, things I had to hand!). I ended up [investigating superregen ideas too]({{ site.baseurl }}/VHF-AM-SuperRegen). This page is about the superhet version.

![Airband Superhet 230811 Modular Build]({{ site.baseurl }}/assets/img/2023-08-11 Build VHF AM.jpg)

Apologies for the first version of this page having very little explanation - I just wanted to get the circuit onto the website.

Also note that the circuit was designed mainly by trial and error, borrowing a few ideas (e.g. the input filter) from other designs
and arriving at component values experimentally in the main, so although I believe the component values are *good*, they may not be optimum.

# The circuit
The circuit diagram is shown below. The only "special" components needed are:
- NE602 local oscillator / mixer IC
- Two ceramic resonator type filters 10.7MHz +/- 10 kHz e.g. TOKEN LT10.7MFP
- Varicap diode BB910 or similar

Obviously, performance isn't going to rival commercial receivers (even cheap scanner radios) but it is a fun build and sensitivity is quite reasonable
(somewhere around -110 dBm MDS from memory). It could still do with a bit more end-to-end gain, but as it is it doesn't really need a squelch circuit
as it's very quiet on background noise only.

![Airband Superhet 230801 Schematic]({{ site.baseurl }}/assets/img/Airband Superhet Max Transistors No IF Can Narrow Filters 230811.png)

This circuit is presented as a starting point for your own experimentation - but in my opinion it's a better starting point than some of the other circuits on the web! The development story with build pictures is on my G1OJS Instagram starting around [here](https://www.instagram.com/p/CvAnG36NHw5/) and ending about [here](https://www.instagram.com/p/Cvy-pRIoMbK/). I started off with a circuit using an IF Can - which I wound myself - and eliminating that from the design was a good move, I think. If I were rebuilding it, I would put a ceramic resonator in every IF stage not just before the first and last.

There are two ways to handle fine tuning - one is to use a reasonably large knob on the tuning pot (~50mm diameter) and the other is to use the fine tuning circuit shown in the schematic above.
