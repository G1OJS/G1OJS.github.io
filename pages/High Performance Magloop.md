---
layout: default
title: "High Performance Magloop"
permalink: /calculating-padding-capacitors/
---

# A High Performance QRO Magloop without a Vacuum Capacitor
I've been experimenting with "magnetic" loop antennas for a few years now and running tests using WSPR (with hundreds of spots & statistical analysis) to drive out the losses from my antenna.
I know from the "Ham Radio Web" that Vaccuum Variable Capacitors (VVC) are the gold standard for low loss capacitors in magloops, but I've achieved good results with air spaced variables and wanted to see how far I could push this without "giving in" and buying a VVC.
Lessons learned with air spaced capacitors:
 - Don't rely on the wiper contact to connect to the moving plates. The wiper is a source of loss resistance - enough to make it melt & fail with just a bit of power! Instead, clamp a flexible wire to the spindle or solder one to the final moving plate.
 - Use copper or aluminium for all connections - avoid steel and galvanized pieces (again, sources of loss resistance).
 - It's not always easy to notice capacitor arcing from a remote position, especially with SSB operation.
 - However, with good connections, limited trials tell me that my air spaced capacitor is comparable with a VVC (which I finally gave in to buy and test) in terms of the impact on the gain of the antenna.

The remaining problem with air spaced capacitors is power handling;my air spaced capacitor will arc at about 20W on 80m and about 40W on 40m. 
Also, VVCs are expensive and need more torque to turn than a typical air spaced capacitor, which means more mechanical design effort for the controller.
So I have been wondering - is there a way to use an air spaced capacitor in conjunction with fixed capacitors to improve the power handling?

The answer is "yes" - but it depends how 

 - 
