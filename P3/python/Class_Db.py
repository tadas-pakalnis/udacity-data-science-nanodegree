# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 20:33:22 2016

@author: pakal

"""
import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

class Db():
    
    def __init__(self, root):
        self.root = root
    
    def assign(self, element, node, attribute):
        try:
            node[attribute] = element.attrib[attribute]
        except:
            pass
        return node

    def shape_element(self, element):
        node = {}
        if element.tag == "node" or element.tag == "way" :
    
            node = self.assign(element, node, "id")
            node = self.assign(element, node, "visible")
            node["type"] = element.tag
            try:
                node["pos"] = [float(element.attrib["lat"]), float(element.attrib["lon"])]
            except:
                pass
    
            node["created"] = {}
            for i in CREATED:
                node["created"][i] = element.attrib[i]
    
            addr = {}
            for tag in element.iter("tag"):
                if ":" in tag.attrib["k"] and tag.attrib["k"].count(":") == 1:
                    names = tag.attrib["k"].split(":")
                    if "addr" in names:
                        addr[names[1]] = tag.attrib["v"]
                elif ":" not in tag.attrib["k"]:
                    if not re.match(problemchars, tag.attrib["k"]):
                        node[tag.attrib["k"]] = tag.attrib["v"]
    
    
            if len(addr) > 0:
                node["address"] = addr
    
            arr = []
            for nd in element.iter("nd"):
                arr.append(nd.attrib["ref"])
    
            if len(arr) > 0:
                node["node_refs"] = arr
    
    
            return node
        else:
            return None


    def process_map(self, pretty = False):
        # You do not need to change this file
        file_out = "tahoe.json"
        self.data = []
        with codecs.open(file_out, "w") as fo:
            for element in self.root:
                el = self.shape_element(element)
                if el:
                    self.data.append(el)
                    if pretty:
                        fo.write(json.dumps(el, indent=2)+"\n")
                    else:
                        fo.write(json.dumps(el) + "\n")
    
        