#! /usr/bin/env python

import os
import codecs
import string

os.chdir(os.pardir+ "/data")
copy = open("nopunct_1.txt", "r")
newfile = open("noupper_2.txt", "w+") 

for line in copy:
    #line_nopunct = line.translate(None, string.punctuation)

    line_noUpper = line.lower()
    print line_noUpper
    newfile.write(line_noUpper)

copy.close()
newfile.close()

