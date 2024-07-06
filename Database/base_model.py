from .db_connection import db
from bson.objectid import ObjectId


class BaseCollection:
    def __init__(self, collection_name, use_custom_id=False):
        self.collection = db.get_collection(collection_name)
        self.use_custom_id = use_custom_id
        if self.use_custom_id:
            self.counter_collection = db.get_collection('counters')
    
    def get_next_sequence_value(self):
        sequence_doc = self.counter_collection.find_one_and_update(
            {'_id': self.collection.name},
            {'$inc': {'sequence_value': 1}},
            upsert=True,
        )
        return sequence_doc['sequence_value']
    
    def id_type(self, id):
        if self.use_custom_id:
            return int(id)
        return ObjectId(id)
    

    def prosessing(cls, data):
        return {key: str(value) if isinstance(value, ObjectId) else value for key, value in data.items()}
        

    def find_all(self, projection=None):
        if projection:
            return self.collection.find({}, projection)
        return self.collection.find()


    def find_by_id(self, id):
        return self.collection.find_one({"_id": self.id_type(id)})


    def insert(self, data):
        if type(data) is list:
            if self.use_custom_id:
                for item in data:
                    item['_id'] = self.get_next_sequence_value()
            return self.collection.insert_many(data).inserted_ids

        if self.use_custom_id:
            data['_id'] = self.get_next_sequence_value()
        return self.collection.insert_one(data).inserted_id


    def update(self, problem_id, data):
        return self.collection.update_one({"_id": self.id_type(problem_id)}, {"$set": data})

    def delete(self, id):
        return self.collection.delete_one({"_id": self.id_type(id)})
