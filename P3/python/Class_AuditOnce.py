# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 20:33:22 2016

@author: pakal

"""
from Class_Audit import Audit
import xml.etree.ElementTree as ET    

class AuditOnce(Audit):
    """
    open files for parsing
    """
    def open_file(self, file_name):
        self.tree = ET.parse(file_name)
        self.root = self.tree.getroot()
        print "File opened"
        
    """
    get k tag values and count the appearances
    print_num - specifies how many values you want to see, 0-> all
    """
    def audit_tag_k(self, print_num = 0):
        self.__init__()
        for element in self.root:
            for tag in element.iter("tag"):                       
                elem = tag.attrib['k']
                self.audit_int[elem] += 1
        self.print_sorted_dict(self.audit_int, print_num)
        
    
    """
    get v tag values
    prints a dict of appearances
    a dict of unique variations can also be printed
    print_num - specifies how many values you want to see, 0-> all
    """
    def audit_tag_v(self, attribute="", print_num = 0):
        self.__init__()
        for element in self.root:
            for tag in element.iter("tag"):            
                if self.is_name(tag, attribute):
                    # create attribute dictionary
                    self.audit_int[tag.attrib['v']] += 1
                    # create a set
                    self.audit_type(tag.attrib['v'])
        self.print_sorted_dict(self.audit_int, print_num)
        
    """
    update tags based on attribute to update, a dict mapping and type
    update_type=re is the default and uses last word matching
    if re is not used than a string is matched using "in" method
    """
    def update_tag_v(self, attribute_to_update, update_mapping,
                     update_type="re"):
        self.__init__()
        for element in self.root:
            for tag in element.iter("tag"):            
                if self.is_name(tag, attribute_to_update):
                    if update_type == "re":
                        new_name = self.update_name_re(tag.attrib['v'], update_mapping)
                    else:
                        new_name = self.update_name_in(tag.attrib['v'], update_mapping)
                    # update tag if return is not None                    
                    if new_name != None:
                        tag.attrib['v'] = new_name
                    # run audit again, to confirm changes
                    self.audit_type(tag.attrib['v'])
        self.pprint_set()
    
    """
    update postcode programatically, by searching for 5 digits
    if 5 digits not found, set value to NA
    """
    def update_post(self):
        self.__init__()
        for element in self.root:
            for tag in element.iter("tag"):            
                if self.is_name(tag, "addr:postcode"):
                    new_name = self.update_post_re(tag.attrib['v'])
                    tag.attrib['v'] = new_name
                    self.audit_type(tag.attrib['v'])
        self.pprint_set()
        
    """
    get tag names and their occurances
    """
    def audit(self):
        for element in self.root:          
            elem = element.tag
            self.audit_int[elem] += 1
        self.print_sorted_dict(self.audit_int)
        
    
    """
    create a new xml file
    """        
    def write(self):
        self.tree.write('output.xml')
        