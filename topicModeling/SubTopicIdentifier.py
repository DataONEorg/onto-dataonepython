'''
Created on Apr 16, 2013

@author: nicholas
'''
import re
import os
from datetime import date, timedelta
from pylab import *
import matplotlib.pyplot as plot
import numpy as np
import scipy.stats as scipy
import math
import logging
from gensim import corpora, models, similarities
from time import time

from GetTopics import GetTopics
from TopicUtils import TopicUtils


class SubTopicIdentifier:

    def __init__(self):
        self.GetTopics = GetTopics()
        self.TopicUtils = TopicUtils()
        self.numTopics = 0
        
    def setNumTopics(self, num):
        self.numTopics = num
    
    def buildCorpus(self, path, threshold):
        files = []
        if os.path.isdir(path + "/" + os.listdir(path)[0]): #if you give it a dir of directories, it will turn EVERYTHING into a single corpus
            for eachDir in os.listdir(path):
                files += self.readFiles(path + "/" + eachDir)
        else: #if you give it a dir of files, it will turn that single dir into a corpus
            files = self.readFiles(path) #doing this takes a trivial amount of time
        files = self.GetTopics.prepareCorpus(files, threshold) #doing this can take up to a minute
        return files
    
    def calculateTopics(self, files):
        lda, corpus, dictionary, topics = self.GetTopics.determineTopics(files, self.numTopics) #doing this takes less than 10 seconds
        return lda, corpus, dictionary, topics
    

    
    #given a path, go through and read each file.  then add it to the files
    # so the returned array is like [ [X,Y,Z], [A,B,C] ]  where [X,Y,Z] is a single file and  X,Y,Z are individual
    #lines 
    def readFiles(self, path):
        files = []
        
        for eachFile in os.listdir(path):
            content = open(path+"/"+eachFile ).readlines()
            files.append(content)
        
        return files
            
    
    #given a list of topics, what is the internal divergence?  if i were to compare each topic against each other topic, and sum up 
    #their divergences what will the boxplot of that look like, and what is the average....
    def internalDivergence(self, topics):
        internalDivergences = []
        numTopics = len(topics)
        
        for i in range(0, len(topics)):
            for j in range(0, len(topics)):
                if j != i:
                    temp = self.TopicUtils.topicDivergence(topics[i], topics[j])
                    internalDivergences.append(temp)
        
        
        #its numTopics * numTopics -1 because each topic is compared with EVERY other topic other than itself.  
        score=  sum(internalDivergences) / (float(numTopics) * (numTopics-1) * numTopics )
        print score
        return score

        #if you want to boxplot uncomment the following llines
#        figure()
#        boxplot(internalDivergences, 0, '')
#        show()
                    

#ideally when you call this you pass in 5 parameters
#param 1: the absolute path to the directory containing the corpus documents
#param 2: the absolute path to the file where you want the output stored
#param 3: the threshold (e.g., 0.45 is 45% of documents) for words that will be ignored if they are too common 
#(ie if a words happens in X percentage of documents, we ignore it because it is too common to be valuable) 
#param 4: the number of topics you want
#param 5: the percentage of documents (e.g., 0.05) you want in each subdomain
if __name__ == '__main__':
    
    
    pathToCorpusDocs = sys.argv[1]
    pathToOutputFile = sys.argv[2]
    
    if len(sys.argv) > 3:
        threshold = float(sys.argv[3])
    else:
        threshold = 1.01 #this value means NOTHING will ever be remvoed because of frequency
        
    if len(sys.argv) > 4:
        numTopics = int(sys.argv[4])
    else:
        numTopics = 10 #we default to 10.  pick something meaningful becuase there is no garuantee that 10 is
        
    if len(sys.argv) > 5:
        similarityThreshold = int(sys.argv[5])
    else:
        similarityThreshold = 0.05 #we default to top 5%.  pick something meaningful becuase there is no garuantee that 0.05 is
    

    t = SubTopicIdentifier()
    t.setNumTopics(numTopics)
    files = t.buildCorpus(pathToCorpusDocs, threshold)
            
    lda, corpus, dictionary, topics = t.calculateTopics(files)
    topics = t.TopicUtils.topicListFixer(topics)
        
    score = t.internalDivergence(topics)
    #    print topics
            
    docSim = t.TopicUtils.getMostSimilarDocuments(corpus, dictionary, topics, lda, similarityThreshold)
            
    pathToOutputFile = sys.argv[2] + "_"+ str(numTopics)
            
    output = open(pathToOutputFile,'w')
    #the file is formatted so that each list (i.e., []) contains tuples, with the first number being the doc number and the second
    # being the score
        
    for each in docSim:
        output.write(str(each) + "\n")
    output.close()
            

    print "all finished"
    
    
    
    

    
