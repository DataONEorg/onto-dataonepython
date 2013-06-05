'''
Created on May 30, 2013

@author: nicholas
'''


import re
import os
import urllib2
import sys
import string
from corpusFetcher import porter2


#load up an ontology file as text and stem each name.  Do this by giving it a dir containing all the ontologies.
#it will load them up one at a time, and then go through them
def getOntologies(dirPath):
    if os.path.isfile(dirPath):
        print "this isnt a dir path, its a file path....that doesnt work...im leaving"
        sys.exit(0)
    
    files = os.listdir(dirPath)
    
    for each in files:
        parseOntology(dirPath + "/" + each)
    
#parse a single ontology.  make each class an entry within a dictionary and then stem ALL instances of it through the entire file
#note that all class names start with a number sign char '#' in front of them, so just look for those
#however, we have to skip past the RDF stuff first....  so...skip everything until we get to the "<!-- Ontology Information -->" string
def parseOntology(filePath):
    words = {}
    outputFile = []
    contents = open(filePath).readlines()
    
    counter = 0
    while counter < len(contents):
        outputFile.append(contents[counter])
        if "<!-- Ontology Information -->" in contents[counter]:
            break
        else:     
            counter +=1
    
    #now we can parse the file
    for i in range(counter, len(contents)):
        if "#" in contents[i]:
            className = re.split("#", contents[i])[1]
            className = className.translate(None, string.punctuation)
            className = className.rstrip() #this removes any newlines that are there
            
            if className in words: #we have this key already
                outputFile.append( contents[i].replace(className, words[className]) ) #replace class name with already found stemmed version
            else:
                stemmedName = porter2.stem(className) #get stemmed word
                words[className] = stemmedName #put it in dictionary
                outputFile.append( contents[i].replace(className, words[className]) ) #replace class name with stemmed version
        else:
            outputFile.append(contents[i])
        
            
    out = open(filePath, "w+")
    out.writelines(outputFile)
    out.close()
    

if __name__ == '__main__':
    dirPath = sys.argv[1]
    getOntologies(dirPath)
    print "finished!"
    
        