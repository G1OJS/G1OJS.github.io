---
layout: default
title: "Capacitor Padding Calculator Config 1"
permalink: /Capacitor-Padding-Calc/
---

This calculator works out the values needed for capacitors C1 and C2 in the diagrams below to achieve a specified range of output capacitance Cout, and shows the range of capacitance achieved when using specified values for C1 and C2
	
<p></p>

| Configuration a)  | Configuration b) |
| ------------- | ------------- |
| ![Padding capacitors config 1]({{ site.baseurl }}/assets/img/Capacitor padding circuit 1.png "Configuration a)" )  | ![Padding capacitors config 2]({{ site.baseurl }}/assets/img/Capacitor padding circuit 2.png "Configuration b)" )  |

<p></p>

Usage: Edit the values in the first four boxes. The calculator will show the values of C1 and C2 needed to achieve this range. Note that errors will occur if unachievable ranges are specified. Once calculated, these values are copied to the "Padding Capacitors Used" boxes and used to calculate the final row which shows the capacitance range achieved. You can edit the "Padding Capacitors Used" boxes to see the effect of chosing different values (e.g. to pick from E12 values or simply to experiment).
<p> </p>
<p> </p>
<html> 
<head>
<style type="text/css">
body {margin: 30px;}
form  { display: table; border: 1px solid red; }
p     { display: table-row;}
label { display: table-cell;}
input { display: table-cell;}
	.readonly {background-color : #d1d1d1;}
</style> 
</head>
<body>
<form>
<p>
 <label></label> 
 <label>Min</label>
 <label></label> 
 <label>Max</label>
</p>
<p> 
 <label for="Alpha">Variable Capacitor Range </label><input type="text" id="Alpha" value="10" size="5" onchange="CalcPadding()">
 <label for="Beta"></label><input type="text" id="Beta" value="250" size="5" onchange="CalcPadding()">
</p>
<p>
  <label for = "Ca">Needed Capacitance Range</label><input type="text" id="Ca" value="200" size="5" onchange="CalcPadding()">
  <label for = "Cb"></label><input type="text" id="Cb" value="240" size="5" onchange="CalcPadding()">
</p>
<p> </p>
<p>
 <label></label> 
 <label>C1</label>
 <label></label> 
 <label>C2</label>
 <label></label> 
 <label>C1</label>
 <label></label> 
 <label>C2</label>
</p>
<p>
  <label for ="CFG1_C1Req">Padding Capacitors Required</label><input type="text" class="readonly" id="CFG1_C1Req" size="5" readonly>
  <label for = "CFG1_C2Req"></label><input type="text" class="readonly" id="CFG1_C2Req" size="5" readonly>
  <label for ="CFG2_C1Req"></label><input type="text" class="readonly" id="CFG2_C1Req" size="5" readonly>
  <label for = "CFG2_C2Req"></label><input type="text" class="readonly" id="CFG2_C2Req" size="5" readonly>
</p>
<p>
  <label for ="CFG1_C1Used">Padding Capacitors Used</label><input type="text" id="CFG1_C1Used"  size="5" onchange="EvaluatePadding()">
  <label for = "CFG1_C2Used"></label><input type="text" id="CFG1_C2Used" size="5" onchange="EvaluatePadding()">
  <label for ="CFG2_C1Used"></label><input type="text" id="CFG2_C1Used"  size="5" onchange="EvaluatePadding()">
  <label for = "CFG2_C2Used"></label><input type="text" id="CFG2_C2Used" size="5" onchange="EvaluatePadding()">
</p>
<p> </p>
<p>
 <label></label> 
 <label>Min</label>
 <label></label> 
 <label>Max</label> 
 <label></label> 
 <label>Min</label>
 <label></label> 
 <label>Max</label>
</p>
<p>
  <label for="CFG1_Cmin">Output Capacitance</label><input type="text" class="readonly" id="CFG1_Cmin" size="5" readonly>
  <label for="CFG1_Cmax"></label><input type="text" class="readonly" id="CFG1_Cmax" size="5" readonly>
  <label for="CFG2_Cmin"></label><input type="text" class="readonly" id="CFG2_Cmin" size="5" readonly>
  <label for="CFG2_Cmax"></label><input type="text" class="readonly" id="CFG2_Cmax" size="5" readonly>
</p>

</form>

</body>
</html>

<script>
function CalcPadding() {

//Calculate required C1 and C2 from input values
    Alpha = Number(document.getElementById("Alpha").value);
    Beta = Number(document.getElementById("Beta").value);
    Ca = Number(document.getElementById("Ca").value);
    Cb = Number(document.getElementById("Cb").value);

    aa=1/Ca-1/Cb;
    bb=aa*Alpha + aa*Beta;
    cc=aa*Alpha*Beta + Alpha - Beta;

    CFG1_C2=(-bb+Math.sqrt(bb*bb-4*aa*cc))/(2*aa)
    CFG1_C1=1/(1/Cb-1/(CFG1_C2+Beta))

    document.getElementById("CFG1_C1Req").value = CFG1_C1.toString();
    document.getElementById("CFG1_C2Req").value = CFG1_C2.toString();

    document.getElementById("CFG1_C1Used").value = Math.max(0,Math.round(CFG1_C1)).toString();
    document.getElementById("CFG1_C2Used").value = Math.max(0,Math.round(CFG1_C2)).toString();

	EvaluatePadding()
}

function EvaluatePadding() {
//Calculate output capacitance range from used C1 and C2
    Alpha = Number(document.getElementById("Alpha").value);
    Beta = Number(document.getElementById("Beta").value);
    CFG1_C1Used = Number(document.getElementById("CFG1_C1Used").value);
    CFG1_C2Used = Number(document.getElementById("CFG1_C2Used").value);

    CFG1_Cmin=1/(1/CFG1_C1Used+1/(CFG1_C2Used+Alpha));
    CFG1_Cmax=1/(1/CFG1_C1Used+1/(CFG1_C2Used+Beta));	
    document.getElementById("CFG1_Cmin").value = CFG1_Cmin.toString();
    document.getElementById("CFG1_Cmax").value = CFG1_Cmax.toString();
}
</script>
