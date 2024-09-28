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
  grid-template-columns: auto auto auto;
  background-color: #2196F3;
  padding: 5px;
  grid-gap: 5px;
}
.bandblock > div {
  background-color: rgba(255, 255, 255, 0.8);
  min-height:100px;
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

<div class="headblock" id="headblock">
  
</div>

<div class="bandblock" id="bandblock"></div>

<script>
  // Define the DXCCs and Bands of interest
  const DXCCs=[223,114,265,122,279,106,294];
  const Bands=["160m","80m","60m","40m","30m","20m","17m","15m","12m","10m","6m","4m","2m","70cm","23cm"];
</script>
  
<script>
// Write the table heading block
  headblock.innerHTML="Showing statistics between Home and DX, where<br>Home = DXCCs "+DXCCs+", and <br>DX = rest of world"

// Add in the boxes for all bands, and inside them the required outputs with IDs
var toAdd = document.createDocumentFragment();
for(var i=0; i < Bands.length; i++){
   var newDiv = document.createElement('div');
   newDiv.id = Bands[i]+i;   
   newDiv.innerHTML="<strong>"+Bands[i]+"</strong> \
     <label>Total Spots</label><br> \
     <label>H&#8680H:</label><output id='"+Bands[i]+"3'>0</output> \
     <label>H&#8680DX:</label><output id='"+Bands[i]+"2'>0</output> \
     <label>DX&#8680H:</label><output id='"+Bands[i]+"1'>0</output>";
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
    sa=parseInt(getVal("sa",message));
    if(DXCCs.includes(sa)){processSpot(message); return;}
    ra=parseInt(getVal("ra",message));
    if(DXCCs.includes(ra)){processSpot(message);}
  }
  
  function processSpot(message){
    band=getVal("b",message);
    senderDXCC=parseInt(getVal("sa",message));
    receiverDXCC=parseInt(getVal("ra",message));
    incrementSpotCounts(band,senderDXCC,receiverDXCC);
  }
  
  function incrementSpotCounts(band,senderDXCC,receiverDXCC){
    var dircode=0;
    if(DXCCs.includes(senderDXCC)) {dircode+=1};
    if(DXCCs.includes(receiverDXCC)) {dircode+=2};
    var elID=band+dircode;
    n=parseInt(document.getElementById(elID).value);
    document.getElementById(elID).value=1+n;
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







