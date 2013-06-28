#! /usr/bin/env python

import os
import codecs
import string

os.chdir(os.pardir+ "/data")
copy = open("noupper_2.txt", "r")
newfile = open("nostop_3.txt", "w+") 

stopwords = open("stopwords_en.txt", "r")

stoplist = []

for line in stopwords:
    stoplist.append(line.strip())
print stoplist



for line in copy:
    
    word_list = line.strip().split()
    filtered_words = [w for w in word_list if not w in stoplist]
    #print filtered_words
    filtered_line = " ".join(filtered_words)
    # print line_nopunct
    newfile.write(filtered_line + "\n")

copy.close()
newfile.close()

