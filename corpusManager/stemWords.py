#! /usr/bin/env python

from porter2 import stem as p2
from porter import stem as p1
from lovins import stem as lovins
from paicehusk import stem as paice
import os
import unittest


#if you want a different type of stemming, replace p2 with whichever type of stemming you want, 
# p2 = snowball
# p1 = porter
# lovins = lovins
# paice = paicehusk

def stemWords(): 
    os.chdir(os.pardir+ "/data")
    existingData = "nostop_3.txt"
    newfile = open("nowStemmed_4.txt", "w+") 
    
    contents = open(existingData).readlines()

    for j in range(0, len(contents)):
        
        results = []     
        words = contents[j].split(" ")
        for i in range(0, len(words)):
            results.append(p2(words[i]))
        
        results = ' '.join(results)
            
        newfile.write(results)
        print results

class MyTest(unittest.TestCase):
    def test(self):
        TC1 = "appeared"
        R1 = "appear" 
        self.assertEqual(p2(TC1), R1)
        
        TC2 = "gears"
        R2 = "gear" 
        self.assertEqual(p2(TC2), R2)
        
        TC3 = "actually"
        R3 = "actual" 
        self.assertEqual(p2(TC3), R3)
        
        TC4 = "rate"
        R4 = "rate" 
        self.assertEqual(p2(TC4), R4)
        
        TC5 = "loaves"
        R5 = "loaf" 
        self.assertEqual(p2(TC5), R5)
        #it cannot handle this test.   FAIL  (returns loav)


if __name__ == "__main__":
    stemWords()