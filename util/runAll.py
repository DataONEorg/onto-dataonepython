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



if __name__ == '__main__':
    
    ontologiesPath = "/home/nicholas/research/Experiments/DataONEjava/stemmedOntologies/" 
    javaFilesPath = "/home/nicholas/research/Experiments/DataONEjava"
    corpusPath = "/home/nicholas/research/Experiments/DataONEjava/corpus.owl"
    owlJar = "/home/nicholas/research/Experiments/DataONEjava/owlapi-distribution-3.4.4-bin.jar" #you need to include the CWD or cobertura will crash
    
    files = os.listdir("/home/nicholas/research/Experiments/DataONEjava/stemmedOntologies")
    
    os.chdir(javaFilesPath)
    
    for eachFile in files:
        print "starting " + str(eachFile)
        if ".owl" in eachFile:#we only want the ontology files
            test = subprocess.Popen("java -classpath  " + owlJar + ":./src owlOntologies.CoverageAnalyzer " + corpusPath + 
                                    " " + ontologiesPath + eachFile  , shell=True)
            test.wait()
    
    