#! /usr/bin/env python

from porter2 import stem
import os


def stemWords(): 
    os.chdir(os.pardir+ "/data")
    existingData = "nostop_3.txt"
    newfile = open("nowStemmed_4.txt", "w+") 
    
    contents = open(existingData).readlines()

    for j in range(0, len(contents)):
        
        results = []     
        words = contents[j].split(" ")
        for i in range(0, len(words)):
            results.append(stem(words[i]))
        
        results = ' '.join(results)
            
        newfile.write(results)
        print results

if __name__ == "__main__":
    stemWords()