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
import math



if __name__ == '__main__':
    
    results = "/home/nicholas/research/Experiments/DataONEjava/results"
    
    files = os.listdir(results)
    
    for eachFile in files:
        if os.path.isfile(results+"/"+eachFile):
            contents = open(results +"/"+eachFile).readlines()
            for eachLine in contents:
                score = float(re.split("=", eachLine)[1].strip())
                if score != 0.0 and not math.isnan(score):
                    print(eachFile)
                    move = subprocess.Popen("mv " + results+"/"+eachFile + " " +results+"/nonZeroResults/", shell=True)
                    move.wait()
                    break
            