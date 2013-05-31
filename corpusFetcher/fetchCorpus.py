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


#this is a basic control loop for gathering the corpus, and editing it to remove punctuation, case sensitivity, stop words, and then stem
get_metadata()
removePunct()
removeUpper()
removeStop()
stemWords()
removeNumbers()


