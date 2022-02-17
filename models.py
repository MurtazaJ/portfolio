from extensions import db
from datetime import datetime

class Testimony(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    company_name = db.Column(db.String(100))
    testimony = db.Column(db.Text,nullable=False)

class Question(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow )

class Contact(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow )