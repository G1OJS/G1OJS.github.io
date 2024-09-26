---
layout: default
title: "4nec2"
permalink: /4nec2/
---

I'm going to collect some useful things I've been doing with 4nec2 on this page. There's not much here at the moment; I'm just starting this page off with a Python script
I wrote to harmonise the ground definition in all my nec input files, which has varied a bit as I've developed expertise in writing nec input files.
This script simply loops through all .nec files under the specified path (including those in subfolders and makes a copy of each file, except if a line in 
the file starts with GN, it is ignored and replaced by the string specified in the variable "newground" the script

### [💻 Python Script to make all 4nec2 files in a folder have the same ground](https://github.com/G1OJS/4nec2-utilities/blob/main/scripts/Harmonise%20Grounds.py)
