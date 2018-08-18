#!/usr/bin/env python
# -*- coding:utf-8 -*- 

import codecs
import sys
import os

#print and store universal directory tree structure.

of = codecs.open('file_structure_github.txt', "w", encoding="utf-8")

root = r"C:\Users\User\Documents\RText"
path = os.path.join(root, "filename")

counter = 0

for currentDirect, subDirect, files in os.walk(root):
    for name in files:
        print(os.path.join(currentDirect, name))
        of.write(os.path.join(currentDirect, name) + "\n")
        counter+1
        if(counter==10):
            break
			
"""
import os 
filesList = os.listdir("C:\Users\User\Documents\")
for f in filesList:
	print f
"""

"""
import os 
for (dirpath, dirnames, filenames) in os.walk("C:\Users\User\Documents\"):
	print dirnames
	break
"""

"""
import glob
dirList = glob.glob("C:\Users\User\Documents\")
for d in dirList:
	print d
"""
