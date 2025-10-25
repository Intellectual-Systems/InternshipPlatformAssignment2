from App.controllers.employer import create_employer, create_position, acceptReject
from App.controllers.staff import create_staff, addToShortlist
from App.controllers.student import create_student

from App.database import db


def create_scenario():
    emp = create_employer('Satoru Iwata', 'iwatapass', 'Nintendo')
    emp2 = create_employer('Devon Pritchard', 'devpass', 'Nintendo of America')
    emp3 = create_employer('Hidetaka Miyazaki', 'hidepass', 'FromSoftware')
    db.session.add(emp)
    db.session.add(emp2)
    db.session.add(emp3)
    db.session.commit()

    pos1 = create_position(emp.id, 'Software Developer Intern', 'IT', 'Assist in software development tasks')
    pos2 = create_position(emp2.id, 'Game Designer Intern', 'Design', 'Assist in game design tasks')
    pos3 = create_position(emp3.id, 'AI Programmer Intern', 'IT', 'Work on AI programming for games')
    db.session.add(pos1)
    db.session.add(pos2)
    db.session.add(pos3)
    db.session.commit()
    
    sta = create_staff(username='Masahiro Sakurai', password='smashpass', employerID=emp.id)
    sta2 = create_staff(username='Yoshio Sakamoto', password='metropass', employerID=emp.id)
    sta3 = create_staff(username='Yoshiaki Koizumi', password='majorapass', employerID=emp.id)
    sta4 = create_staff(username='Shigeru Miyamoto', password='mariopass', employerID=emp.id)
    db.session.add(sta)
    db.session.add(sta2)
    db.session.add(sta3)
    db.session.add(sta4)
    db.session.commit()

    stu = create_student(username='Naoto Kuroshima', password='streetpass', faculty='FHE', department='DCFA', degree='BSc Visual Arts', gpa=3.8)
    stu2 = create_student(username='Eric Barone', password='stardewpassey', faculty='FST', department='DCIT', degree='BSc Comp Sci', gpa=3.9)
    stu3 = create_student(username='Toby Fox', password='underpass', faculty='FST', department='DCIT', degree='BSc Comp Sci & Management', gpa=3.7)
    stu4 = create_student(username='Milton Guasti', password='m2pass', faculty='FST', department='DCIT', degree='BSc IT', gpa=3.6)
    stu5 = create_student(username='Thomas Grip', password='amnepass', faculty='FHE', department='DCFA', degree='BSc Visual Arts', gpa=3.5)
    db.session.add(stu)
    db.session.add(stu2)
    db.session.add(stu3)
    db.session.add(stu4)
    db.session.add(stu5)
    db.session.commit()

    addToShortlist(sta.id, pos1.id, stu.id)
    addToShortlist(sta2.id, pos2.id, stu.id)
    db.session.add(sta)
    db.session.commit()

    acceptReject(emp.id, stu.id, pos1.id, 'accepted', 'Welcome to the team!')
    acceptReject(emp2.id, stu.id, pos2.id, 'rejected', 'We regret to inform you...')
    db.session.add(emp)
    db.session.commit()

