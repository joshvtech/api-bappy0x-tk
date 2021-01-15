from flask import Markup, render_template_string
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime
from uuid import uuid4

db = SQLAlchemy()

class tblNotifications(db.Model):
    __tablename__ = "tblNotifications"
    id = db.Column(db.Integer, primary_key=True)
    important = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime)
    head = db.Column(db.String(128))
    body = db.Column(db.String(512))

    def __iter__(self):
        yield "id", self.id
        yield "important", self.important
        yield "timestamp", self.timestamp
        yield "head", self.head
        yield "body", self.body

    def __repr__(self):
        return(f"<Notification {self.id}>")

class tblVxTech_bank(db.Model):
    __tablename__ = "tblVxTech-bank"
    id = db.Column(db.Integer, primary_key=True)
    placeId = db.Column(db.Integer)
    userId = db.Column(db.Integer)
    balance = db.Column(db.Float, default=0)

    def __iter__(self):
        yield "id", self.id
        yield "placeId", self.placeId
        yield "userId", self.userId
        yield "balance", self.balance

    def __repr__(self):
        return(f"<VxTech Bank # {self.id}>")

class tblVxTech_tokens(db.Model):
    __tablename__ = "tblVxTech-tokens"
    token = db.Column(db.String(128), primary_key=True)
    placeId = db.Column(db.Integer)
    
    def generateToken(self):
        tok = uuid4().hex
        print(tok)
        self.token = generate_password_hash(tok, method="sha256")
    def checkToken(self, pwd):
        print(pwd)
        return check_password_hash(self.token, pwd)

    def __iter__(self):
        yield "id", self.id
        yield "placeId", self.placeId
        yield "userId", self.userId
        yield "balance", self.balance

    def __repr__(self):
        return(f"<VxTech Token # {self.placeId}>")

class tblJetradio_events(db.Model):
    __tablename__ = "tblJetradio-events"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    image = db.Column(db.String(128))
    feature = db.Column(db.String(128))
    timeStart = db.Column(db.DateTime)
    timeEnd = db.Column(db.DateTime)

    def __iter__(self):
        yield "id", self.id
        yield "name", self.name
        yield "image", self.image
        yield "feature", self.feature
        yield "timeStart", self.timeStart
        yield "timeEnd", self.timeEnd

    def __repr__(self):
        return(f"<JetRadio Event # {self.id}>")