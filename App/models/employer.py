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

    def createPosition(self, positionTitle, department, description):
        pos = InternshipPosition(employerID=self.id, positionTitle=positionTitle, department=department, description=description)
        db.session.add(pos)
        db.session.commit()
        return pos
    
    def acceptReject(self, studentID, positionID, status, message=None):
        sp = Student_Position.query.filter_by(studentID=studentID, positionID=positionID).first()
        if sp:
            sp.status = status
            sp.employer_response = message

            # Automatically reject every other student who was shortlisted for this position

            if status.lower() == 'accepted':
                otherStudents = Student_Position.query.filter_by(positionID=positionID).all()
                for os in otherStudents:
                    if os.studentID != sp.studentID:
                        os.status = 'rejected'

            db.session.commit()
            return True
        return False