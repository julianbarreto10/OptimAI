from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Driver(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    tp_veh = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    client_id = db.Column(db.String(50), nullable=False)