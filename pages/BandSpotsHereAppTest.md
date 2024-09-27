---
layout: default
calculator_style: true
title: "Capacitor Padding Calculator"
permalink: /BandSpotsHereAppTest/
---
# Introduction
blah

<html>
<style type="text/css">
  
g><br>
        <label>C1</label><input type="text" id="CFG1_C1Used" onchange="EvaluatePadding()" />
        <label>C2</label><input type="text" id="CFG1_C2Used" onchange="EvaluatePadding()" />
        <!-- inline CSS bacause Jekyll adds margin and padding to img that seems not to be overridden by <style> section -->
        <img style="padding: 0px; margin: 0px; margin-top: 5px; width: 100%;" src="https://g1ojs.github.io/assets/img/Capacitor%20padding%20circuit%201.png"/>
    </div>

    <div class="right1">
        <strong>Capacitance range at C<sub>out</sub>:</strong><br>
        <label>C<sub>min</sub>:</label><output id="CFG1_Cmin"></output><br>
        <label>C<sub>max</sub>:</label><output id="CFG1_Cmax"></output><br>
        <strong>Max voltage, % of voltage at C<sub>out</sub>:</strong><br>
        <label>CV:</label><output id="CFG1_CVV_Cmax"></output>-<output id="CFG1_CVV_Cmin"></output>(C<sub>min</sub>)<br>
        <label>C1:</label><output id="CFG1_C1V_Cmin"></output>-<output id="CFG1_C1V_Cmax"></output>(C<sub>max</sub>)<br>
        <label>C2:</label><output id="CFG1_C2V_Cmax"></output>-<output id="CFG1_C2V_Cmin"></output>(C<sub>min</sub>)
    </div>

    <div class="left2">
      <strong>Configuration b)</strong><br>
      <label>C1</label><input type="text" id="CFG2_C1Used" onchange="EvaluatePadding()" />
      <label>C2</label><input type="text" id="CFG2_C2Used" onchange="EvaluatePadding()" />
      <!-- inline CSS bacause Jekyll adds margin and padding to img that seems not to be overridden by <style> section -->
      <img style="padding: 0px; margin: 0px; margin-top: 5px; width: 100%;" src="https://g1ojs.github.io/assets/img/Capacitor%20padding%20circuit%202.png"/>
    </div>

    <div class="right2">
      <strong>Capacitance range at C<sub>out</sub>:</strong><br>
      <label>C<sub>min</sub>:</label><output id="CFG2_Cmin"></output><br>
      <label>C<sub>max</sub>:</label><output id="CFG2_Cmax"></output><br>
      <strong>Max voltage, % of voltage at C<sub>out</sub>:</strong><br>
      <label>CV:</label><output id="CFG2_CVV_Cmax"></output>-<output id="CFG2_CVV_Cmin"></output>(C<sub>min</sub>)<br>
      <label>C1:</label><output id="CFG2_C1V_Cmin"></output>-<output id="CFG2_C1V_Cmax"></output>(C<sub>max</sub>)<br>
      <label>C2:</label><output>100%</output> (always)
    </div>

</div>
    
</body>

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
 //   document.getElementById("CFG1_C1Req").value = CFG1_C1.toString();
//    document.getElementById("CFG1_C2Req").value = CFG1_C2.toString();
    document.getElementById("CFG1_C1Used").value = Math.max(0,Math.round(CFG1_C1)).toString();
    document.getElementById("CFG1_C2Used").value = Math.max(0,Math.round(CFG1_C2)).toString();

// Write C1 and C2 for config a)
//    document.getElementById("CFG2_C1Req").value = CFG2_C1.toString();
//    document.getElementById("CFG2_C2Req").value = CFG2_C2.toString();
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
    document.getElementById("CFG1_Cmin").value = Math.round(CFG1_Cmin).toString();
    document.getElementById("CFG1_Cmax").value = Math.round(CFG1_Cmax).toString();

//Min and Max capacitance for config b)
    CFG2_Cmin=CFG2_C2Used+1/(1/CFG2_C1Used+1/Alpha);
    CFG2_Cmax=CFG2_C2Used+1/(1/CFG2_C1Used+1/Beta);
    document.getElementById("CFG2_Cmin").value = Math.round(CFG2_Cmin).toString();
    document.getElementById("CFG2_Cmax").value = Math.round(CFG2_Cmax).toString();

// Max voltages across capacitors
    CFG1_C1V_Cmin=1/(1+CFG1_C1Used/(CFG1_C2Used+Alpha))
    CFG1_C1V_Cmax=1/(1+CFG1_C1Used/(CFG1_C2Used+Beta))
    CFG1_CVV_Cmin=1/(1+(CFG1_C2Used+Alpha)/CFG1_C1Used)
    CFG1_CVV_Cmax=1/(1+(CFG1_C2Used+Beta)/CFG1_C1Used)
    
    CFG2_C1V_Cmin=1/(1+(CFG2_C1Used/Alpha))
    CFG2_C1V_Cmax=1/(1+(CFG2_C1Used/Beta))
    CFG2_CVV_Cmin=1/(1+(Alpha/CFG2_C1Used))
    CFG2_CVV_Cmax=1/(1+(Beta/CFG2_C1Used))
   
    document.getElementById("CFG1_C1V_Cmin").value = CFG1_C1V_Cmin.toLocaleString(undefined,{style: 'percent', minimumFractionDigits:0});    
    document.getElementById("CFG1_C1V_Cmax").value = CFG1_C1V_Cmax.toLocaleString(undefined,{style: 'percent', minimumFractionDigits:0});
    document.getElementById("CFG1_CVV_Cmin").value = CFG1_CVV_Cmin.toLocaleString(undefined,{style: 'percent', minimumFractionDigits:0});
    document.getElementById("CFG1_CVV_Cmax").value = CFG1_CVV_Cmax.toLocaleString(undefined,{style: 'percent', minimumFractionDigits:0});
    document.getElementById("CFG1_C2V_Cmin").value = CFG1_CVV_Cmin.toLocaleString(undefined,{style: 'percent', minimumFractionDigits:0});
    document.getElementById("CFG1_C2V_Cmax").value = CFG1_CVV_Cmax.toLocaleString(undefined,{style: 'percent', minimumFractionDigits:0});
    
    document.getElementById("CFG2_C1V_Cmin").value = CFG2_C1V_Cmin.toLocaleString(undefined,{style: 'percent', minimumFractionDigits:0});
    document.getElementById("CFG2_C1V_Cmax").value = CFG2_C1V_Cmax.toLocaleString(undefined,{style: 'percent', minimumFractionDigits:0});
    document.getElementById("CFG2_CVV_Cmin").value = CFG2_CVV_Cmin.toLocaleString(undefined,{style: 'percent', minimumFractionDigits:0});    
    document.getElementById("CFG2_CVV_Cmax").value = CFG2_CVV_Cmax.toLocaleString(undefined,{style: 'percent', minimumFractionDigits:0});
    
 
}

</script>
</html>
