import pickle
import os
import datetime
import time
from colorama import init, Fore, Back, Style

def printsummary():

  os.system('color 1f')
  os.system('cls')

  # dictionaries:
  #    spot_pairs[pair_key]={"ts":tspot, "sc":sp["sc"], "rc":sp["rc"], "km":kmDeg[0], "deg":kmDeg[1], "rp":sp["rp"]}
  #    active_tx[call]=tspot

  # list the active calls, count them and print them
  active_calls_even=[]
  active_calls_odd=[]  
  for active_call in active_tx:
    tspot=active_tx[active_call].second %30
    if(int(tspot/15)==0):
      active_calls_even.append(active_call)
    else:
      active_calls_odd.append(active_call)
  nwUTCstr=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
  print(Style.BRIGHT+Fore.CYAN+Back.BLUE+nwUTCstr)
  print(Style.BRIGHT+Fore.WHITE+Back.BLUE+str(len(active_calls_even))+" active Tx calls even/1st: "+" ".join(active_calls_even))
  print(Style.BRIGHT+Fore.WHITE+Back.BLUE+str(len(active_calls_odd))+" active Tx calls odd/2nd:  "+" ".join(active_calls_odd))
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
    print(Style.BRIGHT+Fore.WHITE+Back.BLUE+active_call + " ("+str(td)+" mins)" + Fore.GREEN+ " Spotted by "+str(len(Spotted_by)) +Fore.YELLOW+ " Spotted "+str(len(Spotted)))
    for i in range(0, len(Spotted_by), 10):
      print(Style.BRIGHT+Fore.GREEN+Back.BLUE+" ".join(Spotted_by[i:i + 10]))
    for i in range(0, len(Spotted), 10):
      print(Style.BRIGHT+Fore.YELLOW+Back.BLUE+" ".join(Spotted[i:i + 10]))
    print()

      
# Main ##############
spot_pairs={}
active_tx={}

init(convert=True)

while True:

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

  printsummary()
  time.sleep(15)








