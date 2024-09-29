---
layout: default
title: "BandOpticon"
permalink: /BandOpticonAppTest/
---
# Introduction
Experimental / under early development. Displays number of FT8 spots on all bands categorised by zone of origin and reception. Updates in real time.

Refresh the page to reset counters.

Next steps 
  - GUI to edit DXCCs
  - Extra detail? What to include? Active Tx call list?
  - Format improvements
  - UTC clock date & time
  - Credits

# BandOpticon

<html>
<head>
<style>
:root { background-color: #2196F3; color:black;text-align: left;}
div {margin: 2px;  padding: 5px;}
#title {text-align: center; font-size: 4em;}
#subtitle {text-align: center; font-size: 1.3em;}
.detail > div {background-color: rgba(255, 255, 255, 0.8);}
.bandblock {display: grid; grid-template-columns: auto auto auto auto auto;}
.bandblock > div {background-color: rgba(255, 255, 255, 0.8);}
</style>
</head>
<body><div>

<div id="title">BandOpticon</div>
<div id="subtitle">Live Pskreporter statistics for FT8 spots on all bands between Home and DX</div>
<div class="detail" id="controls"></div>
<div class="detail" id="detail"></div>
<div class="bandblock" id="bandblock"></div>

<script>
  // Define the DXCCs and Bands of interest
  if(localStorage.getItem('DXCCs')){
    var DXCCs=localStorage.getItem('DXCCs');
  } else {
    DXCCs=[223,114,265,122,279,106,294];
    localStorage.setItem('DXCCs', DXCCs);
  }
  const Bands=["160m","80m","60m","40m","30m","20m","17m","15m","12m","10m","6m","4m","2m","70cm","23cm"];
  const refreshSeconds=2;
  const purgeSeconds=600;
  let spots=[];
  let tWrite=Date.now();
</script>
  
<script>
// Write the initial controls and details content
  controls.innerHTML="<div>Home = DXCCs "+DXCCs+" <a href='#' onclick='editDXCCs();'>edit</a>"
  detail.innerHTML="<div>Band box layout:<br><b>Band</b><br> \
  Spots: number of spots Home &#8680 Home / Home &#8680 DX / DX &#8680 Home<br> \
  Tx Calls: number of unique calls in 'Home' received by anyone<br> \
  Rx Calls: number of unique calls in 'Home' receiving anyone</div>"
  
  function editDXCCs(){
    var resp=prompt("Enter DXCCs",DXCCs);
    var regex=/^(([0-9]+)(,(?=[0-9]))?)+$/;
    if (regex.test(resp)) {
      DXCCs=resp;
      controls.innerHTML="<div>Home = DXCCs "+DXCCs+" <a href='#' onclick='editDXCCs();'>edit</a>";
      localStorage.setItem('DXCCs', DXCCs);
      spots=[];
    } else {
      alert("DXCC list must be comma-separated integers");
    }
  }

// Add in the boxes for all bands, and inside them the required outputs with IDs
var toAdd = document.createDocumentFragment();
for(var i=0; i < Bands.length; i++){
   var newDiv = document.createElement('div');
   newDiv.id = Bands[i];   
   // dircode is 0=H->H, 1=DX->H, 2=H->DX, 3=DX-DX
   newDiv.innerHTML="<strong>"+Bands[i]+"</strong><br> \
     <output id='"+Bands[i]+"spots'></output><br> \
     <output id='"+Bands[i]+"calls'></output>";
   toAdd.appendChild(newDiv);
}
document.getElementById('bandblock').appendChild(toAdd);
</script>

<!--Get the library for MQTT functions -->
<script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>

<script>
  // Connect to Pskreporter and subscribe on connect
  const client=mqtt.connect("wss://mqtt.pskreporter.info:1886");
  client.onSuccess=client.subscribe('pskr/filter/v2/+/FT8/+/+/+/+/+/#');
  client.on("message", (filter,message) => {onMessage(message.toString());}  );

  function onMessage(message){    
    if ( (Date.now()-tWrite)/1000 > refreshSeconds ){
    	tWrite=Date.now();
      purgeSpots();
      writeBandSpotStats();
      writeBandActiveCallStats();
    }
    sa=parseInt(getVal("sa",message));
    if(DXCCs.includes(sa)){addSpot(message); return;}
    ra=parseInt(getVal("ra",message));
    if(DXCCs.includes(ra)){addSpot(message);}
  }
  
  function purgeSpots(){
    var del=[];
    for (let iSpot=1; iSpot < spots.length; iSpot++) {
      var spot=spots[iSpot];
      var tSpot=spot[1];
      if((Date.now()/1000-tSpot) > purgeSeconds) {del.push(iSpot)}
    }
    for (let iSpot=1; iSpot <del.length;iSpot++){spots.splice(del[iSpot],1)}
  }
  
  function addSpot(message){
    band=getVal("b",message);
    senderDXCC=parseInt(getVal("sa",message));
    receiverDXCC=parseInt(getVal("ra",message));
    senderCall=getVal("sc",message);
    receiverCall=getVal("rc",message);
    tSpot=parseInt(getVal("t",message));
    spots.push([band,tSpot,senderCall,receiverCall,senderDXCC,receiverDXCC]);
  }
  
  function writeBandSpotStats(){
 //   misc.innerHTML="Total spots: "+spots.length;
  
    var bandStats = new Array(Bands.length);
    for(let i = 0; i < Bands.length; i++) {
        bandStats[i]=[0,0,0];
    }
    for (let iSpot=1; iSpot < spots.length; iSpot++) {
      var spot=spots[iSpot];
      var dircode=0;    // dircode is 0=H->H, 1=DX->H, 2=H->DX, 3=DX-DX
      if(!DXCCs.includes(spots[iSpot][4])) {dircode+=1};
      if(!DXCCs.includes(spots[iSpot][5])) {dircode+=2};
      iBand=Bands.indexOf(spot[0]);
      bandStats[iBand][dircode]+=1;
    } 
    for (let iBand=0; iBand < Bands.length; iBand++) {
      var snum=bandStats[iBand];
      document.getElementById(Bands[iBand]+"spots").value="Spots "+snum[0]+"/"+snum[2]+"/"+snum[1];
    }
  }
  
   function writeBandActiveCallStats(){
  //spots.push([band,tSpot,senderCall,receiverCall,senderDXCC,receiverDXCC])
     for (iBand=0; iBand<Bands.length; iBand++){

       var active_tx=new Set;
       var active_rx=new Set;
       for (let iSpot=1; iSpot < spots.length; iSpot++) {
         var spot=spots[iSpot];
         if(spot[0]==Bands[iBand]){
           if(DXCCs.includes(spot[4])) {active_tx.add(spot[2])};
           if(DXCCs.includes(spot[5])) {active_rx.add(spot[3])};
         }
       }
  //     console.log(Bands[iBand],active_tx);
       document.getElementById(Bands[iBand]+"calls").innerHTML="Tx Calls "+active_tx.size+"<br>"+"Rx Calls "+active_rx.size;
     }
   }
    
  
  function getVal(key,message){
    var iVal=message.indexOf('"'+key+'":');
    var iColon=message.indexOf(':',iVal);
    var iComma=message.indexOf(",",iColon);
    var val=message.slice(iColon+1,iComma).replace(/"/g, '');
    return val;
  }
 

</script>

</div></body>
</html>













