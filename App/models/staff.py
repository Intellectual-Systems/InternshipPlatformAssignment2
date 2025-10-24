from App.database import db
from .user import User

from sqlalchemy import select

class Staff(User):
    
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    employerID = db.Column(db.Integer, db.ForeignKey('employer.id'), nullable=False)

    def __init__(self, username, password, employerID):
        self.username = username
        self.set_password(password)
        self.employerID = employerID

    def get_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'employerID': self.employerID
        }

    def __repr__(self):
        return f"Staff[id= {self.id}, username= {self.username}, employerID= {self.employerID}]"

    
