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








