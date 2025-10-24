import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User
from App.models.employer import Employer
from App.models.staff import Staff
from App.models.student import Student
from App.models.student import Student_Position
from App.models.internshipposition import InternshipPosition
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user
)

LOGGER = logging.getLogger(__name__)

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="function")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    with app.app_context():
        create_db()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass")
        db.session.add(user)
        db.session.commit()

        assert db.session.query(User).filter_by(username="bob").first() is not None
        # assert user.username == "bob"

    # pure function no side effects or integrations called
    # def test_get_json(self):
    #     user = User("bob", "bobpass")
    #     user_json = user.get_json()
    #     self.assertDictEqual(user_json, {"id":None, "username":"bob"})
    
    # def test_hashed_password(self):
    #     password = "mypass"
    #     hashed = generate_password_hash(password, method='sha256')
    #     user = User("bob", password)
    #     assert user.password != password

    # def test_check_password(self):
    #     password = "mypass"
    #     user = User("bob", password)
    #     assert user.check_password(password)

class EmployerUnitTests(unittest.TestCase):

    def test_new_employer(self):
        emp = Employer("emp1", "emp1pass", "TechCorp")
        db.session.add(emp)
        db.session.commit()

        assert db.session.query(Employer).filter_by(username="emp1").first() is not None
    
    def test_new_position(self):
        emp = Employer("emp2", "emp2pass", "TechCorp")
        db.session.add(emp)
        db.session.commit()

        position = emp.createPosition("Inventory Clerk", "Inventory","Data entry and stock management")
        db.session.add(position)
        db.session.commit()

        assert db.session.query(InternshipPosition).filter_by(id=position.id).first() is not None

class StaffUnitTests(unittest.TestCase):

    def test_new_staff(self):
        emp = Employer("emp1", "emp1pass", "TechCorp")
        db.session.add(emp)
        db.session.commit()

        staff = Staff("staff1", "staff1pass", emp.id)
        db.session.add(staff)
        db.session.commit()

        assert db.session.query(Staff).filter_by(id=staff.id).first() is not None
        # assert staff.username == "staff1"
    
    def test_enroll_student(self):
        emp = Employer("emp3", "emp3pass", "TechCorp")
        db.session.add(emp)
        db.session.commit()

        staff = Staff("staff2", "staff2pass", emp.id)
        db.session.add(staff)
        db.session.commit()

        student = Student("stud1", "stud1pass", "FST", "DCIT", "BSc Comp Sci", 3.8)
        db.session.add(student)
        db.session.commit()

        position = emp.createPosition("Inventory Clerk", "Inventory","Data entry and stock management")
        db.session.add(position)
        db.session.commit()

        staff.addToShortlist(position.id, student.id)
        db.session.add(staff)
        db.session.commit()
        
        assert db.session.query(Student_Position).filter_by(studentID=student.id, positionID=position.id).first() != None

class StudentUnitTests(unittest.TestCase):

    def test_new_student(self):
        student = Student("stud1", "stud1pass", "FST", "DCIT", "BSc Comp Sci", 3.8)
        db.session.add(student)
        db.session.commit()

        assert db.session.query(Student).filter_by(id=student.id).first() is not None
        # assert student.username == "stud1"

class TestEmployerUnit(unittest.TestCase):
    
    def test_new_employer(self):
        employer = Employer("bob_emp", "bobpass", "Bob's Company")
        assert employer.username == "bob_emp"
        assert employer.companyName == "Bob's Company"

    def test_employer_password_hashed(self):
        password = "mypass"
        employer = Employer("rick_emp", password, "Rick's Corp")
        assert employer.password != password

    def test_employer_check_password(self):
        password = "mypass"
        employer = Employer("rick_emp", password, "Rick's Corp")
        assert employer.check_password(password)

'''
    Integration Tests
'''

def test_authenticate():
    user = create_user("bob", "bobpass")
    assert login("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick", "bobpass")
        assert user.username == "rick"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"
        
if __name__ == "__main__":
    unittest.main()
