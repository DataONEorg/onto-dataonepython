'''
Created on Jul 9, 2013

@author: nicholas
'''

from stemWords import stemWords
from partOfSpeachTagger import PoSTagger
import os
import string
import sys
import re
from porter2 import stem as p2
from porter import stem as p1
from lovins import stem as lovins
from paicehusk import stem as paice

#takes a directory full of files that represent a corpus and turns them into a single file
def getCorpusIntoSingleFile(dir):
    output = open("wordfile.txt", "r")
    for eachFile in os.listdir(dir):
        current = open(dir + "/" + eachFile).readlines()
        output.writelines(current)
    output.close()

#removes the punctuation from the "single-file" corpus
def removePunct(dir):
    os.chdir(dir)
    copy = open("wordfile.txt", "r")
    newfile = open("nopunct_1.txt", "w+") 
    
    for line in copy:
        line_nopunct = line.translate(None, string.punctuation)

    
        print line_nopunct
        newfile.write(line_nopunct)

    copy.close()
    newfile.close()
    
#forces lowercase from the "single-file" corpus
def removeUpper(dir):
    os.chdir(dir)
    copy = open("nopunct_1.txt", "r")
    newfile = open("noupper_2.txt", "w+") 
    
    for line in copy:
        #line_nopunct = line.translate(None, string.punctuation)
    
        line_noUpper = line.lower()
        print line_noUpper
        newfile.write(line_noUpper)
    
    copy.close()
    newfile.close()

#removes the stopwords from the "single-file" corpus
def removeStop(dir):
    os.chdir(dir)
    copy = open("noupper_2.txt", "r")
    newfile = open("nostop_3.txt", "w+") 
    
    stopwords = open("stopwords_en.txt", "r")
    
    stoplist = []
    
    for line in stopwords:
        stoplist.append(line.strip())
    print stoplist
    
    for line in copy:
        word_list = line.strip().split()
        filtered_words = [w for w in word_list if not w in stoplist]
        #print filtered_words
        filtered_line = " ".join(filtered_words)
        # print line_nopunct
        newfile.write(filtered_line + "\n")
    
    copy.close()
    newfile.close()
    
#stems each word from the "single-file" corpus
def stemWords(dir, stemmer):
    os.chdir(dir)
    existingData = "nostop_3.txt"
    newfile = open("nowStemmed_4.txt", "w+") 
    
    contents = open(existingData).readlines()

    for j in range(0, len(contents)):
        
        results = []     
        words = contents[j].split(" ")
        for i in range(0, len(words)):
            results.append(stemmer(words[i]))
        
        results = ' '.join(results)
            
        newfile.write(results)


#this goes through and removes a word if it ONLY has numbers.  otherwise it leaves all other words alone
def removeNumbers(dir): 

    os.chdir(dir)
    
    existingData = "nowStemmed_4.txt"
    newfile = open("noAllNumbers_5.txt", "w+") 
    
    contents = open(existingData).readlines()

    for line in contents:
        word_list = line.strip().split()
        filtered_words = [w for w in word_list if re.match("[a-zA-Z]", w) is not None] #remove words that arent all english chars
        #print filtered_words
        filtered_line = " ".join(filtered_words)
    
        newfile.write(filtered_line + "\n")
        print filtered_line

    newfile.close()
    
#removes words which are not nouns, verbs, adverbs or adjectives from the "single-file" corpus
def PoSTagging(dir):
    os.chdir(dir)
    contents = open("noAllNumbers_5.txt").readlines()

    output = open("finishedCorpus_6.txt", "w+") 
    for eachLine in contents:
        temp = PoSTagger.performPoSTagging(eachLine)
        words =""
        for tuple in temp:
            words += tuple[0] + " "
        output.write(words + "\n")
    output.close()
    

#you MUST pass in 1 arguement (the absolute path to the directory containing ONLY corpus files) but can pass in a second, the stemmer you want
#if you do, the options are listed slightly below, but are "porter", "snowball", "lovins", or "paicehusk".  they must not be capitalized
#if not second arguement is passed in, it will default to use snowball, which is an advanced porter stemmer.
if __name__ == '__main__':
    dir = sys.argv[1] #this is the absolute path to the directory containing ONLY corpus files
    
#these are the stemmers that can be passed in.  it defaults to snowball (the advanced porter)
    if len(sys.argv) > 2:
        stemmer = sys.argv[2]
        if stemmer == "snowball":
            stemmer = p2
        if stemmer == "porter":
            stemmer = p1
        if stemmer == "lovins":
            stemmer = lovins
        if stemmer == "paicehusk":
            stemmer = paice
    else:
        stemmer = p2

getCorpusIntoSingleFile(dir)
removePunct(dir)
removeUpper(dir)
removeStop(dir)
stemWords(dir, stemmer)
removeNumbers(dir)
PoSTagging(dir)


print "Finished creating the corpus"