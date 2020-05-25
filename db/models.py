from flask import Markup, render_template_string
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
from humanize import naturaltime

db = SQLAlchemy()

class notifications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    important = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime)
    head = db.Column(db.String(128))
    body = db.Column(db.String(512))

    def __init__(self, id, important, timestamp, head, body):
        self.id = id
        self.important = important
        self.timestamp = timestamp
        self.head = head
        self.body = body

    def __iter__(self):
        yield "id", self.id
        yield "important", self.important
        yield "timestamp", self.timestamp
        yield "head", self.head
        yield "body", self.body

    def __repr__(self):
        return(f"<Notification {self.id}>")

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True)
    key = db.Column(db.String(36), unique=True)