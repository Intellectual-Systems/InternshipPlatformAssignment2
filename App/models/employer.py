from App.database import db
from .user import User
from .internshipposition import InternshipPosition
from .student import Student_Position

class Employer(User):

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    companyName = db.Column(db.String(20), nullable=False)

    def __init__(self, username, password, companyName):
        self.username = username
        self.set_password(password)
        self.companyName = companyName
    
    def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'companyName': self.companyName
        }

    def __repr__(self):
        return f"Employer[id= {self.id}, username= {self.username}, companyName= {self.companyName}]"


    
