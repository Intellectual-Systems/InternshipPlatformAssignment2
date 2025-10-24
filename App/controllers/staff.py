from App.models.staff import Staff
from App.models.student import Student_Position
from App.database import db

def create_staff(username, password, employerID):
    sta = Staff(username, password, employerID)
    db.session.add(sta)
    db.session.commit()
    return sta

def get_staff_by_id(staffID):
    sta = Staff.query.filter_by(id=staffID).first()
    if not sta:
        return None
    return sta

def get_all_staff():
    staff = Staff.query.all()
    if not staff:
        return None
    return staff

def addToShortlist(self, positionID, studentID):
        
        position = InternshipPosition.query.filter_by(id=positionID).first()

        student = Student.query.filter_by(id=studentID).first()

        if position != None and student != None:
            position.shortlist.append(student)
            db.session.commit()
            return True

        return False
