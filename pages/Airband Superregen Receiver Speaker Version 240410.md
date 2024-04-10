---
layout: default
title: "VHF AM Superregen Receiver with Speaker and Optional Squelch Circuit"
permalink: /VHF-AM-SuperRegen Speaker/
---
# G1OJS VHF Airband Superregen Receiver
Following success with the [Earpiece version Superregen Receiver]({{ site.baseurl }}/VHF-AM-SuperRegen Earpiece) I designed the following circuit with a decent detector and Sallen Key filter.

![Airband Superregen Receiver Schematic]({{ site.baseurl }}/assets/img/G1OJS Airband Superregen Speaker Version BJT SK Filter LM386 Rev 3 240409.png)

The squelch circuit below is optional and works by tighly filtering the strongest audio frequencies produced by the detector and using the level to trigger a monostable to open the squelch. I couldn't get the alternative method - [looking at the noise between the audio and quench frequencies & watching for quieting](https://www.theradioboard.org/forum/solid-state-radios/solid-state-superregenerative-rx-with-squelch) - to work, I think, because I'm using a relatively low quench frequency in this design and it was too hard to separate this out.

The detector is Q3 & based on the configuration recommended in Dr Eddie Insam's paper [Designing Super-Regenerative Receivers](https://www.qsl.net/l/lu7did/docs/QRPp/Receptor%20Regenerativo.pdf). As Dr Insam states, this configuration does seem to improve the sensitivity of the SuperRegen Oscillator (SRO), and the radio can detect signals as low as about -110dBm. After that the buffer Q5 feeds a single stage BJT [Sallen Key](https://en.wikipedia.org/wiki/Sallen%E2%80%93Key_topology) Filter Q4 , and this provides enough signal level to present to the volume control and then on to the LM386 audio amp. The two plots on the schematic show the output audio spectrum at the headphone jack (no load) with no antenna connected (left) and with a signal present (right).

The squelch circuit works by monitoring the audio at around 300 Hz with a Q=1.5 filter (LM358b) fed by a low pass gain stage (LM358a). As the spectrum plots show, the audio in this range is about 10dB higher when a signal is present. When audio levels increase at the output of LM358b, the negative peaks of the audio fall below Vcc/2 and trigger the NE555P monostable. The rest of the circuit shapes the NE555P output to remove sharp edges and controls the audio pass diode D2. Unfortunately setting the gain and reference level is best done with an oscilloscope, but could feasibly be done by trial and error. The trick is to set RV4 as high gain as possible without clipping in LM358a on either signal or noise, then adjust the level pot RV6 so that the squelch *just* stays closed on a no-signal condition.

Once set however, the squelch works well enough that I didn't feel the need to add a front panel squelch level control or switch, and is insensitive to variations in the SRO output that occur as the tuning control is swept across the band (which is a problem with the other methods of squelch I think). 

![Airband Superregen Receiver Squelch Circuit Schematic]({{ site.baseurl }}/assets/img/G1OJS Airband Superregen Speaker Version BJT SK Filter LM386 Squelch Rev 1 240409.png)
