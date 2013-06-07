'''
Created on May 30, 2013

@author: nicholas
'''


import re
import os
import urllib2
import sys
import unittest
from nltk.corpus import wordnet as wn


#note that THIS SCRIPT ASSUMES you have NLTK installed.  if you do not, the guide for doing so can be found at 
# http://nltk.org/install.html
#also, for ease of reference, here is a simple legend for PoS tags

#@param word the word we want to find a synonym of
def synonymGenerator(word):
    wn.synsets(word)
    print wn.synsets(word)

#class MyTest(unittest.TestCase):
#    def test(self):
#       

if __name__ == '__main__':
    synonymGenerator("dog")
    synonymGenerator("throat")
    synonymGenerator("water")
    synonymGenerator("beaver")
    synonymGenerator("chair")
    synonymGenerator("canine")
    #word net's results are pretty much garbage.

    
        