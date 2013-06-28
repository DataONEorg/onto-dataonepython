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



class TopicUtils:

    def __init__(self):
        self.GetTopics = GetTopics()
        
    
    #this method will take the topics from an LDA run and return for each topic, the top X% similar documents from the corpus
    #note that its possible that a document is similar to multiple topics and thus appears more than once 
    #@return list: a list of documents to topics.  where each entry in the list (i.e., i in list[i]) is a topic number and the contents are the top X most similar documents
    #@param corpus: the corpus made when we performed the topic modeling
    #@param dictionary: the dictionary that is created when we performed the topic modeling
    #@param topics :  the actual topic dictionaries (in a list form)
    #@param lda: the lda space we created when we performed topic modeling
    #@param similarityThreshold: this is the threshold for how close the documents must be to the topic to match
    def getMostSimilarDocuments(self,corpus,  dictionary, topics, lda, similarityThreshold):
        docSimilarity=[]
        
        lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=len(topics))
        
        
        for eachTopic in topics:
            print "string to find subdomain for topic " +str(eachTopic)
            queryDocSim = self.computeSimilarity(corpus, dictionary, lsi, eachTopic)
                        
            #this sorts the list in decreasing order by the score and not the document
            queryDocSim = sorted(enumerate(queryDocSim), key=lambda item: -item[1]) 
                
            topX = int(len(queryDocSim)*similarityThreshold)
            if topX < 1:
                topX=1 #we have to return something, so if you incorrectly picked a threshold, just give them the singlemost relevent doc
            
            docSimilarity.append( queryDocSim[ 0: topX ] )
            
        return docSimilarity
        
        
        
    #this method will determine for a specific topic which documents are the similarity.  note that it calls various helper functions
    #to transform the topic into a query, and then to returns the similarity of ALL documents in sorted order
    #@param corpus: the corpus made when we performed the topic modeling
    #@param dictionary: the dictionary that is created when we performed the topic modeling
    #@param lda: the lda space we created when we performed topic modeling
    #@param topics :  an actual topic dictionary (just a single one)
    def computeSimilarity(self,corpus,  dictionary, lsi, topic):
        bagOfWords = self.createQuery(dictionary, topic)
        bagOfWords = lsi[bagOfWords]
        index = similarities.MatrixSimilarity(lsi[corpus])
        queryLDA = index[bagOfWords]
        return queryLDA
    
    
    #follows gensims rules for creating queries    
    #@param dictionary: the dictionary that is created when we performed the topic modeling
    #@param lda: the lda space we created when we performed topic modeling
    def createQuery(self, dictionary, topic):
        keys = topic.keys()
        return dictionary.doc2bow(keys)
        
    
    
    
        
        
        
        
    
    #takes a list of topics (as strings) and returns a list of topics (as dictionaries)
    def topicListFixer(self, topic):
        returnableList = []
        
        for eachTopic in topic:
            returnableList.append(self.topicStringIntoTopicDictionary(eachTopic))
            
        return returnableList
    
    
    #takes a topic as its produced by gensim (as a string) and turns it into a dictionary with keys and values
    #and example string is as follows
    #0.022*cooki + 0.017*bug + 0.013*mozilla + 0.010*mozilla/5.0 + 0.008*window + 0.007*build + 0.007*linux
    def topicStringIntoTopicDictionary(self, topic):
        topicDict = {}
        
        pairs = re.split("\+", topic)
        
        for eachPair in pairs:
            value = float(re.split("\*", eachPair)[0].strip())
            key = re.split("\*", eachPair)[1].strip()
            topicDict[key] = value
        
        return topicDict
        
    
    
    
    
    #we are using F-divergence with total variation distance.
    #F-divergence F(dP/dQ) * dQ
    #total variation distance F(x) = | x-1 |
    #if the element doesnt exist in the other topic, we count its difference as a 1 (which is the max distance bewteen any two probabilities in this case)
    #note that the topics are given as dictionaries
    def topicDivergence(self, topic1, topic2):
         
        divergence = 0
        #since we use topic1.keys as our checker, if topic2 has keys topic1 doesnt, we have to account for them before we start
        #thus, this measure will add 1 for each key more that topic2 has that topic1 doesnt.  its our starting divergence
        if len(topic1.keys()) < len(topic2.keys()):
            divergence = len(topic2.keys()) - len(topic1.keys())
        
        keys1 = topic1.keys()
        
        for eachKey in keys1:
            if eachKey in topic2: 
                divergence += math.fabs((topic1[eachKey] / topic2[eachKey]) - 1) * topic2[eachKey]
            else: #if its not there...just add 1, its the max
                divergence += 1
        
        return divergence
    

    #given two sets of topics, find the best matching for each topic.  the two topics should be lists of dictionaries already
    #NOTE: if the topicLists have different quantities of topics, this will not work
    def findBestTopicsMatches(self, topicList1, topicList2):
        matrixOfMatches = []
        for i in range(0, len(topicList1)):
            matrixOfMatches.append([])
            for j in range(0, len(topicList2)):
                matrixOfMatches[i].append([])
        
        #now matrix of matches is a 10 x 10 matrix that can keep scores.  the first index is list 1 and the second is list 2.  the value is their divergence
        for i in range(0, len(topicList1)):
            for j in range(0, len(topicList2)):
                matrixOfMatches[i][j] = self.topicDivergence(topicList1[i], topicList2[j])
        
        matrixOfMatches = np.array(matrixOfMatches) #this makes it so numpy will let me access columns
        print "done populating matrix scores"
        
        topic1Desires = [ [] ] * len(topicList1)
        topic2Desires = [ [] ] * len(topicList2)
        
        #now that we have the matrix, lets get the desires for each topic in its own list
        for i in range(0, len(matrixOfMatches)):
            topic1Desires[i] = list(matrixOfMatches[i])
            topic2Desires[i] = list(matrixOfMatches[:,i])
        
        topic1Desires = [ self.turnScoresIntoRanks(x) for x in topic1Desires ]
        topic2Desires = [ self.turnScoresIntoRanks(x) for x in topic2Desires ]
        
        for i in range(0, len(topic1Desires)):
            topic1Desires[i] = [x+len(topic1Desires) for x in topic1Desires[i]]
        
        #so at this point, topic1Desires point to numbers between 10-19 and topic2Desires point to numbers between 0-9
        #this is to make it work with the downloaded library.  so officially the topics in the second list have indexes that are off by 10
               
        
        results = self.maxWeightMatching(topic1Desires, topic2Desires)
        print "done pairing"
        
        
        print results
        return results 
            
    
    
    def maxWeightMatching(self, firstList, secondList):
        NO_MATCH = "NONE"
        
        matches = [NO_MATCH] * (len(firstList) + len(secondList))
        allLists = firstList + secondList
        
        
        while matches.count(NO_MATCH) > 0: #something is not matched
            
            #try to match everything in the first list
            
            for i in range(0, len(firstList)):
                if matches[i] != NO_MATCH:  #this one is matched, move on
                    continue
                
                seekingMatch = True
                while seekingMatch:
                    currentDesire = firstList[i][0]
                    
                    #3 possibilities, it has no match, it has a match but this is better, it has a match and this is worse
                    
                    #CASE 1: its desire has no match
                    if matches[currentDesire] == NO_MATCH:
                        matches[i] = currentDesire
                        matches[currentDesire] = i
                        seekingMatch = False
                    
                    #CASE 2: it has a match, but this is better
                    elif allLists[currentDesire].index(matches[currentDesire]) > allLists[currentDesire].index(i):
                        temp = matches[currentDesire]
                        matches[temp] = NO_MATCH
                        
                        matches[i] = currentDesire
                        matches[currentDesire] = i
                        seekingMatch = False
                    
                    #CASE 3: it has a match and this match is worse
                    else:
                        del firstList[i][0] #if we cant have this, just throw it away
                
                #end of while seeking match
            #end of for i to len firstList
        #end of while self.NO_match > 0
        return matches[:len(firstList)] #this gives us just the first set of matches.  otherwise we see that X matches to Y and that Y matches to X...we dont need both
        
        


    #given a set of topic desires (i.e., a list of scores) turn those scores into  ranks and then sort them.
    #for example, this list [.5, .9, .7, .2] would become [3, 0, 2, 1] because it first wants the third topic, then the 0th, then the second and finally teh first
    def turnScoresIntoRanks(self, topicDesires):     
        temp = list(topicDesires)
        temp.sort()
        
        results = []
        for i in range(0, len(temp)):
            results.append( topicDesires.index(temp[i]) )
            
        return results      
        
        
        
    
    

    
