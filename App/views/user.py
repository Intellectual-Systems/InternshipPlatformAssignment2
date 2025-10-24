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
@jwt_required()
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@user_views.route('/users', methods=['POST'])
@jwt_required()
def create_user_action():
    data = request.form
    flash(f"User {data['username']} created!")
    create_user(data['username'], data['password'])
    return redirect(url_for('user_views.get_user_page'))

@user_views.route('/api/users', methods=['GET'])
@jwt_required()
def get_users_action():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/api/users', methods=['POST'])
@jwt_required()
def create_user_endpoint():
    data = request.json
    user = create_user(data['username'], data['password'])
    return jsonify({'message': f"{user.username} created"} ), 201

@user_views.route('/static/users', methods=['GET'])
@jwt_required()
def static_user_page():
  return send_from_directory('static', 'static-user.html')

@user_views.route('/list', methods=['GET'])
@jwt_required()
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
@jwt_required()
def list_positions():
    positions = get_all_positions()
    return jsonify([pos.get_json() for pos in positions])

@user_views.route('/list-sta', methods=['GET'])
@jwt_required()
def list_staff():
    staff = get_all_staff()
    return jsonify([sta.get_json() for sta in staff])

@user_views.route('/list-std', methods=['GET'])
@jwt_required()
def list_student():
    students = get_all_students()
    return jsonify([stu.get_json() for stu in students])

@user_views.route('/list-sho', methods=['GET'])
@jwt_required()
def list_shortlists():
    shortlists = get_all_student_positions()
    return jsonify([sho.get_json() for sho in shortlists])



# POST methods for creating entries

# Creates an employer using the specified attributes which include name, pass and companyName

@user_views.route('/create-emp', methods=['POST'])
@jwt_required()
def create_employer_action():
    data = request.json
    emp = create_employer(data['username'], data['password'], data['companyName'])
    
    return jsonify({'message': f"Employer {emp.username} created"}), 201

# View positions for a specified employer

@user_views.route('/view-emp-pos', methods=['POST'])
@jwt_required()
def view_employer_positions_action():
    data = request.json
    emp = db.session.query(Employer).filter_by(id=data['employerID']).first()

    if not emp.id:
        return jsonify({'message': f"Employer with id {data['employerID']} not found"}), 404

    positions = view_positions(emp.id)
    return jsonify([pos.get_json() for pos in positions])

# Accepts or rejects a student for a specified position and employer

@user_views.route('/accept-reject', methods=['POST'])
@jwt_required()
def accept_reject_action():
    data = request.json
    emp = db.session.query(Employer).filter_by(id=data['employerID']).first()
    if not emp:
        return jsonify({'message': f"Employer with id {data['employerID']} not found"}), 404

    success = emp.acceptReject(data['studentID'], data['positionID'], data['status'], data.get('message'))
    if success:
        db.session.add(emp)
        db.session.commit()
        return jsonify({'message': f"Student {data['studentID']} has been {data['status']} for position {data['positionID']} by employer {data['employerID']}"}), 200
    else:
        return jsonify({'message': f"Shortlist entry for student {data['studentID']} and position {data['positionID']} not found"}), 404

# Creates a position using the specified attributes which includes the employer's id

@user_views.route('/create-pos', methods=['POST'])
@jwt_required()
def create_position_action():
    data = request.json
    pos = create_position(data['employerID'], data['positionTitle'], data['department'], data['description'])
    return jsonify({'message': f"Position {pos.positionTitle} created"}), 201

# View shortlist for a specified position

@user_views.route('/view-pos-sho', methods=['POST'])
@jwt_required()
def view_position_shortlist_action():
    data = request.json
    pos = db.session.query(InternshipPosition).filter_by(id=data['positionID']).first()

    if not pos:
        return jsonify({'message': f"Position with id {data['positionID']} not found"}), 404

    shortlist = view_position_shortlist(data['positionID'])
    return jsonify([sho.get_json() for sho in shortlist])

# Creates a staff using the specified attributes which includes the employer's id

@user_views.route('/create-sta', methods=['POST'])
@jwt_required()
def create_staff_action():
    data = request.json
    sta = create_staff(data['username'], data['password'], data['employerID'])
    
    return jsonify({'message': f"Staff {sta.username} created"}), 201

# Creates a student using the specified attributes

@user_views.route('/create-std', methods=['POST'])
@jwt_required()
def create_student_action():
    data = request.json
    stu = create_student(data['username'], data['password'], data['faculty'], data['department'], data['degree'], data['gpa'])
    
    return jsonify({'message': f"Student {stu.username} created"}), 201

# Enrolls a student by creates a shortlist(student_position) entry using the specified attributes which includes staff id, position id and student id

@user_views.route('/enroll', methods=['POST'])
@jwt_required()
def enroll_student_action():
    data = request.json
    sta = db.session.query(Staff).filter_by(id=data['staffID']).first()
    sta.addToShortlist(data['positionID'], data['studentID'])
    
    return jsonify({'message': f"Student {data['studentID']} shortlisted for position {data['positionID']} by staff {data['staffID']} successfully"}), 201

# Viwes shortlists for a specified student

@user_views.route('/view-std-sho', methods=['POST'])
@jwt_required()
def view_student_shortlists_action():
    data = request.json
    stu = db.session.query(Student).filter_by(id=data['studentID']).first()

    if not stu:
        return jsonify({'message': f"Student with id {data['studentID']} not found"}), 404

    shortlists = db.session.query(Student_Position).filter_by(studentID=data['studentID']).all()
    return jsonify([sho.get_json() for sho in shortlists])