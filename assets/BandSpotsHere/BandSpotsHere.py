import paho.mqtt.client as mqtt
import pickle
import math
import datetime
import time
import maidenhead as mh

def hhmmFromMins(Mins):
  return str(int(Mins/60)).zfill(2)+str(int(Mins)%60).zfill(2)

def minsFromHHMM(HHMM):
  return 60*int(HHMM[0:2])+int(HHMM[2:5])

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
  with open('active.pkl', 'wb') as f:
    pickle.dump(active_tx, f)
  

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
except:
  pass

try:
  with open('active.pkl', 'rb') as f:
    active_tx = pickle.load(f)
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
