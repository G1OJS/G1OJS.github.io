---
layout: default
title: "Band Spots Here"
permalink: /BandSpotsHereAppTest/
---
# Introduction
blah

<html>
<style type="text/css">
</style>
<body></body>    

<script>
  import * as Paho.MQTT from "https://cdn.jsdelivr.net/npm/paho-mqtt@1.1.0/paho-mqtt.js";

  var client;


    document.write('Connecting');
    client = new Paho.MQTT.Client("mqtt.pskreporter.info", Number(1885),"a");
    client.onMessageArrived = onMessageArrived;
    client.connect({onSuccess:onConnect});

  // called when the client connects
  function onConnect() {
    document.write('Connected');
    client.subscribe('pskr/filter/v2/+/FT8/+/+/+/+/+/#'); 
  }

  // called when a message arrives
  function onMessageArrived(message) {
    // example:
    // {"sq":49962698899,"f":28076461,"md":"FT8","rp":-18,"t":1727452137,"sc":"PC2J","sl":"JO22le91","rc":"WB5JJJ","rl":"EM35kg34","sa":263,"ra":291,"b":"10m"}
    // we need "b", "ts", "sc", "rc", "sa", "ra"}
    document.write(message.payloadString);
  }
</script>

</html>
