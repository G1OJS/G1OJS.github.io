---
layout: default
title: "Calculating Padding Capacitors"
permalink: /calculating-padding-capacitors/
---
{% include head.html %}

# Calculating Padding Capacitors

Padding capacitors are capacitors added to a variable capacitor in order to change the available range of capacitance. Generally, we will need to add *two* capacitors to steer the capacitance range to where we need it to be; we need to add one capacitor in parallel and another in series. There are two ways of doing this too; a) with the parallel capacitor connected directly across the variable & b) with that capacitor instead connected across the "output":
<p></p>

| Configuration a)  | Configuration b) |
| ------------- | ------------- |
| ![Padding capacitors config 1]({{ site.baseurl }}/assets/img/Capacitor padding circuit 1.png "Configuration a)" )  | ![Padding capacitors config 2]({{ site.baseurl }}/assets/img/Capacitor padding circuit 2.png "Configuration b)" )  |
| [Calculator]({{ site.baseurl }}/Capacitor-Padding-Calc-Cfg1)  | [Calculator]({{ site.baseurl }}/Capacitor-Padding-Calc-Cfg2) |

<p></p>
It's easy to work out the range of capacitance achieved given the available range of the variable capacitor (e.g. 5pF to 250pf) and the values of the added capacitors, by using the formula for combining capacitors:

For capacitors in parallel:

$$C=C1+C2$$

For capacitors in series:

$$\frac{1}{C}=\frac{1}{C1}+\frac{1}{C2}$$

So, for ecample, for configuration a) you'd first add C1 to the variable capacitance and then use the second formula to account for the effect of C2, and you'd do this twice; once for the variable's minimum capacitance and once for its maximum (or you could spreadsheet it and graph out intermediate values).

However, it's not so easy to work out what values you need for C1 and C2 in order to achieve a particular desired capacitance range. This requires a bit more maths.

⚠️ <span style="color:red">If you don't want the maths, skip straight to the bottom of this page to get to the calculators (or click the links under the diagrams above).</span> ⚠️ 

## The Maths!

### Configuration a)

Let's look first at the first configuration with the parallel capacitor connected directly across the variable one:

![Padding capacitors config 1]({{ site.baseurl }}/assets/img/Capacitor padding circuit 1.png)

Let's call the capacitance range we need A (min) to B (max) and the capacitance range of the variable capacitor similarly $\alpha$ and $\beta$.

From the capacitor combination formulas above we can see that

$$\frac{1}{A}=\frac{1}{C1}+\frac{1}{C2+\alpha}$$

for the minimum capacitance, and 

$$\frac{1}{B}=\frac{1}{C1}+\frac{1}{C2+\beta}$$

for the maximum capacitance

Rearranging, 

$$\frac{1}{C1}=\frac{1}{A}-\frac{1}{C2+\alpha}=\frac{1}{B}-\frac{1}{C2+\beta}$$

If we multiply through with $(C2+\alpha)(C2+\beta)$, then expand those brackets and gather terms together, we find that the right hand equality (the one that doesn't involve C1) shows C2 in a quadratic equation:

$$(\frac{1}{A}-\frac{1}{B})C2^2+(\frac{\alpha}{A}-\frac{\alpha}{B}+\frac{\beta}{A}-\frac{\beta}{B})C2+\frac{\alpha\beta}{A}-\frac{\alpha\beta}{B}+\alpha-\beta=0$$

Using the standard notation for quadratic coefficients a,b,c we have a quadratic with:

$$a=\frac{1}{A}-\frac{1}{B}$$

$$b=a(\alpha+\beta)$$

$$c=a\alpha\beta+\alpha-\beta$$

.. noting that, for convenience, the coefficient a appears in the expressions for coefficients b and c.

Then we can use the standard formula (using only the positive square root)

$$C2=\frac{-b+\sqrt{b^2-4ac}}{2a}$$

To get C2, and then C1 follows easily from 

$$\frac{1}{C1}=\frac{1}{B}+\frac{1}{C2+\beta}$$

### Configuration b)


![Padding capacitors config 1]({{ site.baseurl }}/assets/img/Capacitor padding circuit 1.png)

For the other configuration, the maths is very similar and shows that this time C1 rather than C2 is quadratic with coefficients -

$$a=B-A+\alpha-\beta$$

$$b=(B-A)(\alpha+\beta)$$

$$c=\alpha\beta(B-A)$$

This time we use the *negative* result of the square root to find C1:

$$C1=\frac{-b-\sqrt{b^2-4ac}}{2a}$$

... and then get C2 from 

$$C2=B-\frac{1}{(\frac{1}{C1}+\frac{1}{\beta})}$$

## Two simple calculators

I've used the maths above to make two simple JavaScript calculators which you can find [here]({{ site.baseurl }}/Capacitor-Padding-Calc-Cfg1) and [here]({{ site.baseurl }}/Capacitor-Padding-Calc-Cfg2) for configurations a) and b) respectively.

## Planned Changes
Embed calculators on this page?
Construct a combined calculator that allows comparing config a) and config b) side by side
