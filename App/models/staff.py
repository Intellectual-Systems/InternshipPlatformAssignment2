from App.database import db
from .user import User
from .internshipposition import InternshipPosition
from .student import Student

from sqlalchemy import select

class Staff(User):
    
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    employerID = db.Column(db.Integer, db.ForeignKey('employer.id'), nullable=False)

    def __init__(self, username, password, employerID):
        self.username = username
        self.set_password(password)
        self.employerID = employerID

    def __repr__(self):
        return f"Staff[id= {self.id}, username= {self.username}, employerID= {self.employerID}]"

    def addToShortlist(self, positionID, studentID):
        
        position = InternshipPosition.query.filter_by(id=positionID).first()

        student = Student.query.filter_by(id=studentID).first()

        if position != None and student != None:
            position.shortlist.append(student)
            db.session.commit()
            return True

        return False