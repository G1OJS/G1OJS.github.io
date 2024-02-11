---
layout: default
mathjax: true
title: "Calculating Padding Capacitors"
permalink: /calculating-padding-capacitors/
---

# Calculating Padding Capacitors

Padding capacitors are capacitors added to a variable capacitor in order to change the available range of capacitance. 
<p></p>
Generally, we need to add *two* capacitors - one in parallel and another in series. The diagrams below show the two ways of doing this. 
<p></p>

| Configuration a)  | Configuration b) |
| ------------- | ------------- |
| ![Padding capacitors config 1]({{ site.baseurl }}/assets/img/Capacitor padding circuit 1.png "Configuration a)" )  | ![Padding capacitors config 2]({{ site.baseurl }}/assets/img/Capacitor padding circuit 2.png "Configuration b)" )  |

Each method requires different values of each of the padding capacitors C1 and C2, and has different implications for the current and voltage seen by each of the three capacitors making up the circuit, and hence implications for power handling and sensitity to temperature coefficients etc. 
<p></p>
## [📱 Calculator]({{ site.baseurl }}/Capacitor-Padding-Calc)
Click the heading above to get to a calculator that works out C1 and C2 based on your needed capacitance range for a given variable capacitor's range.
<p></p>
The rest of this page explains the maths used in the calculator.


## The Maths
It's easy to work out the range of capacitance achieved given the available range of the variable capacitor (e.g. 5pF to 250pf) and the values of the added capacitors, by using the well-known formulas for combining capacitors:

| Capacitors in Parallel  | Capacitors in Series|
| ------------- | ------------- |
| $$C=C1+C2$$ | $$\frac{1}{C}=\frac{1}{C1}+\frac{1}{C2}$$ |

So, for ecample, for configuration a) you'd first add C1 to the variable capacitance and then use the second formula to account for the effect of C2, and you'd do this twice; once for the variable's minimum capacitance and once for its maximum (or you could spreadsheet it and graph out intermediate values).

However, it's not so easy to work out what values you need for C1 and C2 in order to achieve a particular desired capacitance range. This requires a bit more as explained below.

### Configuration a)

Let's look first at the first configuration with the parallel capacitor connected directly across the variable one:

Let's call the capacitance range we need A (min) to B (max) and the capacitance range of the variable capacitor similarly $\alpha$ and $\beta$.

From the capacitor combination formulas above we can see that

$$\frac{1}{A}=\frac{1}{C1}+\frac{1}{C2+\alpha}$$

for the minimum capacitance, and 

$$\frac{1}{B}=\frac{1}{C1}+\frac{1}{C2+\beta}$$

for the maximum capacitance

Rearranging, 

$$\frac{1}{C1}=\frac{1}{A}-\frac{1}{C2+\alpha}=\frac{1}{B}-\frac{1}{C2+\beta}$$

If we multiply through with $(C2+\alpha)(C2+\beta)$, then expand those brackets and gather terms together, we find that the right hand equality (the one that doesn't involve C1) shows C2 in a quadratic equation:

$$(\frac{1}{A}-\frac{1}{B})C2^2$$
$$+(\frac{\alpha}{A}-\frac{\alpha}{B}+\frac{\beta}{A}-\frac{\beta}{B})C2$$
$$+\frac{\alpha\beta}{A}-\frac{\alpha\beta}{B}+\alpha-\beta=0$$

Using the standard notation for quadratic coefficients a,b,c we have a quadratic with:

$$a=\frac{1}{A}-\frac{1}{B}$$

$$b=a(\alpha+\beta)$$

$$c=a\alpha\beta+\alpha-\beta$$

... noting that, for convenience, the coefficient a appears in the expressions for coefficients b and c.

Then we can use the standard formula (using only the positive square root)

$$C2=\frac{-b+\sqrt{b^2-4ac}}{2a}$$

To get C2, and then C1 follows easily from 

$$\frac{1}{C1}=\frac{1}{B}+\frac{1}{C2+\beta}$$

### Configuration b)

For the other configuration, the maths is very similar and shows that this time C1 rather than C2 is quadratic with coefficients -

$$a=B-A+\alpha-\beta$$

$$b=(B-A)(\alpha+\beta)$$

$$c=\alpha\beta(B-A)$$

This time we use the *negative* result of the square root to find C1:

$$C1=\frac{-b-\sqrt{b^2-4ac}}{2a}$$

... and then get C2 from 

$$C2=B-\frac{1}{(\frac{1}{C1}+\frac{1}{\beta})}$$

