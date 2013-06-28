#! /usr/bin/env python
import os
import urllib2
from xml.dom.minidom import parse, parseString, getDOMImplementation
from urlparse import urlsplit, urljoin, urlunsplit
import codecs



# Deal with downloading and processing a single url
def parse_and_save (url, idfile, wordfile): 

    response = urllib2.urlopen(url).read()

    dom = parseString(response)

    #impl = getDOMImplementation
    docs = dom.getElementsByTagName('doc')

    for document in docs:

        for str in document.childNodes:
            if str.attributes["name"].value == "id":
                idfile.write (str.firstChild.nodeValue + '\n')
        

        

        for node in document.childNodes:
            abstract_text=""
            title_text=""
            keyword_text=""
            
            if node.attributes["name"].value == "abstract":
                abstract_text = " ".join(node.firstChild.nodeValue.splitlines() ) + ' ' 
            if node.attributes["name"].value == "title":
                title_text = " ".join(node.firstChild.nodeValue.splitlines() ) + ' ' 
            if node.attributes["name"].value == "keywords":
                keyword_text = ""
                for child in node.childNodes:
                    keyword_text = keyword_text + " ".join(child.firstChild.nodeValue.splitlines() ) + ' ' 

        #print title_text
        #print abstract_text
        #print keyword_text

        wordfile.write (title_text + abstract_text + keyword_text)

        wordfile.write ("\n")
        
        
os.chdir(os.pardir+ "/data")
idfile = open ("idfile.txt", "w+")
wordfile = codecs.open ("wordfile.txt", encoding='utf8', mode="w+")

for x in range(0,47):
    url = "https://cn.dataone.org/cn/v1/query/solr/?fl=id,title,abstract,keywords&q=formatType:METADATA+-obsoletedBy:*&rows=1000&start="

    url = "%s%i" % (url, x*1000) 
    print (url)
    parse_and_save (url, idfile, wordfile)
 
idfile.close()
wordfile.close()

 


