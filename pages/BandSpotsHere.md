---
layout: default
title: "BandSpotsHere"
subtitle: "Who in my DXCC is transmitting and receiving whom on my favourite bands?"
permalink: /BandSpotsHere/
---
# What is BandSpotsHere?
A [ham radio](https://en.wikipedia.org/wiki/Amateur_radio) related utility that uses the [Pskreporter](https://pskreporter.info/) [MQTT](https://mqtt.org/) feed to display transmit and receive statistics for stations currently active on [FT8](https://www.sigidwiki.com/wiki/FT8) in specified country or group of countries ([DXCC](https://www.electronics-notes.com/articles/ham_radio/awards/dxcc-ham-radio-operating-award.php) codes).

It's useful for guaging the activity levels on specified bands, mix between transmit and receive spots, and who's spotting whom. Spots are monitored globally and presented if either the Tx end or Rx end is in the specified group of DXCC codes.

# Installing the Windows Executable Version
If you just want to install the software, simply download this zip file and extract all files and folders into a convenient folder, and run the batch file by double clicking it.
   - [BandSpotsHereExeV1.1.2.zip]({{ site.baseurl }}/assets/BandSpotsHere/BandSpotsHereExeV1.1.2.zip)

Note that the parameters that specify the bands of interest and the "home" DXCCs are in the bat file 'BandSpotsHere.bat'; you'll need to edit these to suit your area of interest before running.

Once the program is running, the following hotkeys are available:
- b cycles through the bands speccified in the bat file
- d toggles "detail" on and off

Note that the program doesn't know about spots received from PSKR MQTT before the program was launched.

You can stop reading this page here if you don't want to dig deeper.

# Why I made this software
I’ve been wondering for a while if I struggle to receive FT8 on 2m even whilst I can see my Tx is doing well on [Pskreporter](https://pskreporter.info/) If I look at Pskreporter's map of spots of "Country of Callsign G1OJS", I can get some idea. But it's difficult to see if the other spots are from one strong operator with a large beam receiving lots of rx reports from Europe, or if there are quite a few other operators making getting several rx spots each, and how many DX calls this unknown number of active 2m stations in my country are receiving. For example, see the screenshot below:

![PSKR]({{ site.baseurl }}/assets/img/BandSpotsHereV1.1.2%20PSKR.PNG)

BandSpotsHere gets [Pskreporter live data via MQTT](https://groups.io/g/pskr-mqtt) & gives an overview of who’s active and who’s receiving who. This is how it does it: 
- make a list of all callsigns **from the specified DXCCs** spotted or submitting spots on the specified band. Call these the Active Calls.
- categorise these callsigns as Tx only, Tx and Rx, or Rx only
- use these lists to report, for each Active Call:
  - the DX calls (from anywhere) that have reported spotting this Active Call
  - the DX calls (from anywhere) that this Active Call has spotted

The screenshot below shows this working on the 2m band (at the same time as the PSKR screenshot above). It's quite a sparse set of data, but it's meant for relatively empty bands like 2m. It's actually a great way to monitor band activity whilst doing something else, even with the radio off.

![BandSpotsHere]({{ site.baseurl }}/assets/img/BandSpotsHereV1.1.2.PNG)

# Installing the Python Version
If you want to read the Python file & see how it works, and perhaps modify it to suit your own purposes, you'll probably want ti install the Python version.

1. Get Python if you don't already have it. You can download it on the [Python](https://www.python.org/) site.
2. The code refers to several Python libraries that need to be seperately installed. The easiest way to do this is to open a command window and type "pip install" + the name of each of the libraries in turn. The liraries are listed in the file requirements.txt in the zip file.

3. Download this zip file and extract both files into a convenient folder, and run the batch file by double clicking it.
   - [BandSpotsHerePythonV1.1.2.zip]({{ site.baseurl }}/assets/BandSpotsHere/BandSpotsHerePythonV1.1.2.zip)
  













