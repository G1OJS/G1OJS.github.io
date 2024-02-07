<!DOCTYPE html>
<html> 
<head>
<meta charset=utf-8 />
<title>G1OJS Capacitor Padding Calculator</title>
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

<img src='assets/img/Capacitor padding circuit 1.png'>
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
<p>&nbsp</p>
<p>
 <label></label> 
 <label>C1</label>
 <label></label> 
 <label>C2</label>
</p>
<p>
  <label for ="C1Req">Padding Capacitors Required</label><input type="text" class="readonly" id="C1Req" size="5" readonly ">
  <label for = "C2Req"></label><input type="text" class="readonly" id="C2Req" size="5" readonly>
</p>
<p>
  <label for ="C1Used">Padding Capacitors Used</label><input type="text" id="C1Used"  size="5" onchange="EvaluatePadding()">
  <label for = "C2Used"></label><input type="text" id="C2Used" size="5" onchange="EvaluatePadding()">
</p>
<p>&nbsp</p>
<p>
 <label></label> 
 <label>Min</label>
 <label></label> 
 <label>Max</label>
</p>
<p>
  <label for="Cmin">Output Capacitance</label><input type="text" class="readonly" id="Cmin" size="5" readonly>
  <label for="Cmax"></label><input type="text" class="readonly" id="Cmax" size="5" readonly>
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

    C2=(-bb+Math.sqrt(bb*bb-4*aa*cc))/(2*aa)
    C1=1/(1/Cb-1/(C2+Beta))

    document.getElementById("C1Req").value = C1.toString();
    document.getElementById("C2Req").value = C2.toString();

    document.getElementById("C1Used").value = Math.max(0,Math.round(C1)).toString();
    document.getElementById("C2Used").value = Math.max(0,Math.round(C2)).toString();

	EvaluatePadding()
}

function EvaluatePadding() {
//Calculate output capacitance range from used C1 and C2
    Alpha = Number(document.getElementById("Alpha").value);
    Beta = Number(document.getElementById("Beta").value);
    C1Used = Number(document.getElementById("C1Used").value);
    C2Used = Number(document.getElementById("C2Used").value);

    Cmin=1/(1/C1Used+1/(C2Used+Alpha));
    Cmax=1/(1/C1Used+1/(C2Used+Beta));	
    document.getElementById("Cmin").value = Cmin.toString();
    document.getElementById("Cmax").value = Cmax.toString();
}
</script>
