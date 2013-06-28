#! /usr/bin/env python
import os
import urllib2
from xml.dom.minidom import parse, parseString, getDOMImplementation
from urlparse import urlsplit, urljoin, urlunsplit
import codecs

import get_metadata as get_metadata
import removePunct as removePunct
import removeUpper as removeUpper
import removeStop as removeStop
from stemWords import stemWords
from removeNumbers import removeNumbers
from partOfSpeachTagger import PoSTagger


#this is a basic control loop for gathering the corpus, and editing it to remove punctuation, case sensitivity, stop words, and then stem
get_metadata()
removePunct()
removeUpper()
removeStop()
stemWords()
removeNumbers()

os.chdir(os.pardir+ "/data")
contents = open("noAllNumbers_5.txt").readlines()

output = open("finishedCorpus_6.txt", "w+") 
for eachLine in contents:
    temp = PoSTagger.performPoSTagging(eachLine)
    words =""
    for tuple in temp:
        words += tuple[0] + " "
    output.write(words + "\n")
    
output.close()
print "Finished creating the corpus"


