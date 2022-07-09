from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
class Container(db.Model):
    id = db.Column(db.Text, primary_key =True)
    img_before = db.Column(db.LargeBinary, nullable = False)
    img_after = db.Column(db.LargeBinary, nullable= False)
    create_at = db.Column(db.DateTime, default=datetime.now())
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __repr__(self):
        return '<Container %r>' % self.id

class User(db.Model):
    id = db.Column(db.Integer, primary_key =True, autoincrement=True)
    username = db.Column(db.String(255), nullable = False)
    password = db.Column(db.String(255), nullable = False)
    email = db.Column(db.String, nullable = False)
    isAdmin = db.Column(db.Boolean, default=False)
    container_list = db.relationship('Container', backref='user')

    def __repr__(self):
        return '<User %r>' % self.username



    
    