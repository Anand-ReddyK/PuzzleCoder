from django.conf import settings
from django.contrib.sessions.backends.base import SessionBase, CreateError
from datetime import datetime, timedelta
from .db_connection import db

class SessionStore(SessionBase):
    def __init__(self, session_key=None):
        super().__init__(session_key)
        self.db = db
        self.collection = self.db.get_collection(settings.MONGO_SESSION_COLLECTION)

    @property
    def session_key(self):
        return self._session_key

    @session_key.setter
    def session_key(self, value):
        self._session_key = value

    def load(self):
        session_data = self.collection.find_one({"_id": self.session_key})
        if session_data and session_data['expire_date'] > datetime.utcnow():
            return self.decode(session_data['session_data'])
        self.create()
        return {}

    def create(self):
        while True:
            self._session_key = self._get_new_session_key()
            try:
                self.save(must_create=True)
            except CreateError:
                continue
            self.modified = True
            return

    def save(self, must_create=False):
        if self.session_key is None:
            self.create()

        session_data = {
            '_id': self.session_key,
            'session_data': self.encode(self._get_session(no_load=must_create)),
            'expire_date': self.get_expiry_date(),
        }

        if must_create:
            if self.collection.find_one({'_id': self.session_key}):
                raise CreateError
            self.collection.insert_one(session_data)
        else:
            self.collection.update_one({'_id': self.session_key}, {'$set': session_data}, upsert=True)

    def delete(self, session_key=None):
        if session_key is None:
            session_key = self.session_key
        self.collection.delete_one({'_id': session_key})

    def exists(self, session_key):
        return self.collection.find_one({'_id': session_key}) is not None

    def clear_expired(self):
        self.collection.delete_many({'expire_date': {'$lt': datetime.utcnow()}})
