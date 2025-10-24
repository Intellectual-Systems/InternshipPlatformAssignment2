from App.database import db
from App.models.user import User

class Student_Position(db.Model):
    __tablename__ = 'student_position'
    studentID = db.Column(db.Integer, db.ForeignKey('student.id'), primary_key=True)
    positionID = db.Column(db.Integer, db.ForeignKey('internshipposition.id'), primary_key=True)
    status = db.Column(db.String(20), nullable=False, default='pending')
    employer_response = db.Column(db.String(20), nullable=True, default=None)

    def __init__(self, studentID, positionID):
        self.studentID = studentID
        self.positionID = positionID

    def get_json(self):
        return {
            'studentID': self.studentID,
            'positionID': self.positionID,
            'status': self.status,
            'employer_response': self.employer_response
        }

    def __repr__(self):
        return f"Student_Position[studentID= {self.studentID} -> positionID= {self.positionID}, status= {self.status}, employer_response= {self.employer_response}]"

class Student(User):

    __tablename__ = 'student'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    faculty = db.Column(db.String(20), nullable=False)
    department = db.Column(db.String(20), nullable=False)
    degree = db.Column(db.String(20), nullable=False)
    gpa = db.Column(db.Integer, nullable=False)
    shortlists = db.relationship('InternshipPosition', secondary='student_position', back_populates='shortlist')

    def __init__(self, username, password, faculty, department, degree, gpa):
        self.username = username
        self.set_password(password)
        self.faculty = faculty
        self.department = department
        self.degree = degree
        self.gpa = gpa

    def get_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'faculty': self.faculty,
            'department': self.department,
            'degree': self.degree,
            'gpa': self.gpa
        }

    def __repr__(self):
        return f"Student[id= {self.id}, username= {self.username}, faculty= {self.faculty}, department= {self.department}, degree= {self.degree}, gpa= {self.gpa}]"