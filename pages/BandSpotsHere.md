---
layout: default
title: "BandSpotsHere - How am I doing relative to other stations in my DXCC?"
permalink: /BandSpotsHere/
---
# BandSpotsHere - How am I doing relative to other stations in my DXCC?

## TL;DR
A [ham radio](https://en.wikipedia.org/wiki/Amateur_radio) related utility that uses the [Pskreporter](https://pskreporter.info/) [MQTT](https://mqtt.org/) feed to display transmit and receive statistics for stations currently active on [FT8](https://www.sigidwiki.com/wiki/FT8) in a specified country ([DXCC](https://www.electronics-notes.com/articles/ham_radio/awards/dxcc-ham-radio-operating-award.php) code).

## Notes
At the time of writing (Sep 2024), I've been working on this utility for about a week; hence, this page is really to publish the idea and allow people who know a bit about coding to try it out.

Also, this whole page assumes a lot of knowledge about ham radio, the FT8 mode and [Pskreporter.info](https://pskreporter.info/)

## Introduction 
I’ve been wondering for a while if I struggle to receive FT8 on 2m even whilst I can see my Tx is doing well on [Pskreporter](https://pskreporter.info/) If I look at Pskreporter's map of spots of "Country of Callsign G1OJS", I can get some idea. But it's difficult to see if the other spots are from one strong operator with a large beam receiving lots of rx reports from Europe, or if there are quite a few other operators making getting several rx spots each, and how many DX calls this unknown number of active 2m stations in my country are receiving. For example, see the screenshot below:

![PSKRExample]({{ site.baseurl }}/assets/img/PSKReporter.JPG)

So I've made a little Python thing to get [Pskreporter live data via MQTT](https://groups.io/g/pskr-mqtt) & give an overview of who’s active and who’s receiving who on 2m (it can work for any band but 2m is why I made it). 

It works like this: 
- make a list of all callsigns **from the specified DXCC** spotted on the specified band. Call these the Active Calls.
- make a list of all Pskreporter spots where at least one end of the spot is in the specified DXCC and band.
- use these lists to report, for each Active Call:
  - how many DX calls have reported spotting this Active Call (& list them)
  - how many DX calls this Active Call has spotted (& list them)

The screenshot below shows this working on the 2m band (at the same time as the PSKR screenshot above). It's quite a sparse set of data, but it's meant for relatively empty bands like 2m. It's actually a great way to monitor band activity whilst doing something else, even with the radio off.

![BandSpotsHere]({{ site.baseurl }}/assets/img/BandSpotsHere.JPG)

## Installing it
1. Get Python.These scripts are written in Python and you'll need to install that if you haven't got it yet. You can download it on the [Python](https://www.python.org/) site.
2. The code refers to several Python libraries that need to be seperately installed. The easiest way to do this is to open a command window and type "pip install" + the name of each of the libraries in turn. The liraries are:
   - pickle
   - os
   - datetime
   - time
   - colorama
   - paho.mqtt.client
   - math
   - maidenhead (this isn't actually used in the display yet, but is in the spot gathering code)
   - sys

3. Download all 4 files from [here]({{ site.baseurl }}/assets/BandSpotsHere/Python V1). Put all 4 files in a convenient folder, and run both batch files by double clicking them.
  
You need to run both batch files at the same time (start either first) because one gathers spots via MQTT and the other displays the analysis of them. There's probably a much better way to do this using threading within one Python module but this was the easiest and most convenient for me. 

The parameters that specify the band of interest and the "home" DXCC are in the first bat file ('BandSpotsHere.bat'); you'll need to edit these to suit your area of interest before running.

The spot-gathering code saves two 'Pickle' files in the same directory as the code for the display code to use. If you stop the code and change the band or home DXCC, please delete these files or you'll have a mix of spots from the previous and new places and won't be able to tell them apart until they have 'expired' (see 'stale_mins'). Actually you can delete these files at any time should you want to manually reset the spots or active list to empty. **Known issue:** the code that calls the 'clear out old spots & calls' part currently lives in the loop that activates if a spot is received, which means that if no spots are received, spots older than the 'stale_mins' specification will still display.

Development ideas for the future include a GUI of some kind (or at least hotkeys) and using Maidenhead square(s) as an alternative to DXCC to specify the "neighbours" you want to watch.










