---
layout: default
title: "Calculating Padding Capacitors"
permalink: /calculating-padding-capacitors/
---
{% include head.html %}

**Calculating Padding Capacitors**

Padding capacitors are capacitors added to a variable capacitor in order to change the available range of capacitance. Generally, we will need to add *two* capacitors to steer the capacitance range to where we need it to be; we need to add one capacitor in parallel and another in series. There are two ways of doing this too; a) with the parallel capacitor connected directly across the variable & b) with that capacitor instead connected across the "output".

![Padding capacitors config 1]({{ site.baseurl }}/assets/img/Capacitor padding circuit 1.png)

![Padding capacitors config 2]({{ site.baseurl }}/assets/img/Capacitor padding circuit 2.png)

It's easy to work out the range of capacitance achieved given the available range of the variable capacitor (e.g. 5pF to 250pf) and the values of the added capacitors, by using the formula for adding capacitors:

For capacitors in parallel:

$$C_{out}=C_1+C_2$$

For capacitors in series:

$$\frac{1}{C_{out}}=\frac{1}{C_1}+\frac{1}{C_2}$$

However, it's not so easy to work out what padding capacitors are needed to achieve a particular desired capacitance range. This requires a bit more maths.

**The Maths!**


