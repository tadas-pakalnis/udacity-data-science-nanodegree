# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 20:33:22 2016

@author: pakal

https://docs.python.org/3/library/xml.etree.elementtree.html
http://wiki.openstreetmap.org/wiki/OSM_XML
http://wiki.openstreetmap.org/wiki/Map_Features

Sample project:
https://docs.google.com/document/d/1F0Vs14oNEs2idFJR3C_OPxwS6L0HPliOii-QpbmrMo4/pub?embedded=True
"""

import os
# filepath for importing module
os.chdir(os.path.dirname(__file__))
# class methods: audit_tag_k, audit_tag_v
from Class_AuditOnce import AuditOnce
from Class_Db import Db
from pymongo import MongoClient
import json

# filepath for data
os.chdir(os.pardir+'\\data')

if __name__ == "__main__":
    # OPEN FILE
    tahoe= AuditOnce()
    tahoe.open_file("south-lake-tahoe_california.osm")
    
    # AUDIT
    # street, postcode, state
    tahoe.audit_tag_k(500)
    tahoe.audit_tag_v("addr:street")
    tahoe.audit_tag_v("addr:postcode")
    tahoe.audit_tag_v("addr:state")
    tahoe.pprint_set()

    
    # UPDATE
    
    # correct street names by mapping
    map_street = { "St": "Street",
               "Rd": "Road",
               "Ln":"Lane",
               "Blvd":"Boulevard"}
    tahoe.update_tag_v("addr:street", map_street)
    
    map_street = {"Hwy":"Highway"}
    tahoe.update_tag_v("addr:street", map_street, "in")

    # correct postcode with re matching
    tahoe.update_post()
  
    # correct states
    map_state = {"California": "CA",
                "Nevada":"NV"}
    tahoe.update_tag_v("addr:state", map_state, "in")
    
    # MongoDb
    tahoe_dict = Db(tahoe.root)
    data = tahoe_dict.process_map()
    
     
    # Read data from file to an array
    data = []
    for line in open('tahoe.json', 'r'):
        data.append(json.loads(line))
    
    # Insert the data into local MongoDB Database
    client = MongoClient('localhost', 27017)
    db = client.tahoe
    collection = db.tahoe
    collection.insert_many(data)
    
    collection
    
    # Stats
    # xml file size
    os.path.getsize("south-lake-tahoe_california.osm")/1024/1024
    # json file size
    os.path.getsize("tahoe.json")/1024/1024
    
    # unique users
    len(collection.distinct("created.uid"))
    
    # The Number of Nodes
    collection.find({"type":"node"}).count()
    
    # The Number of Ways
    collection.find({"type":"way"}).count()
    
    # Top 2 users
    result = collection.aggregate([
                {"$group":{"_id":"$created.user", "count":{"$sum":1} } },        
                {"$sort":{"count":-1} }, 
                {"$limit":2} ] )
    [i for i in result]
    
    
    # Most 5 popular restaurant
    result = collection.aggregate([
                {"$match":{"amenity":{"$exists":1}, "amenity":"restaurant", "cuisine":{"$exists":1} } }, 
                {"$group":{"_id":"$cuisine", "count":{"$sum":1} } },        
                {"$sort":{"count":-1} }, 
                {"$limit":5} ] )
    [i for i in result]
    

    #  Banks
    result = collection.aggregate([
                {"$match":{"amenity":{"$exists":1}, "amenity":"bank", "name":{"$exists":1} } }, 
                {"$group":{"_id":"$name", "count":{"$sum":1} } },        
                {"$sort":{"count":-1} }, 
                {"$limit":5} ] )
    [i for i in result]

    # Groupd Zip codes
    result = collection.aggregate([
                {"$match":{"address.postcode":{"$exists":1} } },
                {"$group":{"_id":"$address.postcode", "count":{"$sum":1} } } ])
    [i for i in result]
   
    # Top 5 amenities
    result = collection.aggregate([
                {"$match":{"amenity":{"$exists":1} } },
                {"$group":{"_id":"$amenity", "count":{"$sum":1} } },
                {"$sort":{"count":-1} }])
    
    # Top 3 fast foods
    result = collection.aggregate([
                {"$match":{"amenity":{"$exists":1}, "amenity":"fast_food", "name":{"$exists":1} } }, 
                {"$group":{"_id":"$name", "count":{"$sum":1} } },        
                {"$sort":{"count":-1} }, 
                {"$limit":5} ] )
    [i for i in result]
    
    # Top user contribution
    result = collection.aggregate([
                {"$group":{"_id": "$created.user", "count": {"$sum": 1}}},
                {"$project": {"ratio": {"$divide" :["$count",collection.count()] } } },
                {"$sort": {"ratio": -1} },
                {"$limit": 1} ])
    [i for i in result]
    
    # users with num amenities added
    
    result = collection.aggregate([
                {"$match":{"amenity":{"$exists":1} } },
                {"$group":{"_id": "$created.user", "count": {"$sum": 1}}},
                {"$project": {"ratio": {"$divide" :["$count",collection.find({ "amenity":{"$exists":1} }).count()] },
                                                    "count_":"$count"} },
                {"$sort": {"ratio": -1} },
                {"$limit": 1} ])
    
