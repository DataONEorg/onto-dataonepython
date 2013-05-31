'''
Created on May 30, 2013

@author: nicholas
'''


import re
import os
import urllib2
import sys




#given a list with URLs, go through and download each one, and save it
def getOntolgoies(list):
    
    for url in list:
        response = urllib2.urlopen(url).read()
        
        #we cannot use teh URL as a file name because of slashes, so just get the actual name from the end of the URL
        #  %%%%%NOTE%%%%%   this method of gathering the name will not work if the URL doesnt contain a unique name at the end of its path
        name = re.split("/", url)
        name = name[len(name)-1]
        
        output = open(name, "w+")
        output.write(response)
        output.close()




if __name__ == '__main__':
    
    pathToURLFile = sys.argv[1] #this should be a file with a series of URLs followed by a "\n"
    pathToOutputLocation = sys.argv[2] #this should be a directory where you want the ontology files stored

    
    ontologies = open(pathToURLFile).readlines()
    os.chdir(pathToOutputLocation)
    getOntolgoies(ontologies)
    
        