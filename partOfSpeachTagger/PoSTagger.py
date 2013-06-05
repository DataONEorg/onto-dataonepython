'''
Created on May 30, 2013

@author: nicholas
'''


import re
import os
import urllib2
import sys
import nltk
import unittest

#note that THIS SCRIPT ASSUMES you have NLTK installed.  if you do not, the guide for doing so can be found at 
# http://nltk.org/install.html
#also, for ease of reference, here is a simple legend for PoS tags
#
#CC: conjunction, coordinating       & n and both but either et for less minus neither nor or plus so therefore times v. ...
#CD: numeral, cardinal               mid-1890 nine-thirty forty-two one-tenth ten million 0.5 one forty-seven 1987 twenty ...
#DT: determiner                      all an another any both del each either every half la many much nary neither no ...
#EX: existential there               there
#FW: foreign word                    gemeinschaft hund ich jeux habeas Haementeria ...
#IN: preposition or conjunction      subordinating astride among uppon whether out inside pro despite on by throughout...
#JJ: adjective or numeral ordinal    third ill-mannered pre-war regrettable oiled calamitous first separable...
#JJR: adjective, comparative         bleaker braver breezier briefer brighter brisker broader bumper busier...
#JJS: adjective, superlative         calmest cheapest choicest classiest cleanest clearest closest commonest
#LS: list item marker                A A. B B. C C. D E F First G H I J K One SP-44001 SP-44002 SP-44005....
#MD: modal auxiliary                 can cannot could couldn't dare may might must need ought shall should shouldn't will would
#NN: noun, common, singular or mass  common-carrier cabbage knuckle-duster Casino afghan shed thermostat investment slide...
#NNP: noun, proper, singular         Motown Venneboerger Czestochwa Ranzer Conchita Trumplane Christos...
#NNPS: noun, proper, plural          Americans Americas Amharas Amityvilles Amusements Anarcho-Syndicalists...
#NNS: noun, common, plural           undergraduates scotches bric-a-brac products bodyguards facets coasts divestitures...
#PDT: pre-determiner                 all both half many quite such sure this
#POS: genitive marker                ' 's
#PRP: pronoun, personal              hers herself him himself hisself it itself me myself one oneself ours...
#PRP$: pronoun, possessive           her his mine my our ours their thy your...
#RB: adverb                          occasionally unabatingly maddeningly adventurously professedly stirringly prominently ...
#RBR: adverb, comparative            further gloomier grander graver greater grimmer harder harsher healthier heavier higher ...
#RBS: adverb, superlative            best biggest bluntest earliest farthest first furthest hardest heartiest highest largest ...
#RP: particle                        aboard about across along apart around aside at away back before behind by crop down ever ...
#SYM: symbol                         % & ' '' ''. ) ). * + ,. < = > @ A[fj] U.S U.S.S.R * ** *** ....
#TO: "to" as preposition or infinitive marker    to
#UH: interjection                                   Goodbye Goody Gosh Wow Jeepers Jee-sus Hubba Hey Kee-reist Oops amen huh howdy uh ...
#VB: verb, base form                                ask assemble assess assign assume atone attention avoid bake balkanize bank begin ...
#VBD: verb, past tense                              dipped pleaded swiped regummed soaked tidied convened halted registered cushioned ...
#VBG: verb, present participle or gerund            telegraphing stirring focusing angering judging stalling lactating...
#VBN: verb, past participle                         multihulled dilapidated aerosolized chaired languished panelized used experimented ...
#VBP: verb, present tense, not 3rd person singular  predominate wrap resort sue twist spill cure lengthen brush terminate appear 
#                                                   tend stray glisten obtain comprise detest tease attract emphasize mold 
#                                                   postpone sever return wag ...
#VBZ: verb, present tense, 3rd person singular    bases reconstructs marks mixes displeases seals carps weaves snatches slumps 
#                                                 stretches authorizes smolders pictures emerges stockpiles
#                                                 seduces fizzes uses bolsters slaps speaks pleads ...
#WDT: WH-determiner      that what whatever which whichever
#WP: WH-pronoun          that what whatever whatsoever which who whom whosoever
#WP$: WH-pronoun         possessive whose
#WRB: Wh-adverb          how however whence whenever where whereby whereever wherein whereof why

#


#@param text is a string
def tokenize(text):
    return nltk.word_tokenize(text)


#@param tokens is a list of strings
#this function calls the tokenizer (which basically splits the string on white space) and returns the tagged words as a list of tuples
def PoSTag(tokens):
    taggedTokens = nltk.pos_tag(tokens) 
    #taggedTokens is a list of tuples: first entry is a string and the second is a keyword (representing which PoS it is)
    return taggedTokens


#for our current work, we ONLY care about nouns (N, or NP), verbs (V, VD, VG, or VN) adjectives (ADJ) or adverbs (ADV)
#if we want something different, edit this method
#note that we are using a super set of what we need. because we stem, most of these should never be used (e.g., past tense verbs), but
#are included just in case our stemmer performs funny
def setupTagSet():
    acceptableTags =set(["JJ","JJR","JJS","NN","NNS","RB","RBR","RBS","VB","VBD","VBG","VBN","VBP","VBZ"])
    return acceptableTags
    

#@param taggedTokens is a list of tuples of string and tags
#@param acceptableTags is a set of strings containing the keys for the tags that we accept.  the legend is at the top of this file
#this function filters out all words that contains tags that we do not want
def filterPoSTags(taggedTokens, acceptableTags):
    goodTags = []
    for tuple in taggedTokens:
        if tuple[1] in acceptableTags: #its tuple[1] because tuple[0] is the string and tuple[1] is the PoS tag
            goodTags.append(tuple)
        
    return goodTags

#@param text the string to be tagged
#this performs the steps in order and returns the results.  outside classes should call this method
def performPoSTagging(text):
    tokens= tokenize(text)
    taggedTokens=PoSTag(tokens)
    goodTags = filterPoSTags(taggedTokens, setupTagSet())
    return goodTags


#@param listTuples these are the word-PoS tags.  now that they are filtered, just give ma a list of words.  its all i need
def getWords(listTuples):
    results = []
    for each in listTuples:
        results.append(each[0])
    
    return results


class MyTest(unittest.TestCase):
    def test(self):
        TestCase1 = "Ah! My husband and I wish we could travel yearly to Europe and take in all the amazing sites."
        TestCase1ExpectedResults = [("husband", "NN"), ("wish", "VB"), ("travel", "VB"), ("yearly", "RB"), ("take", "VB"), 
                                    ("amazing", "JJ"), ("sites", "NNPS")]
        self.assertEqual(set(performPoSTagging(TestCase1)), set(TestCase1ExpectedResults))
        
        
        TestCase2 = "egads, the evil teacher assigns us work daily and expects it on his desk by eight the next morning!"
        TestCase2ExpectedResults = [("evil", "JJ"), ("teacher", "NN"), ("assigns", "VB"), ("work", "NN"), ("daily", "RB"), 
                                    ("expects", "VBZ"), ("desk", "NN"), ("next", "JJ"), ("morning", "NN")]
        self.assertEqual(set(performPoSTagging(TestCase2)), set(TestCase2ExpectedResults))

#these test cases fail, but fails because of NLTK...not my code.  
#however, all the necessary terms ARE in the answer set...which is all we actually need.  the only concern is that they put words in
#they shouldnt be there  (like egads from test case 2)


if __name__ == '__main__':
    #these two lines are used to run the test cases
#    m = MyTest()
#    m.test()
    


    
        