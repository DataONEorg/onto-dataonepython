#! /usr/bin/env python


import re
import os
import unittest

#this goes through and removes a word if it ONLY has numbers.  otherwise it leaves all other words alone
def removeNumbers(): 

    os.chdir(os.pardir+ "/data")
    
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

#since the main method reads from script, this replicates its code and can be used to test strings as input
def testMethod(contents):
    results = []
    for line in contents:
        word_list = line.strip().split()
        filtered_words = [w for w in word_list if re.match("[a-zA-Z]", w) is not None]
        #print filtered_words
        filtered_line = " ".join(filtered_words)
    
        results.append(filtered_line)
    
    return results

class MyTest(unittest.TestCase):
    
    def test(self):
        testContents = [ "i am 28 years old", "is 007c a good code", "what about 007cos", "@8374!k*3731, thats weird"]
        R1 = ["i am years old", "is a good code", "what about", "thats weird"] 
        self.assertEqual(testMethod(testContents), R1)
        #passes ok
        
        

if __name__ == "__main__":
    removeNumbers()
    
    
    