---
layout: default
title: "BandOpticon"
permalink: /BandOpticonAppTest/
---
# Introduction
Experimental / under early development.

Next steps 
  - also (instead?) count unique calls instead of repeat spots
  - add clickable functions (e.g. click on band results for detail window, click to change DXCC group etc, reset counters ....)

# BandOpticon
<html>
<head>
<style>
.titleblock {
  grid-column: 1 / span 5;
  background-color: #2196F3;
  color:black;
  text-align: center;
  font-size: 4em;
  padding: 5px;
  grid-gap: 5px;
  min-height:40px;
}
.headblock {
  grid-column: 1 / span 5;
  background-color: #2196F3;
  color:white;
  font-weight: bold;
  padding: 5px;
  grid-gap: 5px;
  min-height:40px;
}
.bandblock {
  display: grid;
  grid-template-columns: auto auto auto auto auto;
  background-color: #2196F3;
  padding: 5px;
  grid-gap: 5px;
}
.bandblock > div {
  background-color: rgba(255, 255, 255, 0.8);
  min-height:10px;
  padding: 5px;
}

output {
    display: inline-block;
    margin-left: 0px;
    margin-right: 3px;
    width: auto;
    text-align: left;
}
label {
    display: inline-block;
    margin-left: 0px;
    margin-right: 2px;
    width: auto;
    text-align: left;
    font-size: 1em;
}

</style>
</head>


<body>

<div class="titleblock" id="title">BandOpticon</div>
<div class="headblock" id="key"></div>
<div class="bandblock" id="bandblock"></div>

<script>
  // Define the DXCCs and Bands of interest
  const DXCCs=[223,114,265,122,279,106,294];
  const Bands=["160m","80m","60m","40m","30m","20m","17m","15m","12m","10m","6m","4m","2m","70cm","23cm"];
  const refreshSeconds=2;
  let spots=[];
  let tWrite=Date.now();
</script>
  
<script>
// Write the table heading block
  key.innerHTML="Showing statistics between Home and DX, \
  where:<br><li>Home = DXCCs "+DXCCs+", and </li><li>DX = rest of world</li><br> \
  Format: Band, Spots(Home &#8680 Home), Spots(Home &#8680 DX), (Spots DX &#8680 Home)<br><br>"

// Add in the boxes for all bands, and inside them the required outputs with IDs
var toAdd = document.createDocumentFragment();
for(var i=0; i < Bands.length; i++){
   var newDiv = document.createElement('div');
   newDiv.id = Bands[i]+i;   
   // dircode is 0=H->H, 1=DX->H, 2=H->DX, 3=DX-DX
   newDiv.innerHTML="<strong>"+Bands[i]+"</strong> \
     <output id='"+Bands[i]+"0'>0</output>, \
     <output id='"+Bands[i]+"2'>0</output>, \
     <output id='"+Bands[i]+"1'>0</output>";
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
      writeStats();
    }
    sa=parseInt(getVal("sa",message));
    if(DXCCs.includes(sa)){processSpot(message); return;}
    ra=parseInt(getVal("ra",message));
    if(DXCCs.includes(ra)){processSpot(message);}
  }
  
  function processSpot(message){
    
    band=getVal("b",message);
    senderDXCC=parseInt(getVal("sa",message));
    receiverDXCC=parseInt(getVal("ra",message));
    senderCall=getVal("sc",message);
    receiverCall=getVal("rc",message);
    tSpot=parseInt(getVal("t",message));
    
    spots.push([band,tSpot,senderCall,receiverCall,senderDXCC,receiverDXCC]);
  }
  
  function writeStats(){

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
      for (let dircode=0; dircode < 3; dircode++){
// do I really need 3 output fields? Could just make this into a string for each band
        document.getElementById(Bands[iBand]+dircode).value=bandStats[iBand][dircode];
      }
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

</body>


</html>










