#! /usr/bin/env python

from porter2 import stem
import os
import unittest


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

class MyTest(unittest.TestCase):
    def test(self):
        TC1 = "appeared"
        R1 = "appear" 
        self.assertEqual(stem(TC1), R1)
        
        TC2 = "gears"
        R2 = "gear" 
        self.assertEqual(stem(TC2), R2)
        
        TC3 = "actually"
        R3 = "actual" 
        self.assertEqual(stem(TC3), R3)
        
        TC4 = "rate"
        R4 = "rate" 
        self.assertEqual(stem(TC4), R4)
        
        TC5 = "loaves"
        R5 = "loaf" 
        self.assertEqual(stem(TC5), R5)
        #it cannot handle this test.   FAIL  (returns loav)


if __name__ == "__main__":
    stemWords()