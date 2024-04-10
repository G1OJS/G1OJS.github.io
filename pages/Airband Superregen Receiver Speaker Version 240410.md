---
layout: default
title: "VHF AM Superregen Receiver with Speaker and Optional Squelch Circuit"
permalink: /VHF-AM-SuperRegen Speaker/
---
# G1OJS VHF Airband Superregen Receiver
Following success with the [Earpiece version Superregen Receiver]({{ site.baseurl }}/VHF-AM-SuperRegen Earpiece) I designed the following circuit with a decent detector and Sallen Key filter.

![Airband Superregen Receiver Schematic]({{ site.baseurl }}/assets/img/G1OJS Airband Superregen Speaker Version BJT SK Filter LM386 Rev 3 240409.png)

The squelch circuit below is optional and works by tighly filtering the strongest audio frequencies produced by the detector and using the level to trigger a monostable to open the squelch. I couldn't get the alternative method - looking at the noise between the audio and quench frequencies & watching for quieting - to work because I'm using a relatively low quench frequency in this design and it was too hard to separate this out.

![Airband Superregen Receiver Squelch Circuit Schematic]({{ site.baseurl }}/assets/img/G1OJS Airband Superregen Speaker Version BJT SK Filter LM386 Squelch Rev 1 240409.png)
