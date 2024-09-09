---
layout: default
title: "BandSpotsHere - How am I doing relative to other stations in my DXCC?"
permalink: /BandSpotsHere/
---

I’ve been wondering for a while if I struggle to receive FT8 on 2m even whilst I can see my Tx is doing well on Pskreporter.

So I've made a little Python thing to get Pskreporter live data via MQTT & give an overview of who’s active and who’s receiving who on 2m (it can work for any band but 2m is why I made it). 

It works like this: 
- make a list of all callsigns **from the specified DXCC** spotted on the specified band. Call these the Active Calls.
- make a list of all Pskreporter spots where at least one end of the spot is in the specified DXCC and band.
- use these lists to report, for each Active Call:
-   How many DX calls have reported spotting this Active Call (& list them)
-   How many DX calls this Active Call has spotted (& list them)

The screenshot below shows this working on the 2m band
