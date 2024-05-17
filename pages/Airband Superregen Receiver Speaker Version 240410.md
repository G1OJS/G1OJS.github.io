---
layout: default
title: "VHF AM Superregen Receiver with Speaker and Optional Squelch Circuit"
permalink: /VHF-AM-SuperRegen Speaker/
---
# G1OJS VHF Airband Superregen Receiver with Squelch
This page describes my Superregen VHF AM receiver with Squelch. It has several advantages over a superhet design:
- Fewer components
- No alignment required
- Easy tuning
- AGC action inherent in the superregen circuit, so no AGC circuit needed
- Superregen "capture effect"

## Circuit description
![Airband Superregen Receiver Schematic]({{ site.baseurl }}/assets/img/G1OJS Airband Superregen With Squelch 17-05-24.png)

### Superregen Receiver Section
The Superregen circuit based around Q2 is nothhing new, and follows several designs available on the web. As with all superregenerative oscillators (SROs), it is necessary to precede the circuit by an amplifier stage to avoid radiation of the oscillations produced by the SRO. Q1 performs this function and provides sufficient gain to allow the SRO to detect signals as low as -110 dBm.

The detector is Q3 & based on the configuration recommended in Dr Eddie Insam's paper [Designing Super-Regenerative Receivers]
(https://www.qsl.net/l/lu7did/docs/QRPp/Receptor%20Regenerativo.pdf). As Dr Insam states, this configuration does seem to improve the sensitivity of the SuperRegen Oscillator (SRO). After that the buffer Q5 feeds a single stage BJT [Sallen Key](https://en.wikipedia.org/wiki/Sallen%E2%80%93Key_topology) Filter Q4 , and this provides enough signal level to present to the volume control and then on to the LM386 audio amp. 

### Squelch Circuit Background
<details markdown=1><summary markdown="span">Click to expand</summary>
Squelch circuits can be quite tricky to implement in SRO receivers because the background noise under "no signal" conditions can be almost as loud as wanted signals when a carrier is present. There are several ways around this problem:

1) Monitor the "no signal" noise above the highest modulation frequency and watch for the amplitude of this to fall when a carrier is present.
2) Tightly fitler the audio and use a traditional audio squelch, hoping to exclude as much "no signal" noise as possible via the filtering (i.e. the opposite approach to 1).
3) My own invention as far as I know: monitor the audio spectrum (again tightly filtered as in 2) but instead of triggering the squelch based on the *level* of the audio, watch for *changes* in the audio level. This way, the squelch responds to the transition between "no signal" hiss and the quieted audio on reception of an unmodulated carrier, and also responds to the cadence of voice signals (the increase and decrease in volume across speech sounds is itself a signal that can be monitored).

Examples of all three circuits are shown below.




</details>

### Squelch Circuit
The squelch circuit is based around a fairly traditional diode pump (Greinacher circuit). It monitors the "no signal" noise above the highest modulation frequency and watches for the amplitude of this to fall when a carrier is present. When the audi level falls below a threshold, the squelch opens (this is option 1 in the "Squelch Circuit Background" section above).

Rather than use a narrow bandpass filter to monitor the hiss above the max audio frequency, this circuit takes advantage of the (uncommon) 2nd order low pass filtering provided by the Sallen-Key filter around Q5, and uses a fairly basic high pass filter (C101 working against the input impedance of Q101) to work with this and create a bandpass filter in aggregate. Even so, some audio does make it through especially on loud signals, which is problematic as this is hard for a simple level detector to distinguish from the level of "no signal" hiss; remember we are looking for "quiet" audio to open the squelch.

A diode pump circuit feeds a JFET (Q102) in a way that provides a fast rise time & fall time binary response at the drain of the JFET when audio levels drop below a threshold set by RV101. With very quiet audio (dead carrier or carrier with low level audio modulation) the diode pump produces an output close to zero volts; this leaves the JFET conducting and Q103 turned off, allowing audio to pass unhindered from the volume control to the LM386 amplifier. In the "no signal" condition, the background noise levels increase, and the diode pump produdes larger negative voltages which cause the JFET to turn off, biasing Q103 into conduction and shorting out the audio at the input to the LM386 amplifier.

Unfortunately, this latter state would also arise when strongly modulated carriers are received, resulting in the squelch *closing* on strong audio (not good!), although (due to the fast time constants in the diode pump) this is confined to voice peaks only. To create a useable squelch circuit, all that is needed is a way to keep the squelch open across strong voice peaks. A simple capacitor across the base-emitter junction of Q103 is sufficient to do this, by providing a "pulse stretching" or monostable function which maintains the "squelch open" condition across voice peaks, and also provides a short (but not too long) "hang time" for the overall squelch action.

 

