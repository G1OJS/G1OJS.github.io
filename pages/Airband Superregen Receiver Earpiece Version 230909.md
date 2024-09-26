---
layout: default
title: "VHF AM Superregen Receiver"
permalink: /VHF-AM-SuperRegen Earpiece/
---
Last summer (2023) I got the construction bug and wanted to build an airband receiver free from microprocessors. Something with an "analogue feel". 
So I set about Googling and found quite a few designs for superregen receivers and a particular superhet kit that comes up very often based around
the NE602 oscillator/mixer and several op-amps, plus an "IF can" transformer. I wanted to make something that was as close to an all-transistor all-solid-state design as I could (in other words, things I had to hand!). 

![Airband Superregen Receiver Build 230909]({{ site.baseurl }}/assets/img/Airband Superregen Receiver Build Photo 230909.jpg)

At the time (despite being a Ham since 1984 and an electronics engineering graduate) I hadn't realised that a SuperRegenerative receiver is very different from a Regenerative Receiver. Key things I leaned straightaway - a superregen receiver:

- doesn't have a "regen" control that allows the circuit to behave as a high Q AM receiver which can tip into self oscillation and become a DSB receiver. A superregen is an AM receiver (which can also be used on FM via slope detection), and its operating point is set internally.
- has a kind of "capture effect" which causes the receiver to focus on the strongest signal in the passband
- can be almost as sensitive as any other receiver
- has a log law response to RF signal level, meaning good dynamic range without need of an AGC

One of the best explanations of how these receivers actually *work* is a paper called "Designing Super-Regenerative Receivers" by Dr Eddie Insam. There is a copy [here](https://www.qsl.net/l/lu7did/docs/QRPp/Receptor%20Regenerativo.pdf). Don't be put off by the maths because the text explains things well.

The circuit used above started off as my build of a circuit found at lots of places online, all variants of this one described in [Radio Builder](https://radiobuilder.blogspot.com/2012/10/airbandregen1t.html). Some of the variants have quite strange and unnecessary variations! There is nothing critical - nor magical - about the twisted and folded antenna found in some versions that don't have the RF isolator/amplifier. 

I added an RF gain stage and two-transistor audio amplifier, and spent *a lot* of time investigating the effect of changing the component values in the quench frequency components and audio tap. The circuit I ended up with is below, and it works really well:

![Airband Superregen Receiver 230909]({{ site.baseurl }}/assets/img/Airband Superregen Receiver 230909.png)

Construction note: keep leads short as possible in the RF parts (first two transistors). If you find the 10pF capacitor connected to the varicap diode in the photo above, you'll see that the path to ground via that capacitor and the varicap diode is a lot shorter than it appears from the circuit diagram. 

This little receiver has quite a few advantages:
- Current draw only about 9 mA
- Capture effect combined with wide passband makes for easy yet selective tuning
- Fun to build with only 4 transistors & a handful of R, L, C.
- Almost as sensitive as any other receiver
- No IF frequency therefore no image filtering required & no problems with pager system images etc

It does of course have disadvantages. One is that it can be overwhelmed by strong signals if connected to a large antenna. Another is that stray capacitance and lead inductance play affect the performance such that different layouts will behave slightly differently. But for a hand portable with a quarter wave whip, it's a lot of fun. It's even possible to add a squelch circuit, but this requires a whole IC and Rs and Cs & is a bit fiddly to operate, though it does work (page coming on this soon, maybe).

Note: as with all superregen receivers, the superregen stage oscillates with a lot of amplitude at the receive frequency and across a lot of adjacent spectrum. If used close to airports, it must be in a screened box and any antenna must be isolated by using an input amplifier/isolator as shown.


