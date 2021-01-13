from flask import Markup, render_template_string
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

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

    def __iter__(self):
        yield "id", self.id

    def __repr__(self):
        return(f"<VxTech Bank # {self.id}>")

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