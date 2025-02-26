
from server import db
from uuid import uuid4
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

class Search(db.Model):
    __tablename__= 'search'
    id = db.Column(db.String(),primary_key=True, default=lambda: str(uuid4()))
    query = db.Column(db.String(),nullable=False)
    user_id = db.Column(db.String,db.ForeignKey("users.id"))

    def __repr__(self):
        return f".User.{self.query}"

    def save(self):
        db.session.add(self)
        db.session.commit()


class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String(),primary_key=True, default=lambda: str(uuid4()))
    username = db.Column(db.String,nullable=False)
    password = db.Column(db.Text)
    searches = db.relationship(Search,backref="user")

    def __repr__(self):
        return f".User.{self.username}"    
    

    def generate_password(self,password):
        return generate_password_hash(password)

    def check_password_hash(self,password):
        return check_password_hash(self.password,password)
    
    def set_password(self,password):
        self.password = generate_password_hash(password)


    def save(self):
        db.session.add(self)
        db.session.commit()
