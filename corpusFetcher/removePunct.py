#! /usr/bin/env python

import os
import codecs
import string

os.chdir(os.pardir+ "/data")
copy = open("wordfile.txt", "r")
newfile = open("nopunct_1.txt", "w+") 

for line in copy:
    line_nopunct = line.translate(None, string.punctuation)

    
    print line_nopunct
    newfile.write(line_nopunct)

copy.close()
newfile.close()

