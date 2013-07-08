'''
Created on May 30, 2013

@author: nicholas
'''


import re
import os
import urllib2
import sys
from corpusManager import porter2


def mergeValues(inputPath, outputPath):
    contents = open(inputPath).readlines()
    outputFile = open(outputPath, "w+")
    
    thesaurusDict = {}
    
    for eachLine in contents:  #remember these files are formatted as follows: head \t PoS \t listOfSynonyms (where each synonym is deliniated by a comma)
        temp = re.split("\t", eachLine)
        head = temp[0].strip()
        PoS = temp[1].strip()
        
        synonyms = ""
        listOfSyn = [x.strip() for x in re.split(",", temp[2])]
        
        if head in thesaurusDict:
            currentList = thesaurusDict[head][1] #the one gets of the list of synonyms and not the PoS
            union = set(currentList) | set(listOfSyn)
            thesaurusDict[head] = (thesaurusDict[head][0], list(union))  #reinsert the same PoS but with a new and updated synonym list
        else:  
            thesaurusDict[head] = (PoS, listOfSyn)
    
    for key in thesaurusDict.keys():
        synonyms = thesaurusDict[key][1]
        oneLine = key + "\t" + thesaurusDict[key][0] + "\t"
        
        for i in range(0, len(synonyms)): #remake the sentence with the synonyms and commas and what not
            oneLine += synonyms[i]  
            if i != len(synonyms)-1:  #this needs to be here because we cant have a dangling comma after the last word
                oneLine += ","
        
        outputFile.write(oneLine + "\n")
        
        

    outputFile.close()

if __name__ == '__main__':
    if len(sys.argv) > 1: #ie you passed a path to the synonym file
        inputPath = sys.argv[1]
        outputPath = sys.argv[2]
    else:
        inputPath  ="/home/nicholas/research/Experiments/DataONEjava/synonyms/GenEnglishSynCompendiumStemmed.txt"
        outputPath = "/home/nicholas/research/Experiments/DataONEjava/synonyms/mergedSynCompendiumStemmed.txt"
    
    mergeValues(inputPath, outputPath)
    print "all done"
    
        