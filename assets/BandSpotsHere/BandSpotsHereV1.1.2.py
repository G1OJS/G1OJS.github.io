import paho.mqtt.client as mqtt
import os
import datetime
from pynput import keyboard
import pygetwindow as pgw
import time
from colorama import init, Fore, Back, Style
import sys

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

  sp["sa"]=sp["sa"].zfill(3)
  sp["ra"]=sp["ra"].zfill(3)

  return sp

# The callback for when the client receives a CONNACK response from the server.
# Subscribing in on_connect() means that if we lose the connection and
# reconnect then subscriptions will be renewed
def on_connect(client, userdata, flags, reason_code, properties):
    connectmessage("Connected with result code '" + str(reason_code)+"'")

    # This subscribe gets all FT8 reports
    client.subscribe("pskr/filter/v2/+/FT8/+/+/+/+/+/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
  global spots,lastdisplay
  sp=msg_to_spot_dict(msg)

  # if neither end of the spot pair is in the DXCC list, we aren't interested
  if(sp["sa"] not in DXCCs and sp["ra"] not in DXCCs): 
    return

  # record the spot pair with details
  # DON'T categorise into Tx/Rx-only here, because each call could have several spots (some tx some rx)
  tspot=datetime.datetime.fromtimestamp(int(sp["t"]))
  key=sp["sc"]+"->"+sp["rc"]
  spots[key]={"b":sp["b"], "ts":tspot, "sc":sp["sc"], "rc":sp["rc"], "sa":sp["sa"], "ra":sp["ra"], "rp":sp["rp"]}

  tnow=datetime.datetime.now()
  td=(tnow-lastdisplay).total_seconds()
  if(td>15): 
    # flush out old spot pairs
    delete= [pair for pair in spots if (tnow-spots[pair]["ts"]).total_seconds()/60 > stale_mins]
    for pair in delete:
      del spots[pair]
    printsummary()

def connectmessage(cm):
  os.system('color 1f')
  os.system('cls')
  print(Style.BRIGHT+Fore.CYAN+Back.BLUE+Vstr)
  print(Style.BRIGHT+Fore.CYAN+Back.BLUE+cm)
  print()
  print(Style.BRIGHT+Fore.CYAN+Back.BLUE+"Gathering spots for "+" ".join(bands))
  print(Style.BRIGHT+Fore.CYAN+Back.BLUE+"For spots in & out of DXCCs "+" ".join(DXCCs))
  print()
  print(Style.BRIGHT+Fore.CYAN+Back.BLUE+"Stats will appear every 15 seconds")
  print()
  print(Style.BRIGHT+Fore.WHITE+Back.BLUE+"Press b to cycle through bands, d to toggle detail")
  time.sleep(8)

def printsummary():
  global lastdisplay
  tnow=datetime.datetime.now()
  lastdisplay=datetime.datetime.now()
  gathertime=round((tnow-starttime).total_seconds()/60,1)
  sp0ts=spots.copy()

  os.system('color 1f')
  os.system('cls')

  # print an informative header
  nwUTCstr=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
  print(Style.BRIGHT+Fore.CYAN+Back.BLUE+Vstr)
  print(Style.BRIGHT+Fore.CYAN+Back.BLUE+nwUTCstr)
  print(Style.BRIGHT+Fore.CYAN+Back.BLUE+"Watching to/from DXCCs "+",".join(DXCCs) + " for "+str(gathertime)+" mins")
  print()

  # count spots on all bands of interest
  cstr=""
  for b in bands:
    bc=sum(1 for k in sp0ts.keys() if sp0ts[k]["b"] == b)
    tmp=b+":"+str(bc)+" "
    if(b==band):
      tmp=Fore.WHITE+tmp+Fore.CYAN
    cstr+=tmp
  print("Spots (all bands): "+cstr)
  print()
  print(Fore.WHITE+"On "+band+":"+Fore.CYAN)

  # find the active calls on the watched band, and categorise them
  # check for all tx calls first
  active_calls_Tx=[]
  for pair in sp0ts:
    if ((sp0ts[pair]["b"]==band) and (sp0ts[pair]["sa"] in DXCCs) and (sp0ts[pair]["sc"] not in active_calls_Tx)):
      active_calls_Tx.append(sp0ts[pair]["sc"])

  # active Tx calls that are also receiving
  active_calls_TxRx=[]
  for pair in sp0ts:
    if ((sp0ts[pair]["b"]==band) and (sp0ts[pair]["ra"] in DXCCs) and (sp0ts[pair]["rc"] in active_calls_Tx) and (sp0ts[pair]["rc"] not in active_calls_TxRx)):
      active_calls_TxRx.append(sp0ts[pair]["rc"])
      active_calls_Tx.remove(sp0ts[pair]["rc"])

  # now the calls that are just rx
  active_calls_Rx=[]
  for pair in sp0ts:
    if ((sp0ts[pair]["b"]==band) and (sp0ts[pair]["ra"] in DXCCs) and (sp0ts[pair]["rc"] not in active_calls_TxRx+active_calls_Tx+active_calls_Rx)):
      active_calls_Rx.append(sp0ts[pair]["rc"])

  if not details:

    # print out the number of calls in each category and list them
    print()
    print(Style.BRIGHT+Fore.GREEN+Back.BLUE+str(len(active_calls_TxRx))+" active calls transmitting and receiving:")
    print(" ".join(active_calls_TxRx))
    print()
    print(Style.BRIGHT+Fore.YELLOW+Back.BLUE+str(len(active_calls_Tx))+" active calls transmitting but not receiving:")
    print(" ".join(active_calls_Tx))
    print()
    print(Style.BRIGHT+Fore.RED+Back.BLUE+str(len(active_calls_Rx))+" active calls only receiving:  ")
    print(" ".join(active_calls_Rx))
    print()
    print(Style.BRIGHT+Fore.WHITE+Back.BLUE+"~details hidden~")

  else:

    # print out the number of calls in each category and list them together with spotter/spotted
    print()
    # for each active TxRx call make two lists: "spotted_by" = receiving stations reporting the active call, "spotted" = transmitting stations reported *by* the active call
    # note that here, only, the "other end" of the spot can be global
    print(Style.BRIGHT+Fore.GREEN+Back.BLUE+str(len(active_calls_TxRx))+" active calls transmitting and receiving:")
    for call in active_calls_TxRx:
      Spotted_by=[]
      Spotted=[]
      for pair in sp0ts:
        if (sp0ts[pair]["b"]==band):
          if call==sp0ts[pair]["sc"]:
            Spotted_by.append(sp0ts[pair]["rc"])
          if call==sp0ts[pair]["rc"]:
            Spotted.append(sp0ts[pair]["sc"])
      print(Style.BRIGHT+Fore.GREEN+Back.BLUE+call + " -> " + " ".join(Spotted_by))
      print(Style.BRIGHT+Fore.GREEN+Back.BLUE+call + " <- " + " ".join(Spotted))
    print()

    # for each active Tx-only call make one lists: "spotted_by" = receiving stations reporting the active call
    # note that here, only, the "other end" of the spot can be global
    print(Style.BRIGHT+Fore.YELLOW+Back.BLUE+str(len(active_calls_Tx))+" active calls transmitting but not receiving:")
    for call in active_calls_Tx:
      Spotted_by=[]
      for pair in sp0ts:
        if (sp0ts[pair]["b"]==band):
          if call==sp0ts[pair]["sc"]:
            Spotted_by.append(sp0ts[pair]["rc"])
      print(Style.BRIGHT+Fore.YELLOW+Back.BLUE+call + " -> " + " ".join(Spotted_by))
    print()

    # for each active Rx-only call make one lists: "spotted" = transmitting stations reported *by* the active call
    # note that here, only (as above), the "other end" of the spot can be global
    print(Style.BRIGHT+Fore.RED+Back.BLUE+str(len(active_calls_Rx))+" active calls only receiving:  ")
    for call in active_calls_Rx:
      Spotted=[]
      for pair in sp0ts:
        if (sp0ts[pair]["b"]==band):
          if call==sp0ts[pair]["rc"]:
            Spotted.append(sp0ts[pair]["sc"])
      print(Style.BRIGHT+Fore.RED+Back.BLUE+call + " <- " + " ".join(Spotted))

def key_press(key):
  global keyPressed,band,details

  if(str(pgw.getActiveWindow().title)!=launchwindow): return

  try:
    keyPressed=key.char
  except:
    return

  if(keyPressed in "bB"):
    i=(bands.index(band)+1) % (len(bands))
    band = bands[i]

  if(keyPressed in "dD"):
    details=not(details)
  
  printsummary()
    

def key_release(key):
  pass

# keyboard listener for key events
listener = keyboard.Listener(
    on_press=key_press,
    on_release=key_release)
listener.start()

      
# Main ##############
Vstr="BandSpotsHereV1.1.2 by G1OJS"
bands=sys.argv[1].split(",")
band=bands[0]
DXCCs=sys.argv[2].split(",")
stale_mins=int(sys.argv[3])

launchwindow=str(pgw.getActiveWindow().title)

spots={}
keyPressed=""
details=True

init(convert=True)
starttime=datetime.datetime.now()
lastdisplay=datetime.datetime.now()
#printsummary()

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect("mqtt.pskreporter.info", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqttc.loop_forever()











