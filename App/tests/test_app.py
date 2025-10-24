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
from App.controllers.employer import (
    create_employer,
    get_employer_by_id,
    get_all_employers,
    view_positions,
    view_position_shortlist,
    create_position as employer_create_position
)
from App.controllers.staff import (
    create_staff,
    get_staff_by_id,
    get_all_staff
)
from App.controllers.student import (
    create_student,
    get_student_by_id,
    get_all_students,
    get_student_position_by_id,
    get_all_student_positions
)
from App.controllers.internshipposition import (
    create_position,
    get_position_by_id,
    get_all_positions
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
        assert user.username == "bob"

    # pure function no side effects or integrations called
    # def test_get_json(self):
    #     user = User("bob", "bobpass")
    #     user_json = user.get_json()
    #     self.assertDictEqual(user_json, {"id":None, "username":"bob"})
    
    def test_hashed_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)

class EmployerUnitTests(unittest.TestCase):

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

class StaffUnitTests(unittest.TestCase):

    def test_new_staff(self):
        staff = Staff("staff1", "staff1pass", 1)
        assert staff.username == "staff1"
        assert staff.employerID == 1
    
    def test_staff_inherits_from_user(self):
        staff = Staff("staff1", "staff1pass", 1)
        assert isinstance(staff, User)
    
    def test_staff_password_hashed(self):
        password = "mypass"
        staff = Staff("staff1", password, 1)
        assert staff.password != password

class StudentUnitTests(unittest.TestCase):

    def test_new_student(self):
        student = Student("stud1", "stud1pass", "FST", "DCIT", "BSc Comp Sci", 3.8)
        assert student.username == "stud1"
        assert student.faculty == "FST"
        assert student.department == "DCIT"
        assert student.degree == "BSc Comp Sci"
        assert student.gpa == 3.8
        # assert student.username == "stud1"

'''
    Integration Tests
'''

class UserIntegrationTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass")
        db.session.add(user)
        db.session.commit()

        assert db.session.query(User).filter_by(username="bob").first() is not None
        # assert user.username == "bob"

    def test_create_user(self):
        user = create_user("rick", "bobpass")
        assert user.username == "rick"

    def test_get_all_users_json(self):
        create_user("bob", "bobpass")
        create_user("rick", "rickpass")
        users_json = get_all_users_json()
        assert len(users_json) == 2

    # Tests data changes in the database
    def test_update_user(self):
        user = create_user("bob", "bobpass")
        update_user(user.id, "ronnie")
        updated_user = get_user(user.id)
        assert updated_user.username == "ronnie"

    def test_get_user_by_username(self):
        create_user("alice", "alicepass")
        user = get_user_by_username("alice")
        assert user is not None
        assert user.username == "alice"

class EmployerIntegrationTests(unittest.TestCase):

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

    def test_create_employer(self):
        employer = create_employer("emp1", "emp1pass", "TechCorp")
        assert employer is not None
        assert employer.username == "emp1"
        assert employer.companyName == "TechCorp"
    
    def test_get_employer_by_id(self):
        employer = create_employer("emp2", "emp2pass", "DataCorp")
        retrieved_emp = get_employer_by_id(employer.id)
        assert retrieved_emp is not None
        assert retrieved_emp.companyName == "DataCorp"
    
    def test_create_position_via_controller(self):
        employer = create_employer("emp3", "pass", "StartupCo")
        position = create_position(employer.id, "Software Intern", "Engineering", "Python development")
        
        assert position is not None
        assert position.positionTitle == "Software Intern"
        assert position.department == "Engineering"
        assert position.employerID == employer.id

class StaffIntegrationTests(unittest.TestCase):

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

    def test_create_staff(self):
        employer = create_employer("emp1", "pass", "Company")
        staff = create_staff("staff1", "staffpass", employer.id)
        
        assert staff is not None
        assert staff.username == "staff1"
        assert staff.employerID == employer.id
    
    def test_get_staff_by_id(self):
        employer = create_employer("emp2", "pass", "Company2")
        staff = create_staff("staff2", "pass", employer.id)
        
        retrieved_staff = get_staff_by_id(staff.id)
        assert retrieved_staff is not None
        assert retrieved_staff.username == "staff2"
    
    def test_staff_add_student_to_shortlist(self):
        employer = create_employer("emp4", "pass", "Company4")
        staff = create_staff("staff3", "pass", employer.id)
        student = create_student("student1", "pass", "FST", "DCIT", "BSc CS", 3.5)
        position = create_position(employer.id, "Intern", "IT", "Description")
        
        # Staff adds student to shortlist
        result = staff.addToShortlist(position.id, student.id)
        assert result == True
        
        # Verify student was added
        shortlist = view_position_shortlist(position.id)
        assert shortlist is not None
        assert len(shortlist) == 1
        assert shortlist[0].studentID == student.id

