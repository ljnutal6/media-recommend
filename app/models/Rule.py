import pymongo
from pymongo import MongoClient

client = MongoClient()
db = client.database
collection = db.ruleCollection

def add_rule(id_list, id, confidence):
  rule = {"lhs": id_list,
          "rhs": id,
          "confidence": confidence}
  rule_id = collection.insert(rule)
  return rule_id
    
def find(rule_id):
  return collection.find_one({"_id": rule_id})

def remove_all():
  collection.remove({})
