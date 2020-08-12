from flask import Flask, jsonify
from mongoengine import *
from application import application
from config import mongoLogin
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from config import SECRET_KEY


username = mongoLogin["username"]
password = mongoLogin["password"]
CONNECTION_STRING = f"mongodb+srv://{username}:{password}@algo.7da41.mongodb.net/?retryWrites=true&w=majority"
client = connect(CONNECTION_STRING)
db = client.get_database('algo_db')
user_collection = mongoengine.collection.Collection(db, 'users')
algorithm_collection = mongoengine.collection.Collection(db, 'algorithms')


class SampleInput(EmbeddedDocument):
    pass

class SampleOutput(EmbeddedDocument):
    pass

class Options(EmbeddedDocument):
    validated_email = BooleanField(default = False)
    developer = BooleanField(default = False)
    admin = BooleanField(default = False)


class Algorithm(Document):
    id = ObjectIdField()
    title = StringField(required=True, max_length=200)
    description = StringField(required=True)
    author = ReferenceField(User)
    sample_input = DictField(EmbeddedDocumentField(SampleInput))
    sample_output = DictField(EmbeddedDocumentField(SampleOutput))
    date_submitted = DateTimeField(default=datetime.utcnow)
    tags = ListField(StringField(default=[]))

class User(Document):
    id = ObjectIdField()
    username = StringField(required=True, max_length=20, unique=True)
    email = EmailField(required=True,max_length=100,unique=True)
    password = PasswordField()
    options = DictField(EmbeddedDocumentField(Options))
    photo = ObjectField(required=False, default='default.jpg')
    date_joined = DateTimeField(default=datetime.utcnow)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.find_one(user_id)