class StudentIntegrationTests(unittest.TestCase):

    def test_new_student(self):
        student = Student("stud1", "stud1pass", "FST", "DCIT", "BSc Comp Sci", 3.8)
        db.session.add(student)
        db.session.commit()

        assert db.session.query(Student).filter_by(id=student.id).first() is not None
        # assert student.username == "stud1"

    def test_create_student(self):
        student = create_student("student1", "pass", "FST", "DCIT", "BSc CS", 3.8)
        
        assert student is not None
        assert student.username == "student1"
        assert student.faculty == "FST"
        assert student.gpa == 3.8
    
    def test_get_student_by_id(self):
        student = create_student("student2", "pass", "FST", "DCIT", "BSc IT", 3.5)
        
        retrieved_student = get_student_by_id(student.id)
        assert retrieved_student is not None
        assert retrieved_student.username == "student2"

class TestEmployerIntegration(unittest.TestCase):
    
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

def test_authenticate():
    user = create_user("bob", "bobpass")
    assert login("bob", "bobpass") != None

class WorkflowIntegrationTests(unittest.TestCase):
    """Test complete workflows integrating multiple controllers"""
    
    def test_complete_internship_workflow(self):
        # 1. Employer creates account
        employer = create_employer("techcorp", "pass", "TechCorp Inc")
        assert employer is not None
        
        # 2. Employer creates position
        position = create_position(employer.id, "Software Intern", "Engineering", "Python dev")
        assert position is not None
        
        # 3. Staff member is created for employer
        staff = create_staff("recruiter", "pass", employer.id)
        assert staff is not None
        
        # 4. Student creates account
        student = create_student("john", "pass", "FST", "DCIT", "BSc CS", 3.7)
        assert student is not None
        
        # 5. Staff adds student to position shortlist
        result = staff.addToShortlist(position.id, student.id)
        assert result == True
        
        # 6. Verify shortlist
        shortlist = view_position_shortlist(position.id)
        assert shortlist is not None
        assert len(shortlist) == 1
        assert shortlist[0].studentID == student.id
        assert shortlist[0].positionID == position.id
    
    def test_employer_accept_reject_workflow(self):
        # Setup
        employer = create_employer("company", "pass", "Company Inc")
        staff = create_staff("hr", "pass", employer.id)
        student = create_student("jane", "pass", "FST", "DCIT", "BSc IT", 3.9)
        position = create_position(employer.id, "Data Analyst", "Analytics", "Data work")
        
        # Add student to shortlist
        staff.addToShortlist(position.id, student.id)
        
        # Employer accepts student
        result = employer.acceptReject(student.id, position.id, "accepted", "Welcome!")
        assert result == True
        
        # Verify status changed
        student_pos = Student_Position.query.filter_by(
            studentID=student.id, 
            positionID=position.id
        ).first()
        assert student_pos is not None
        assert student_pos.status == "accepted"
    
    def test_multiple_students_shortlist(self):
        employer = create_employer("bigcorp", "pass", "BigCorp")
        staff = create_staff("manager", "pass", employer.id)
        position = create_position(employer.id, "Intern", "IT", "General IT work")
        
        # Create multiple students
        student1 = create_student("alice", "pass", "FST", "DCIT", "BSc CS", 3.8)
        student2 = create_student("bob", "pass", "FST", "DCIT", "BSc IT", 3.6)
        student3 = create_student("charlie", "pass", "FST", "DCIT", "BSc CS", 3.9)
        
        # Add all to shortlist
        staff.addToShortlist(position.id, student1.id)
        staff.addToShortlist(position.id, student2.id)
        staff.addToShortlist(position.id, student3.id)
        
        # Verify all added
        shortlist = view_position_shortlist(position.id)
        assert shortlist is not None
        assert len(shortlist) == 3
        
        student_ids = [sp.studentID for sp in shortlist]
        assert student1.id in student_ids
        assert student2.id in student_ids
        assert student3.id in student_ids

if __name__ == "__main__":
    unittest.main()