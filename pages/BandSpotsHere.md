---
layout: default
title: "BandSpotsHere - How am I doing relative to other stations in my DXCC?"
permalink: /BandSpotsHere/
---
# BandSpotsHere - How am I doing relative to other stations in my DXCC?

## TL;DR
A [ham radio](https://en.wikipedia.org/wiki/Amateur_radio) related utility that uses the [Pskreporter](https://pskreporter.info/) [MQTT](https://mqtt.org/) feed to display transmit and receive statistics for stations currently active on [FT8](https://www.sigidwiki.com/wiki/FT8) in specified country ([DXCC](https://www.electronics-notes.com/articles/ham_radio/awards/dxcc-ham-radio-operating-award.php) codes).

## Notes
At the time of writing (Sep 2024), I've been working on this utility for about a week; hence, this page is really to publish the idea and allow people who know a bit about coding to try it out.

Also, this whole page assumes a lot of knowledge about ham radio, the FT8 mode and [Pskreporter.info](https://pskreporter.info/)

## Introduction 
I’ve been wondering for a while if I struggle to receive FT8 on 2m even whilst I can see my Tx is doing well on [Pskreporter](https://pskreporter.info/) If I look at Pskreporter's map of spots of "Country of Callsign G1OJS", I can get some idea. But it's difficult to see if the other spots are from one strong operator with a large beam receiving lots of rx reports from Europe, or if there are quite a few other operators making getting several rx spots each, and how many DX calls this unknown number of active 2m stations in my country are receiving. For example, see the screenshot below:

![PSKRExample]({{ site.baseurl }}/assets/img/PSKR for BandSpotsHereV1.1.1.JPG)

So I've made a little Python thing to get [Pskreporter live data via MQTT](https://groups.io/g/pskr-mqtt) & give an overview of who’s active and who’s receiving who on 2m (it can work for any band but 2m is why I made it). 

It works like this: 
- make a list of all callsigns **from the specified DXCC** spotted on the specified band. Call these the Active Calls.
- make a list of all Pskreporter spots where at least one end of the spot is in the specified DXCC and band.
- use these lists to report, for each Active Call:
  - how many DX calls have reported spotting this Active Call (& list them)
  - how many DX calls this Active Call has spotted (& list them)

The screenshot below shows this working on the 2m band (at the same time as the PSKR screenshot above). It's quite a sparse set of data, but it's meant for relatively empty bands like 2m. It's actually a great way to monitor band activity whilst doing something else, even with the radio off.

![BandSpotsHere]({{ site.baseurl }}/assets/img/BandSpotsHereV1.1.1.JPG)

## Installing it
1. Get Python.These scripts are written in Python and you'll need to install that if you haven't got it yet. You can download it on the [Python](https://www.python.org/) site.
2. The code refers to several Python libraries that need to be seperately installed. The easiest way to do this is to open a command window and type "pip install" + the name of each of the libraries in turn. The liraries are:
   - paho.mqtt.client
   - os
   - datetime
   - pynput
   - pygetwindow
   - time
   - colorama
   - sys

3. Download this zip file and extract both files into a convenient folder, and run the batch file by double clicking it.
   - [Python V1.zip]({{ site.baseurl }}/assets/BandSpotsHere/Python V1.1.1.zip)

The parameters that specify the bands of interest and the "home" DXCCs are in the bat file ('BandSpotsHere.bat'); you'll need to edit these to suit your area of interest before running.











