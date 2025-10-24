from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from.index import index_views

from App.controllers import (
    create_user,
    get_all_users,
    get_all_users_json,
    jwt_required
)
from App.controllers.employer import *
from App.controllers.student import *
from App.controllers.staff import *
from App.controllers.internshipposition import *
from App.controllers.student import *

from App.models.employer import Employer
from App.models.staff import Staff
from App.models.student import Student
from App.models.internshipposition import InternshipPosition
from App.models.student import Student_Position


user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@user_views.route('/users', methods=['POST'])
def create_user_action():
    data = request.form
    flash(f"User {data['username']} created!")
    create_user(data['username'], data['password'])
    return redirect(url_for('user_views.get_user_page'))

@user_views.route('/api/users', methods=['GET'])
def get_users_action():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
    data = request.json
    user = create_user(data['username'], data['password'])
    return jsonify({'message': f"{user.username} created"} ), 201

@user_views.route('/static/users', methods=['GET'])
def static_user_page():
  return send_from_directory('static', 'static-user.html')

@user_views.route('/list', methods=['GET'])
def list_users():
    employers = get_all_employers()
    students = get_all_students()
    staff = get_all_staff()
    users = {
        'employers': [emp.get_json() for emp in employers],
        'staff': [sta.get_json() for sta in staff],
        'students': [stu.get_json() for stu in students]
    }
    return jsonify(users)
    

# Basic routes for listing data

@user_views.route('/list-emp', methods=['GET'])
@jwt_required()
def list_employers():
    employers = get_all_employers()
    return jsonify([emp.get_json() for emp in employers])

@user_views.route('/list-pos', methods=['GET'])
def list_positions():
    positions = get_all_positions()
    return jsonify([pos.get_json() for pos in positions])

@user_views.route('/list-sta', methods=['GET'])
def list_staff():
    staff = get_all_staff()
    return jsonify([sta.get_json() for sta in staff])

@user_views.route('/list-std', methods=['GET'])
def list_student():
    students = get_all_students()
    return jsonify([stu.get_json() for stu in students])

@user_views.route('/list-sho', methods=['GET'])
def list_shortlists():
    shortlists = get_all_student_positions()
    return jsonify([sho.get_json() for sho in shortlists])

# Route for scenario test

@user_views.route('/scenario', methods=['GET'])
def scenario_test():
    emp = create_employer("emp1", "emppass", "Tech Corp")
    db.session.add(emp)
    db.session.commit()

    pos = emp.createPosition("Intern Developer", "IT", "Assist in development tasks")
    db.session.add(pos)
    db.session.commit()

    sta = create_staff("sta1", "stapass", emp.id)
    db.session.add(sta)
    db.session.commit()

    stu = create_student("stu1", "stupass", "FST", "DCIT", "BSc Comp Sci", 3.8)
    db.session.add(stu)
    db.session.commit()

    sta.addToShortlist(pos.id, stu.id)
    db.session.add(stu)
    db.session.add(pos)
    db.session.commit()

    emp.acceptReject(stu.id, pos.id, "Accepted", "Welcome aboard!")
    db.session.add(emp)
    db.session.add(stu)
    db.session.add(pos)
    db.session.commit()

    return jsonify({
        'employer': emp.get_json(),
        'position': pos.get_json(),
        'staff': sta.get_json(),
        'student': stu.get_json(),
        'shortlist': Student_Position.query.filter_by(studentID=stu.id, positionID=pos.id).first().get_json()
    })

# POST methods for creating entries

# Creates an employer using the specified attributes which include name, pass and companyName

@user_views.route('/create-emp', methods=['POST'])
def create_employer_action():
    data = request.json
    emp = create_employer(data['username'], data['password'], data['companyName'])
    
    return jsonify({'message': f"Employer {emp.username} created with id {emp.id}"}), 201

# Creates a position using the specified attributes which includes the employer's id

@user_views.route('/create-pos', methods=['POST'])
def create_position_action():
    data = request.json
    emp = db.session.query(Employer).filter_by(id=data['employerID']).first()
    pos = emp.createPosition(data['positionTitle'], data['department'], data['description'])
    db.session.add(emp)
    db.session.commit()
    return jsonify({'message': f"Position {pos.positionTitle} created with id {pos.id}"}), 201

# Creates a staff using the specified attributes which includes the employer's id

@user_views.route('/create-sta', methods=['POST'])
def create_staff_action():
    data = request.json
    sta = create_staff(data['username'], data['password'], data['employerID'])
    
    return jsonify({'message': f"Staff {sta.username} created with id {sta.id}"}), 201

# Creates a student using the specified attributes

@user_views.route('/create-std', methods=['POST'])
def create_student_action():
    data = request.json
    stu = create_student(data['username'], data['password'], data['faculty'], data['department'], data['degree'], data['gpa'])
    
    return jsonify({'message': f"Student {stu.username} created with id {stu.id}"}), 201

# Enrolls a student by creates a shortlist(student_position) entry using the specified attributes which includes staff id, position id and student id

@user_views.route('/enroll', methods=['POST'])
def enroll_student_action():
    data = request.json
    sta = db.session.query(Staff).filter_by(id=data['staffID']).first()
    sta.addToShortlist(data['positionID'], data['studentID'])
    
    return jsonify({'message': f"Student {data['studentID']} shortlisted for position {data['positionID']} by staff {data['staffID']} successfully"}), 201