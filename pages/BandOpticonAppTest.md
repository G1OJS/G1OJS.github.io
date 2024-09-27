---
layout: default
title: "BandOpticon"
permalink: /BandOpticonAppTest/
---
# Introduction
blah

# BandOpticon
<html>
<head>
<style>
.bandblock {
  display: grid;
  grid-template-areas:
  'top top top top top'
  'A B C D E'
  'F G H I J'
  'K L M N O';
  grid-template-columns: 1fr 1fr  1fr  1fr  1fr;
  grid-gap: 5px;
  background-color: #2196F3;
  padding: 5px;
}

.top { grid-area: top; }
.A { grid-area: A; }
.B { grid-area: B; }
.C { grid-area: C; }
.D { grid-area: D; }
.E { grid-area: E; }
.F { grid-area: F; }
.G { grid-area: G; }
.H { grid-area: H; }
.I { grid-area: I; }
.J { grid-area: J; }
.K { grid-area: K; }
.L { grid-area: L; }
.M { grid-area: M; }
.N { grid-area: N; }
.O { grid-area: O; }

.bandblock > div {
  background-color: rgba(255, 255, 255, 0.8);
  padding: 5px;
}

input {
    margin-left: 0px;
    margin-right: 0px;
    width: 40px;
}

label {
    display: inline-block;
    margin-left: 0px;
    margin-right: 2px;
    width: 40px;
    text-align: right;
}

output {
    display: inline-block;
    margin-left: 0px;
    margin-right: 5px;
    width: 35px;
    text-align: right;
}
</style>
</head>


<body>

<div class="bandblock">
    <div class="top">
      <output id='msgs'></output>/<output id='spots'></output>
      <strong>Format = 'Spotted n times'/'Spotting n spots' </strong>
    </div>

    <div class="A">
      <strong>160m</strong><br>
      <output id='160mo'></output>/<output id='160mi'></output>
    </div>

    <div class="B">
      <strong>80m</strong><br>
      <output id='80mo'></output>/<output id='80mi'></output>
    </div>
    
    <div class="C">
      <strong>60m</strong><br>
      <output id='60mo'></output>/<output id='60mi'></output>
    </div>
  
    <div class="D">
      <strong>40m</strong><br>
      <output id='40mo'></output>/<output id='40mi'></output>
    </div>
    
    <div class="E">
      <strong>30m</strong><br>
      <output id='30mo'></output>/<output id='30mi'></output>
    </div>
    
    <div class="F">
      <strong>20m</strong><br>
      <output id='20mo'></output>/<output id='20mi'></output>
    </div>
    
    <div class="G">
      <strong>17m</strong><br>
      <output id='17mo'></output>/<output id='17mi'></output>
    </div>
    
    <div class="H">
      <strong>15m</strong><br>
      <output id='15mo'></output>/<output id='15mi'></output>
    </div>
    
    <div class="I">
      <strong>12m</strong><br>
      <output id='12mo'></output>/<output id='12mi'></output>
    </div>
    
    <div class="J">
      <strong>10m</strong><br>
      <output id='10mo'></output>/<output id='10mi'></output>
    </div>
        
    <div class="K">
      <strong>6m</strong><br>
      <output id='6mo'></output>/<output id='6mi'></output>
    </div>
    
    <div class="L">
      <strong>4m</strong><br>
      <output id='4mo'></output>/<output id='4mi'></output>
    </div>
    
    <div class="M">
      <strong>2m</strong><br>
      <output id='2mo'></output>/<output id='2mi'></output>
    </div>
    
    <div class="N">
      <strong>70cm</strong><br>
      <output id='70cmo'></output>/<output id='70cmi'></output>
    </div>
   
</div>

<script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>

<script>
  const DXCCs=",223,114,265,122,279,106,294,"
  const Band="10m"
</script>

<script>
  const client=mqtt.connect("wss://mqtt.pskreporter.info:1886");
  client.onSuccess=onConnect();
  client.on("message", (filter,message) => {onMessage(message.toString());}  );

  function onConnect() {
    document.write('Connected');
    client.subscribe('pskr/filter/v2/+/FT8/+/+/+/+/+/#'); 
  }

  function onMessage(message){    
    var a=message.indexOf('"sa":');
    var b=message.indexOf(",",a);
    var sa=message.slice(a+5,b);
    a=message.indexOf('"ra":');
    b=message.indexOf(",",a);
    var ra=message.slice(a+5,b);

    if(DXCCs.indexOf(","+sa+",")>=0 || DXCCs.indexOf(","+ra+",")>=0){
      n=document.getElementById('spots').value;
      if(n=='') {n=0} else {n=parseInt(n)};
      document.getElementById('spots').value=1+n;
      addSpot(message)
    }
  }
</script>

<script>
  function getVal(key,message){
    var a=message.indexOf('"'+key+'":');
    a=message.indexOf(':',a);
    var b=message.indexOf(",",a);
    var sa=message.slice(a+1,b);
    return sa;
  }
  function addSpot(message){

      b=getVal("b",message);
      b=b.substr(1, b.length-2);
      
      sa=getVal("sa",message);
      if(DXCCs.indexOf(","+sa+",")>0){io='o'} else {io='i'};
      n=document.getElementById(b+io).value;
      if(n=='') {n=0} else {n=parseInt(n)};
      document.getElementById(b+io).value=1+n;

  }

</script>
    
</body>


</html>




