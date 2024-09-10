---
layout: default
title: "BandSpotsHere - How am I doing relative to other stations in my DXCC?"
permalink: /BandSpotsHere/
---
# BandSpotsHere - How am I doing relative to other stations in my DXCC?

## TL;DR
A [ham radio](https://en.wikipedia.org/wiki/Amateur_radio) related utility that uses the [Pskreporter](https://pskreporter.info/) [MQTT](https://mqtt.org/) feed to display transmit and receive statistics for stations currently active on [FT8](https://www.sigidwiki.com/wiki/FT8) in a specified country ([DXCC](https://www.electronics-notes.com/articles/ham_radio/awards/dxcc-ham-radio-operating-award.php) code).

## Notes
At the time of writing (Sep 2024), I've been working on this utility for about a week; hence, this page is really to publish the idea and allow people who know a bit about coding to try it out. As I develop it further, I'll add some install instructions and see what I can do to make that as simple as possible. In the meantime: download & install [Python](https://www.python.org/), open a command window and type "pip install " + each of the libraries mentioned below, download the two bits of Python code from this page, and the two Windows batch files (bottom of this page) to run them, and run both batch files.

Also, this whole page assumes a lot of knowledge about ham radio, the FT8 mode and [Pskreporter.info](https://pskreporter.info/)

## Introduction 
I’ve been wondering for a while if I struggle to receive FT8 on 2m even whilst I can see my Tx is doing well on [Pskreporter](https://pskreporter.info/) If I look at Pskreporter's map of spots of "Country of Callsign G1OJS", I can get some idea. But it's difficult to see if the other spots are from one strong operator with a large beam receiving lots of rx reports from Europe, or if there are quite a few other operators making getting several rx spots each, and how many DX calls this unknown number of active 2m stations in my country are receiving. For example, see the screenshot below:

![PSKRExample]({{ site.baseurl }}/assets/img/PSKRExample.JPG)

So I've made a little Python thing to get [Pskreporter live data via MQTT](https://groups.io/g/pskr-mqtt) & give an overview of who’s active and who’s receiving who on 2m (it can work for any band but 2m is why I made it). 

It works like this: 
- make a list of all callsigns **from the specified DXCC** spotted on the specified band. Call these the Active Calls.
- make a list of all Pskreporter spots where at least one end of the spot is in the specified DXCC and band.
- use these lists to report, for each Active Call:
  - how many DX calls have reported spotting this Active Call (& list them)
  - how many DX calls this Active Call has spotted (& list them)

The screenshot below shows this working on the 2m band (at the same time as the PSKR screenshot above). It's quite a sparse set of data, but it's meant for relatively empty bands like 2m. It's actually a great way to monitor band activity whilst doing something else, even with the radio off.

![LiveSpotsExample]({{ site.baseurl }}/assets/img/BandSpotsHereExample.jfif)

I've listed the Python code below. It's not a polished installable product yet, just Python code to play with. You need to run both bits of Python at the same time (one gathers spots via MQTT and the other displays the analysis of them). There's probably a much better way to do this using threading within one Python module but this was the easiest and most convenient for me. I run the Python scripts from two .bat files with the same names as the scripts. You'll need a fair few Python libraries that you can easily install using Pip Install:
- pickle
- os
- datetime
- time
- colorama
- paho.mqtt.client
- math
- maidenhead (this isn't actually used in the display yet, but is in the spot gathering code)

The parameters that specify the band of interest and the "home" DXCC are at the top of the "main" block around line 105 in the spot-gathering code.

Development ideas for the future include a GUI of some kind (or at least hotkeys) and using Maidenhead square(s) as an alternative to DXCC to specify the "neighbours" you want to watch.

## [The spot-gathering code]({{ site.baseurl }}/assets/BandSpotsHere/BandSpotsHere.py)
Click the title above to download the code.
```Python
import paho.mqtt.client as mqtt
import pickle
import math
import datetime
import time
import maidenhead as mh

def MHtoDB(Square1, Square2):
  d2r=3.1415926/180.0
# Get lat/long from squares
  ll=mh.to_location(Square1[0:6], center=True)
  lat1=ll[0]
  lon1=ll[1]
  ll=mh.to_location(Square2[0:6], center=True)
  lat2=ll[0]
  lon2=ll[1]
# Distance and bearing
  km=6371*math.acos(math.sin(d2r*lat2)*math.sin(d2r*lat1)+math.cos(d2r*lat1)*math.cos(d2r*lat2)*math.cos(d2r*(lon2-lon1)))
  deg=math.atan2(math.sin(d2r*(lon2-lon1))*math.cos(d2r*lat2),math.cos(d2r*lat1)*math.sin(d2r*lat2)-math.sin(d2r*lat1)*math.cos(d2r*lat2)*math.cos(d2r*(lon2-lon1)))/d2r
  return round(km),round((deg+360) % 360)

def msg_to_spot_dict(msg):
  # convert the msg into a dict with entries as follows:
  # "t":  secs since 1970-01-01,  "sq": sequence number
  # "f":  frequency (Hz), "b":band, "md":mode, 
  # "sc": sender call,    "sl":sender loc sq,     "sa": sender dxcc
  # "rc": receiver call,  "rl": receiver loc sq,  "ra": receiver dxcc
  # "rp": report(snr) 

  res=str(msg.payload)[3:-2]
  sp={}
  for s in str(res).split(","):
    it=s.split(":")
    sp[it[0][1:-1]]=it[1].strip('\"')

  return sp


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

    # Example: client.subscribe("pskr/filter/v2/2m/FT8/+/+/+/+/223/#") gets spots of England 2m
    # This pair of subscribes gets all reports where at least one end is in the home_dxcc:
    client.subscribe("pskr/filter/v2/"+band+"/FT8/+/+/+/+/"+home_dxcc+"/#")
    client.subscribe("pskr/filter/v2/"+band+"/FT8/+/+/+/+/+/"+home_dxcc)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
  global spot_pairs, active_tx,lastsave
  sp=msg_to_spot_dict(msg)

  # time the spot was made
  tspot=datetime.datetime.fromtimestamp(int(sp["t"]))

  # if the *transmitter* is in the home_dxcc (i.e. counts as "active"), make sure its in the active tx list
  if (sp["sa"]==home_dxcc) and (sp["sc"] not in active_tx):
    active_tx[sp["sc"]]=tspot

  # flush out active_tx calls not seen for a while
  for txc in active_tx:
    tnow=datetime.datetime.now()
    ts=active_tx[txc]
    td=int((tnow-ts).total_seconds()/60)
    if(td>stale_mins):
      active_tx.pop(txc)
  
  # if either station in the spot is in the active list (home_dxcc and recent), record the spot pair with details
  if (sp["sc"] in active_tx) or (sp["rc"] in active_tx):
    kmDeg=MHtoDB(sp["sl"],sp["rl"])
    pair_key=sp["sc"]+"->"+sp["rc"]
    spot_pairs[pair_key]={"ts":tspot, "sc":sp["sc"], "rc":sp["rc"], "km":kmDeg[0], "deg":kmDeg[1], "rp":sp["rp"]}

  # if it's been a while, clean and save the dictionaries
  tnow=datetime.datetime.now()
  td=(tnow-lastsave).total_seconds()
  if(td>15): 
    savedicts()

def savedicts():
  global lastsave
  # save the dictionaries
  tnow=datetime.datetime.now()
 
  # flush out active_tx calls not seen for a while
  delete= [active_call for active_call in active_tx if (tnow-active_tx[active_call]).total_seconds()/60 > stale_mins]
  for active_call in delete:
    del active_tx[active_call]
  # flush out old spot pairs
  delete= [pair for pair in spot_pairs if (tnow-spot_pairs[pair]["ts"]).total_seconds()/60 > stale_mins]
  for pair in delete:
    del spot_pairs[pair]
  # save the cleaned dictionaries
  lastsave=tnow
  print("Saving "+str(len(spot_pairs))+ " spot pairs for "+str(len(active_tx))+ " active calls on "+band+" in dxcc "  + home_dxcc)
  with open('spots.pkl', 'wb') as f:
    pickle.dump(spot_pairs, f)
    f.close()
  with open('active.pkl', 'wb') as f:
    pickle.dump(active_tx, f)
    f.close()

# Main ########

####### Edit this part for your requirements: #####
band="2m"
home_dxcc="223"
stale_mins=15
###################################################

lastsave=datetime.datetime.now()

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect("mqtt.pskreporter.info", 1883, 60)

spot_pairs={}
active_tx={}

try:
  with open('spots.pkl', 'rb') as f:
    spot_pairs = pickle.load(f)
    f.close()
except:
  pass

try:
  with open('active.pkl', 'rb') as f:
    active_tx = pickle.load(f)
    f.close()
except:
  pass

try:
  savedicts()
except:
  pass

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqttc.loop_forever()

```

## [The Display Code]({{ site.baseurl }}/assets/BandSpotsHere/BandSpotsHereDisplay.py)
Click the title above to download the code.
```Python
import pickle
import os
import datetime
import time
from colorama import init, Fore, Back, Style


def printsummary(bare):

  init(convert=True)
  os.system('color 1f')
  os.system('cls')

  # dictionaries:
  #    spot_pairs[pair_key]={"ts":tspot, "sc":sp["sc"], "rc":sp["rc"], "km":kmDeg[0], "deg":kmDeg[1], "rp":sp["rp"]}
  #    active_tx[call]=tspot

  # list the active calls, count them and print them
  active_calls=""
  for active_call in active_tx:
    active_calls+=active_call+" "
  print(Fore.WHITE+Back.BLUE+str(len(active_tx))+" active Tx calls: "+active_calls)
  print()
  # for each active call ...
  for active_call in active_tx:

  # ... make two lists: "spotted_by" = receiving stations reporting the active call, "spotted" = transmitting stations reported *by* the active call
    Spotted_by=[]
    Spotted=[]
    for pair in spot_pairs:
      if active_call==spot_pairs[pair]["sc"]:
        Spotted_by.append(spot_pairs[pair]["rc"])
      if active_call==spot_pairs[pair]["rc"]:
        Spotted.append(spot_pairs[pair]["sc"])

  # ... calculate the age of the last spot of the active call, and list the details from spotted and spotted_by
    nw=datetime.datetime.now()
    t=active_tx[active_call]
    td=int((nw-t).total_seconds()/60)
    print(Fore.WHITE+Back.BLUE+active_call + " ("+str(td)+" mins)" + Fore.GREEN+ " Spotted by "+str(len(Spotted_by)) +Fore.YELLOW+ " Spotted "+str(len(Spotted)))
    if not bare:
      print(Fore.GREEN+Back.BLUE+" ".join(Spotted_by))
      print(Fore.YELLOW+Back.BLUE+" ".join(Spotted))
      print()

      
# Main ##############
spot_pairs={}
active_tx={}

while True:
  try:
    with open('spots.pkl', 'rb') as f:
      spot_pairs = pickle.load(f) 
      f.close()
  except:
    pass
  try:
    with open('active.pkl', 'rb') as f:
      active_tx = pickle.load(f)
      f.close()
  except:
    pass

  printsummary(False)
  time.sleep(15)


```

## Batch Files
These are the Windows batch files that I use to run the two Python programs:
- [BandSpotsHere.bat]({{ site.baseurl }}/assets/BandSpotsHere/BandSpotsHereDisplay.bat)
- [BandSpotsHereDisplay.bat]({{ site.baseurl }}/assets/BandSpotsHere/BandSpotsHereDisplay.bat)

I put these in the same folder as the Python code and then make shortcuts to them.







