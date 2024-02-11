---
layout: default
calculator_style: true
title: "Capacitor Padding Calculator"
permalink: /Capacitor-Padding-Calc/
---
# Introduction
This calculator works out the values needed for capacitors C1 and C2 in the diagrams below to achieve a specified range of output capacitance Cout, and shows the range of capacitance achieved when using specified values for C1 and C2. The maths behind the calculator is described on the calculator's parent page [here]({{ site.baseurl }}/calculating-padding-capacitors).

# Usage
Edit the values in the first four boxes. The calculator will then show the values of C1 and C2 needed to achieve this range using each configuration. Note that errors will occur if unachievable ranges are specified. Once calculated, these values are copied to the "Padding Capacitors Used" boxes and used to calculate the final row which shows the capacitance ranges achieved. You can edit the "Padding Capacitors Used" boxes to see the effect of chosing different values (e.g. to pick from E12 values or simply to experiment).

<html>
<style type="text/css">
img {
    width: 100%;
}
input {
    height: 15px;
    width: 35px;
    float: left;
    margin-bottom: 5px;
      margin-left: 0px;
  margin-right: 5px;
}
span.first {
  width: 200px;
  margin-left: 0px;
  margin-right: 5px;
  float: left;
  text-align: left;
}
span {
  width: 200px;
  margin-left: 0px;
  margin-right: 5px;
  float: left;
  text-align: center;
}
div {
  clear: both;
  min-width: 640px;
}
label {
  width: 35px;
  margin-left: 0px;
  margin-right: 5px;
  float: left;
  text-align: right;
}
.readonly { background-color: #d1d1d1; }
</style>

<meta name="viewport" content="width=640">

<body onload="CalcPadding()" >
<div> <!-- main div -->
  <h2>Available and needed capacitance ranges:</h2>
  <span class="first">Variable Capacitor Range</span>
  <label>Min</label><input type="text" id="Alpha" value="10" onchange="CalcPadding()" />
  <label>Max</label><input type="text" id="Beta" value="250" onchange="CalcPadding()" />
  <div></div>
  <span class="first">Needed Capacitance Range</span>
  <label>Min</label><input type="text" id="Ca" value="200" onchange="CalcPadding()"/>
  <label>Max</label><input type="text" id="Cb" value="240" onchange="CalcPadding()"/>
  <div></div>
 
  <h2>Exact Solutions:</h2>
  <span class="first">.</span>
  <span><b>Configuration a)</b></span>
  <span><b>Configuration b)</b></span>
  <div></div>
  <span class="first">.</span>
  <span><img src="https://g1ojs.github.io/assets/img/Capacitor%20padding%20circuit%201.png"/></span>
  <span><img src="https://g1ojs.github.io/assets/img/Capacitor%20padding%20circuit%202.png"/></span>
  <div></div>
  <span class="first">Padding Capacitors Required</span>
  <span>
    <label>C1</label><input type="text" id="CFG1_C1Req" class="readonly" readonly=true />
    <label>C2</label><input type="text" id="CFG1_C2Req" class="readonly" readonly=true />
  </span>
  <span>
    <label>C1</label><input type="text" id="CFG2_C1Req" class="readonly" readonly=true/>
    <label>C2</label><input type="text" id="CFG2_C2Req" class="readonly" readonly=true/>
  </span>
  <div></div>
  <h2>Practical Solutions:</h2>
  <span class="first">Padding Capacitors Used</span>
  <span>
    <label>C1</label><input type="text" id="CFG1_C1Used"   onchange="EvaluatePadding()"/>
    <label>C2</label><input type="text" id="CFG1_C2Used"  onchange="EvaluatePadding()"/>
  </span>
  <span>
    <label>C1</label><input type="text" id="CFG2_C1Used"  onchange="EvaluatePadding()"/>
    <label>C2</label><input type="text" id="CFG2_C2Used"  onchange="EvaluatePadding()"/>
  </span>
  <div></div>
  
  <span class="first">Output Capacitance</span>
  <span>
    <label>Min</label><input type="text" class="readonly" id="CFG1_Cmin" size="5" readonly=true />
    <label>Max</label><input type="text" class="readonly" id="CFG1_Cmax" size="5" readonly=true />
  </span>
  <span>
    <label>Min</label><input type="text" class="readonly" id="CFG2_Cmin" size="5" readonly=true  />
    <label>Max</label><input type="text" class="readonly" id="CFG2_Cmax" size="5" readonly=true  />
  </span>
  <div></div>

  <h4>Maximum Capacitor Voltages (scaled to 1V at Cout):</h4>
  <span class="first">C1, at max Cout </span>
  <span style="width: 125px;">.</span>
  <input type="text" class="readonly" id="CFG1_C1V_Cmax" size="5" readonly=true />  
  <span style="width: 150px;">.</span>
  <input type="text" class="readonly" id="CFG2_C1V_Cmax" size="5" readonly=true />
   <div></div>
   <span class="first">CV, at min Cout</span>
   <span style="width: 35px;">.</span>
   <input type="text" class="readonly" id="CFG1_CVV_Cmin" size="5" readonly=true />
   <span style="width: 155px;">.</span>
   <input type="text" class="readonly" id="CFG2_CVV_Cmin" size="5" readonly=true />
  <div></div>
