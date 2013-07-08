'''
Created on May 30, 2013

@author: nicholas
'''


import re
import os
import urllib2
import sys
from corpusManager import porter2


def stemThesaurus(inputPath, outputPath):
    contents = open(inputPath).readlines()
    outputFile = open(outputPath, "w+")
    
    for eachLine in contents:  #remember these files are formatted as follows: head \t PoS \t listOfSynonyms (where each synonym is deliniated by a comma)
        temp = re.split("\t", eachLine)
        head = porter2.stem(temp[0].strip())
        PoS = temp[1]
        
        synonyms = ""
        listOfSyn = re.split(",", temp[2])
        for i in range(0, len(listOfSyn)):
            synonyms += porter2.stem(listOfSyn[i].strip())    
            if i != len(listOfSyn)-1:  #this needs to be here because we cant have a dangling comma after the last word
                synonyms += ","
        
        oneLine = head + "\t" + PoS + "\t" + synonyms +"\n"
        outputFile.write(oneLine)

    outputFile.close()

if __name__ == '__main__':
    if len(sys.argv) > 1: #ie you passed a path to the synonym file
        inputPath = sys.argv[1]
        outputPath = sys.argv[2]
    else:
        inputPath  ="/home/nicholas/research/Experiments/DataONEjava/synonyms/GenEnglishSynCompendium.txt"
        outputPath = "/home/nicholas/research/Experiments/DataONEjava/synonyms/GenEnglishSynCompendiumStemmed.txt"
    
    stemThesaurus(inputPath, outputPath)
    
        