---
layout: default
title: "BandSpotsHere"
subtitle: "Who in my DXCC is transmitting and receiving whom on my favourite bands?"
permalink: /BandSpotsHere/
---

# What is BandSpotsHere?
BandSpotsHere is a piece of MS-Windows software that gets data from  [Pskreporter](https://pskreporter.info/) & gives an overview of who’s active and who’s receiving who. 

![BandSpotsHere]({{ site.baseurl }}/assets/img/BandSpotsHereV1.1.2.PNG){: .image-right }
The information is presented in a way that has several advantages over looking at the map views directly on Pskreporter:
 - **See activity for a group of DXCCs rather than a single "country of callsign ..."** On Pskreporter you have to choose between a single callsign, callsign's country, or everyone. When your local area has several DXCCs in it, it's useful to be able to combine them into one view (e.g. the UK is what I want to monitor, not England).
 - **See which active stations are transmitting or just receiving.** In other words, are there stations actively working the bands, or have they just left their equipment running & gone to work - or are they even a WEBSDR station?
 - **Get a view of whether the active stations are getting spotted by more DX calls than they are spotting themselves, or vice versa.** In other words, how is receive performance stacking up against transmit performance for the active stations? 
 - **Easily compare this with your own transmit and receive spots.** How does this compare to your own station's performance? If you aren't receiving or tranmitting as well as you'd like, is this a problem with your setup or is it just how the band is currently?
 - **See which DX callsigns are spotting, and being spotted by, the active callsigns in your specified DXCCs.** i.e. where is the band open to *from your specified 'home region' (DXCC group)*
 - **Simultaneously, monitor spot numbers across several other bands to watch for band openings.** Watch the volume of spots rise and fall on all your specified bands at the same time as looking at the detail above for one of these bands. This is a good way to see if activity is starting on another band, and you can then cycle through the bands to see all of the detail above.

# Installation
Download this zip file and extract all files and folders into a convenient folder. To run the program, simply double click the file 'BandSpotsHere.bat'.
   - [BandSpotsHereExeV1.1.2.zip]({{ site.baseurl }}/assets/BandSpotsHere/BandSpotsHereExeV1.1.2.zip)

# Usage
To change the pre-loaded bands and DXCC codes, edit the file 'BandSpotsHere.bat' before running.

Once the program is running, you can cycle through the bands by pressing  the 'b' key.

On busy bands, you will probably not want to see all indidvidual spot details (mainly because this will produce more than one page of output and require you to manually scroll through it), so you can toggle this detail on and off by pressing the 'd' key.

Note that the program doesn't know about spots received from PSKR MQTT before the program was launched.

The screen will update every 15 seconds. Spot information is kept for 15 minutes (by default - you can change this in the 'BandSpotsHere.bat' file) after which they are deleted from memory, so the screen information reflects the last 15 (or what you specify) minutes of band activity.

If you want, you can make several copies of 'BandSpotsHere.bat' with different settings (different bands and/or DXCCs to watch) and run them simultaneously. So you can have one instance watching VHF bands including what's happening in nearby countries, and another watching HF bands just for your own country's band activity.















