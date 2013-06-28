'''
Created on May 30, 2013

@author: nicholas
'''


import re
import os
import urllib2
import sys
from corpusFetcher import porter2
import subprocess
from pylab import *



if __name__ == '__main__':
    
    ontologiesPath = "/home/nicholas/research/Experiments/DataONEjava/stemmedBioportalOntologies/" 
    
    #class      :     "<owl:Class rdf:about"
    #subClass   :     "<rdfs:subClassOf rdf"
    #equivalence:     "<owl:equivalentClass rdf"
    
    numClass=[]
    numSubClass=[]
    numEquivalence=[]
    
    cls = "<owl:Class rdf:about"
    scls ="<rdfs:subClassOf rdf"
    equiv="<owl:equivalentClass rdf"
    
    files = os.listdir(ontologiesPath)
    for i in range(0, len(files)):
        numClass.append(0)
        numSubClass.append(0)
        numEquivalence.append(0)
        
        contents = open(ontologiesPath+"/"+files[i]).readlines()
        for eachLine in contents:
            if cls in eachLine:
                numClass[i] +=1
            elif scls in eachLine:
                numSubClass[i] +=1
            elif equiv in eachLine:
                numEquivalence[i] +=1
        
    print "number of classes is " + str(sum(numClass))
    print "number of subClasses is " + str(sum(numSubClass))
    print "number of equiv is " + str(sum(numEquivalence))
    print "total number of ontologies is " + str(len(files))
    
    data = [numClass, numSubClass, numEquivalence]
    boxplot(data,0,'')
    xticks([1.0,2.0,3.0],["classes per", "subClasses per", "equivalences per"])
    show()
    