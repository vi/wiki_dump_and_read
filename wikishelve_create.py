#!/usr/bin/env python

import shelve
#import zshelve
import sys
from xml.sax import make_parser, handler

if len(sys.argv)<2:
    sys.stderr.write("Usage: wikishelve_create shelve_file < dump.xml\n")
    sys.exit(1)

shelf = shelve.open(sys.argv[1])

class WikiShelveCreate(handler.ContentHandler):

    def __init__(self):
        self.char_chunks=[]
        self.cur_title=u""
        pass


    def startElement(self, name, attrs):
        self.char_chunks=[]

    def characters(self, content):
        self.char_chunks.append(content);

    def endElement(self, name):
        content = "".join(self.char_chunks)
        self.char_chunks=[]
        if(name=="title"):
            self.cur_title = content
        if(name=="text"):
            shelf[self.cur_title.encode("UTF-8")] = content
            print(self.cur_title.encode("UTF-8"))

            
parser = make_parser()
parser.setContentHandler(WikiShelveCreate())
parser.parse(sys.stdin)