In both configurations, the maximum voltage across C1 occurs at maximum output capacitance, and the maximum voltage across CV occurs at minimum output capacitance. The voltage across C2 is the same as that across CV in configuration a), and the same as that across the output in configuration b).
  <div></div>

</div> <!-- main div -->  

<div style="height: 50px;"></div>

</body>
</html>

<script>

function CalcPadding() {

//Calculate required C1 and C2 from input values

//Get input parameters
    Alpha = Number(document.getElementById("Alpha").value);
    Beta = Number(document.getElementById("Beta").value);
    Ca = Number(document.getElementById("Ca").value);
    Cb = Number(document.getElementById("Cb").value);

//C1 and C2 for config a)
    aa=1/Ca-1/Cb;
    bb=aa*Alpha + aa*Beta;
    cc=aa*Alpha*Beta + Alpha - Beta;
    CFG1_C2=(-bb+Math.sqrt(bb*bb-4*aa*cc))/(2*aa)
    CFG1_C1=1/(1/Cb-1/(CFG1_C2+Beta))

//C1 and C2 for config b)
    aa=Cb-Ca+Alpha-Beta;
    bb=(Cb-Ca)*(Alpha+Beta);
    cc=Alpha*Beta*(Cb-Ca);
    CFG2_C1=(-bb-Math.sqrt(bb*bb-4*aa*cc))/(2*aa)
    CFG2_C2=Cb-1/(1/CFG2_C1+1/Beta)

// Write C1 and C2 for config a)
    document.getElementById("CFG1_C1Req").value = CFG1_C1.toString();
    document.getElementById("CFG1_C2Req").value = CFG1_C2.toString();
    document.getElementById("CFG1_C1Used").value = Math.max(0,Math.round(CFG1_C1)).toString();
    document.getElementById("CFG1_C2Used").value = Math.max(0,Math.round(CFG1_C2)).toString();

// Write C1 and C2 for config a)
    document.getElementById("CFG2_C1Req").value = CFG2_C1.toString();
    document.getElementById("CFG2_C2Req").value = CFG2_C2.toString();
    document.getElementById("CFG2_C1Used").value = Math.max(0,Math.round(CFG2_C1)).toString();
    document.getElementById("CFG2_C2Used").value = Math.max(0,Math.round(CFG2_C2)).toString();

// Call to write resulting values
    EvaluatePadding()
}

function EvaluatePadding() {
//Calculate output capacitance range from used C1 and C2

//Get all circuit capacitance values
    Alpha = Number(document.getElementById("Alpha").value);
    Beta = Number(document.getElementById("Beta").value);
    CFG1_C1Used = Number(document.getElementById("CFG1_C1Used").value);
    CFG1_C2Used = Number(document.getElementById("CFG1_C2Used").value);
    CFG2_C1Used = Number(document.getElementById("CFG2_C1Used").value);
    CFG2_C2Used = Number(document.getElementById("CFG2_C2Used").value);

//Min and Max capacitance for config a)
    CFG1_Cmin=1/(1/CFG1_C1Used+1/(CFG1_C2Used+Alpha));
    CFG1_Cmax=1/(1/CFG1_C1Used+1/(CFG1_C2Used+Beta));	
    document.getElementById("CFG1_Cmin").value = CFG1_Cmin.toString();
    document.getElementById("CFG1_Cmax").value = CFG1_Cmax.toString();

//Min and Max capacitance for config b)
    CFG2_Cmin=CFG2_C2Used+1/(1/CFG2_C1Used+1/Alpha);
    CFG2_Cmax=CFG2_C2Used+1/(1/CFG2_C1Used+1/Beta);
    document.getElementById("CFG2_Cmin").value = CFG2_Cmin.toString();
    document.getElementById("CFG2_Cmax").value = CFG2_Cmax.toString();

// Max voltages across capacitors
    CFG1_C1V_Cmax=CFG1_Cmax/CFG1_C1Used
    CFG1_CVV_Cmin=CFG1_Cmax/(Beta+CFG1_C2Used)    
    CFG2_C1V_Cmax=(CFG2_Cmax-CFG2_C2Used)/CFG2_C1Used
    CFG2_CVV_Cmin=1-CFG2_C1V_Cmax
    document.getElementById("CFG1_C1V_Cmax").value = CFG1_C1V_Cmax.toString();
    document.getElementById("CFG1_CVV_Cmin").value = CFG1_CVV_Cmin.toString();
    document.getElementById("CFG2_C1V_Cmax").value = CFG2_C1V_Cmax.toString();
    document.getElementById("CFG2_CVV_Cmin").value = CFG2_CVV_Cmin.toString();	
}

</script>
