from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Container(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    img_before = db.Column(db.LargeBinary, nullable = False)
    img_after = db.Column(db.LargeBinary, nullable= False)