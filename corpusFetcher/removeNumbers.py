#! /usr/bin/env python


import re
import os
#this goes through and removes a word if it ONLY has numbers.  otherwise it leaves all other words alone
def removeNumbers(): 

    os.chdir(os.pardir+ "/data")
    
    existingData = "nowStemmed_4.txt"
    newfile = open("noAllNumbers_5.txt", "w+") 
    
    contents = open(existingData).readlines()

    for line in contents:
        word_list = line.strip().split()
        filtered_words = [w for w in word_list if re.match("[a-zA-Z]", w) is not None]
        #print filtered_words
        filtered_line = " ".join(filtered_words)
    
        newfile.write(filtered_line + "\n")
        print filtered_line

    newfile.close()


if __name__ == "__main__":
    removeNumbers()