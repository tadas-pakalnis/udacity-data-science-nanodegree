# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 20:33:22 2016

@author: pakal


"""

from collections import defaultdict
import re
import pprint
    
class Audit:
    

    def __init__(self):
        self.audit_int = defaultdict(int)
        self.audit_set = defaultdict(set)
    
    """
    sort values by their count in descending order and print the result
    count - specifies how many values you want to see, 0-> all
    """
    def print_sorted_dict(self, d, count=0):
        keys = d.keys()
        keys = sorted(keys, key=lambda s: s.lower())
        for k in keys:
            v = d[k]
            if v > count:
                print "%s: %d" % (k, v)
    
    """
    get k value of attribute
    """
    def is_name(self, elem, attribute):
        if attribute == "":
            return True
        return (elem.attrib['k'] == attribute)
    
    """
    get last word of each attribute and create a set of arrays (array stores full name)
    """
    def audit_type(self, name):
        # type_re finds last word
        type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
        m = type_re.search(name)
        if m:
            name_type = m.group()
            self.audit_set[name_type].add(name)
    
    """
    update attribute name by using re and "in" method
    """
    def update_name_re(self, name, update_mapping):
        # type_re finds last word
        type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
        m = type_re.search(name)
        if m:
            name_type = m.group()
            if name_type in update_mapping:
                new_name = name.replace(name_type, 
                                        update_mapping[name_type])
                return new_name
    
    """
    clean/ update postcodes by searching for 5 digits, if not found return NA
    """
    def update_post_re(self, name):
        m = re.findall(r'\d{5}', name)
        if not m:
            return 'NA'
        else:
            return m[0]
            
    """
    update attribute name by using "in" method
    """
    def update_name_in(self, name, update_mapping):
        for key, value in update_mapping.items():
            if key in name:
                new_name = name.replace(key, value)
                return new_name


    """
    print nice dict
    """
    def pprint_set(self):
        pprint.pprint(dict(self.audit_set))