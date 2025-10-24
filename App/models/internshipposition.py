from App.database import db

class InternshipPosition(db.Model):

    __tablename__ = 'internshipposition'

    id = db.Column(db.Integer, primary_key=True)
    employerID = db.Column(db.Integer, db.ForeignKey('employer.id'), nullable=False)
    positionTitle = db.Column(db.String(20), nullable=False)
    department = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(20), nullable=False)
    shortlist = db.relationship('Student', secondary='student_position', back_populates='shortlists')

    def __init__(self, employerID, positionTitle, department, description):
        self.employerID = employerID
        self.positionTitle = positionTitle
        self.department = department
        self.description = description
    
    def get_json(self):
        return{
            'id': self.id,
            'employerID': self.employerID,
            'positionTitle': self.positionTitle,
            'department': self.department,
            'description': self.description,
            'shortlist': [student.id for student in self.shortlist]
        }

    def __repr__(self):
        return f"InternshipPosition[id= {self.id}, employerID= {self.employerID}, positionTitle= {self.positionTitle}, department= {self.department}, description= {self.description}, shortlist= {[student.id for student in self.shortlist]}]"