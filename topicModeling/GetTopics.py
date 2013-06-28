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
from corpusManager import porter2

class GetTopics:

    

    #parse the files and do the preprocessing
    def prepareCorpus(self, files, threshold):
        print "preparing corpus"
        filesToWords = self.parseFiles(files)
        filesToWords = self.filterOutCommonWords(filesToWords, threshold)#FILTER OUT SUPER COMMON WORDS (appearing in more than X% of the documents)
        
        return filesToWords

    
    #given that LDA does not take into account super common words, we have to preprocess the document to remove them
    #the list is as follows, each entry in the list is a file, and each entry inside that list is a word
    def filterOutCommonWords(self, filesToWords, threshold):
        
        #due to teh way bug reports are formatted with mozilla, some words should ALWAYS be removed because they are in a ton of reports and
        #throw off the LDA stuff.
        #words to ALWAYS remove: 
        evilWordList = [] #if there are words we EXPLICITLY want removed, put them in here
        for eachEvilWord in evilWordList:
            filesToWords = self.removeWord(eachEvilWord, filesToWords)
        
        
        words = {}
        for eachFile in filesToWords:
            for eachWord in set(eachFile): #notice that we made it a set, horray!  its a set so that if a word happens more than once in a document, its score wont be skyrocketing
                if eachWord in words:
                    words[eachWord] += 1
                else:
                    words[eachWord] =1
        
        numOfFiles = len(filesToWords)
        
        keys = words.keys()
        thresholdValue = threshold * numOfFiles
        
        for eachKey in keys:
            if words[eachKey] >=  thresholdValue:
                filesToWords = self.removeWord(eachKey, filesToWords)
        
        return filesToWords
                
                
    
    #given a specific corpus, generate the topics.  the corpus comes in teh form of a list of files, where the each entry is as from readlines()
    def determineTopics(self, filesToWords, numTopics):
        #lda, corpus, dictionary, topics
        return self.computeLDA(filesToWords, numTopics)
    
        

    #this will take the a list of files, and go through, getting the individual words.  it will then put them into the 
    #a list.  the idea being when we are done, we can call the Gensim library 
    #note that the results are as follows  =    [ [X,Y,Z] [A,B,C] ] big list, with each file being its own list of words  (X,Y,Z are different lines)  
    def parseFiles(self, files):
        filesToWords = []
        for eachFile in files:
            words = []
            for eachLine in eachFile:
                wordsFromLine = self.splitLine(eachLine)
                for everyWord in wordsFromLine:
#                    if self.isLegitWord(everyWord): #this checks if the words is a real word and not just grammer and above a certain length 
#                    everyWord = self.stemWord(everyWord)
                    words.append(everyWord)
            filesToWords.append(words)    
        return filesToWords
    
    
    
    #DEPRICATED!   do all parsing and normalizing in the corpus manager package
#    #return true is word is more than 2 characters, not just grammer characters, or a stop word  else return false
#    def isLegitWord(self, word):
#        if len(word) > 2: #this ensures length greater than 2 and also not the empty string (by definition)
#            if re.match('[a-zA-Z]+[a-zA-Z]+[a-zA-Z]+', word) is not None: #this ensures at LEAST 3 english characters
#                if not word in self.stopWords: #stop words are the devil
#                    return True
#        
#        return False
            
    
    #given a line, split on teh white space and returns a list of words
    def splitLine(self, line):  
        temp = re.split("\s", line)
        while temp.count('')>0:
            temp.remove('')
        return temp
        
        
    

    def computeLDA(self, filesToWords, numOfTopics):
        dictionary = corpora.Dictionary(filesToWords)
        
        corpus = [dictionary.doc2bow(text) for text in filesToWords]
        
        #the LDA model takes as input a "bag of words : integer count" and returns topics
        lda = models.ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=numOfTopics)
        
        
        topics =  lda.show_topics(numOfTopics)
        
        print("done computing LDA")
        return lda, corpus, dictionary, topics
    

if __name__ == '__main__':
    print "nothing to do, call TopicController"

#    print "begin and middle " + str(scipy.ttest_rel(begin, middle))
#    print "begin and end " + str(scipy.ttest_rel(begin, end))
#    print "middle and end " + str(scipy.ttest_rel(middle, end))
    
