from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'sylverith_secret_key_2024'  # Change this in production

# Sample Database (in production, use a real database)
class Database:
    def __init__(self):
        self.admin_users = [
            {
                "id": 1,
                "email": "admin@sylverith.com",
                "password": "admin123",
                "name": "System Administrator",
                "role": "super_admin",
                "permissions": ["all"],
                "lastLogin": None,
                "createdAt": "2024-01-01"
            },
            {
                "id": 2,
                "email": "principal@sylverith.com",
                "password": "principal123",
                "name": "Dr. Sarah Johnson",
                "role": "principal",
                "permissions": ["students", "teachers", "classes", "reports"],
                "lastLogin": None,
                "createdAt": "2024-01-01"
            },
            {
                "id": 3,
                "email": "registrar@sylverith.com",
                "password": "registrar123",
                "name": "Michael Chen",
                "role": "registrar",
                "permissions": ["students", "parents", "classes"],
                "lastLogin": None,
                "createdAt": "2024-01-01"
            }
        ]
        
        self.students = [
            {
                "id": "ST001",
                "name": "John Doe",
                "email": "john.doe@student.sylverith.com",
                "class": "Grade 5A",
                "parentId": "P001",
                "phone": "+1 234-567-8901",
                "address": "123 Main Street, City, State 12345",
                "status": "active",
                "enrollmentDate": "2024-01-15",
                "dateOfBirth": "2013-05-20"
            },
            {
                "id": "ST002",
                "name": "Sarah Smith",
                "email": "sarah.smith@student.sylverith.com",
                "class": "Grade 4B",
                "parentId": "P002",
                "phone": "+1 234-567-8902",
                "address": "456 Oak Avenue, City, State 12345",
                "status": "active",
                "enrollmentDate": "2024-01-20",
                "dateOfBirth": "2014-03-15"
            },
            {
                "id": "ST003",
                "name": "Michael Johnson",
                "email": "michael.johnson@student.sylverith.com",
                "class": "Grade 6A",
                "parentId": "P003",
                "phone": "+1 234-567-8903",
                "address": "789 Pine Road, City, State 12345",
                "status": "active",
                "enrollmentDate": "2024-02-01",
                "dateOfBirth": "2012-11-10"
            },
            {
                "id": "ST004",
                "name": "Emily Davis",
                "email": "emily.davis@student.sylverith.com",
                "class": "Grade 5B",
                "parentId": "P004",
                "phone": "+1 234-567-8904",
                "address": "321 Elm Street, City, State 12345",
                "status": "active",
                "enrollmentDate": "2024-02-10",
                "dateOfBirth": "2013-08-25"
            },
            {
                "id": "ST005",
                "name": "David Wilson",
                "email": "david.wilson@student.sylverith.com",
                "class": "Grade 4A",
                "parentId": "P005",
                "phone": "+1 234-567-8905",
                "address": "654 Maple Lane, City, State 12345",
                "status": "active",
                "enrollmentDate": "2024-02-15",
                "dateOfBirth": "2014-01-12"
            }
        ]
        
        self.parents = [
            {
                "id": "P001",
                "name": "Jane Doe",
                "email": "jane.doe@email.com",
                "phone": "+1 234-567-8900",
                "children": ["ST001"],
                "address": "123 Main Street, City, State 12345",
                "status": "active",
                "registrationDate": "2024-01-15"
            },
            {
                "id": "P002",
                "name": "Mike Smith",
                "email": "mike.smith@email.com",
                "phone": "+1 234-567-8901",
                "children": ["ST002"],
                "address": "456 Oak Avenue, City, State 12345",
                "status": "active",
                "registrationDate": "2024-01-20"
            },
            {
                "id": "P003",
                "name": "Lisa Johnson",
                "email": "lisa.johnson@email.com",
                "phone": "+1 234-567-8902",
                "children": ["ST003"],
                "address": "789 Pine Road, City, State 12345",
                "status": "active",
                "registrationDate": "2024-02-01"
            },
            {
                "id": "P004",
                "name": "Robert Davis",
                "email": "robert.davis@email.com",
                "phone": "+1 234-567-8903",
                "children": ["ST004"],
                "address": "321 Elm Street, City, State 12345",
                "status": "active",
                "registrationDate": "2024-02-10"
            },
            {
                "id": "P005",
                "name": "Jennifer Wilson",
                "email": "jennifer.wilson@email.com",
                "phone": "+1 234-567-8904",
                "children": ["ST005"],
                "address": "654 Maple Lane, City, State 12345",
                "status": "active",
                "registrationDate": "2024-02-15"
            }
        ]
        
        self.assistants = [
            {
                "id": "AS001",
                "name": "Sarah Wilson",
                "email": "sarah.wilson@sylverith.com",
                "role": "admin",
                "department": "Administration",
                "phone": "+1 234-567-8906",
                "permissions": ["students", "teachers", "reports", "settings"],
                "status": "active",
                "createdDate": "2024-01-01"
            },
            {
                "id": "AS002",
                "name": "Michael Brown",
                "email": "michael.brown@sylverith.com",
                "role": "moderator",
                "department": "Student Affairs",
                "phone": "+1 234-567-8907",
                "permissions": ["students", "reports"],
                "status": "active",
                "createdDate": "2024-01-15"
            }
        ]
        
        self.marks = [
            {
                "id": "MK001",
                "studentId": "ST001",
                "studentName": "John Doe",
                "semester": "semester1",
                "arabic": 17,
                "english": 18,
                "math": 16,
                "physics": 18,
                "art": 18,
                "total": 87,
                "average": 17.4,
                "grade": "A",
                "createdDate": "2024-01-15"
            },
            {
                "id": "MK002",
                "studentId": "ST002",
                "studentName": "Sarah Smith",
                "semester": "semester1",
                "arabic": 16,
                "english": 17,
                "math": 18,
                "physics": 16,
                "art": 18,
                "total": 85,
                "average": 17.0,
                "grade": "A",
                "createdDate": "2024-01-15"
            }
        ]
        
        self.teachers = [
            {
                "id": "T001",
                "name": "Dr. Emily Johnson",
                "email": "emily.johnson@teacher.sylverith.com",
                "phone": "+1 234-567-9001",
                "subject": "Mathematics",
                "classes": ["Grade 5A", "Grade 5B"],
                "experience": "8 years",
                "qualification": "PhD in Mathematics",
                "status": "active",
                "hireDate": "2020-08-15"
            },
            {
                "id": "T002",
                "name": "Mr. James Brown",
                "email": "james.brown@teacher.sylverith.com",
                "phone": "+1 234-567-9002",
                "subject": "English Literature",
                "classes": ["Grade 4A", "Grade 4B"],
                "experience": "6 years",
                "qualification": "Master's in English",
                "status": "active",
                "hireDate": "2021-01-10"
            },
            {
                "id": "T003",
                "name": "Ms. Maria Garcia",
                "email": "maria.garcia@teacher.sylverith.com",
                "phone": "+1 234-567-9003",
                "subject": "Science",
                "classes": ["Grade 6A", "Grade 6B"],
                "experience": "10 years",
                "qualification": "Master's in Biology",
                "status": "active",
                "hireDate": "2019-09-01"
            },
            {
                "id": "T004",
                "name": "Mr. David Lee",
                "email": "david.lee@teacher.sylverith.com",
                "phone": "+1 234-567-9004",
                "subject": "History",
                "classes": ["Grade 5A", "Grade 6A"],
                "experience": "5 years",
                "qualification": "Master's in History",
                "status": "active",
                "hireDate": "2022-08-20"
            }
        ]
        
        self.classes = [
            {
                "id": "C001",
                "name": "Grade 5A",
                "gradeLevel": "5th Grade",
                "teacherId": "T001",
                "studentCount": 25,
                "maxStudents": 30,
                "room": "Room 201",
                "schedule": "Monday-Friday, 8:00 AM - 3:00 PM",
                "status": "active"
            },
            {
                "id": "C002",
                "name": "Grade 5B",
                "gradeLevel": "5th Grade",
                "teacherId": "T001",
                "studentCount": 23,
                "maxStudents": 30,
                "room": "Room 202",
                "schedule": "Monday-Friday, 8:00 AM - 3:00 PM",
                "status": "active"
            },
            {
                "id": "C003",
                "name": "Grade 4A",
                "gradeLevel": "4th Grade",
                "teacherId": "T002",
                "studentCount": 28,
                "maxStudents": 30,
                "room": "Room 101",
                "schedule": "Monday-Friday, 8:00 AM - 3:00 PM",
                "status": "active"
            },
            {
                "id": "C004",
                "name": "Grade 4B",
                "gradeLevel": "4th Grade",
                "teacherId": "T002",
                "studentCount": 26,
                "maxStudents": 30,
                "room": "Room 102",
                "schedule": "Monday-Friday, 8:00 AM - 3:00 PM",
                "status": "active"
            },
            {
                "id": "C005",
                "name": "Grade 6A",
                "gradeLevel": "6th Grade",
                "teacherId": "T003",
                "studentCount": 24,
                "maxStudents": 30,
                "room": "Room 301",
                "schedule": "Monday-Friday, 8:00 AM - 3:00 PM",
                "status": "active"
            }
        ]
        
        self.activities = [
            {
                "id": 1,
                "type": "student_registration",
                "description": "New student registered: John Doe",
                "userId": "admin@sylverith.com",
                "timestamp": datetime.now().isoformat(),
                "details": {"studentId": "ST001", "studentName": "John Doe"}
            },
            {
                "id": 2,
                "type": "parent_update",
                "description": "Parent profile updated: Sarah Smith",
                "userId": "registrar@sylverith.com",
                "timestamp": datetime.now().isoformat(),
                "details": {"parentId": "P002", "parentName": "Sarah Smith"}
            },
            {
                "id": 3,
                "type": "class_creation",
                "description": "New class created: Grade 5A",
                "userId": "principal@sylverith.com",
                "timestamp": datetime.now().isoformat(),
                "details": {"classId": "C001", "className": "Grade 5A"}
            }
        ]

    def authenticate_user(self, email, password):
        user = next((u for u in self.admin_users if u["email"] == email and u["password"] == password), None)
        if user:
            user["lastLogin"] = datetime.now().isoformat()
            return {
                "success": True,
                "user": {
                    "id": user["id"],
                    "email": user["email"],
                    "name": user["name"],
                    "role": user["role"],
                    "permissions": user["permissions"]
                }
            }
        return {"success": False, "message": "Invalid credentials"}

    def get_statistics(self):
        # Get unique classes from students
        unique_classes = set()
        for student in self.students:
            if student.get("class"):
                unique_classes.add(student["class"])
        
        # Get unique levels (grades) from classes
        unique_levels = set()
        for class_name in unique_classes:
            if "Grade" in class_name:
                # Extract grade number (e.g., "Grade 5A" -> "5")
                grade_part = class_name.split()[1]
                if grade_part.isdigit():
                    unique_levels.add(int(grade_part))
        
        return {
            "totalStudents": len(self.students),
            "totalParents": len(self.parents),
            "totalTeachers": len(self.teachers),
            "totalClasses": len(unique_classes),
            "totalLevels": len(unique_levels),
            "activeStudents": len([s for s in self.students if s["status"] == "active"]),
            "activeParents": len([p for p in self.parents if p["status"] == "active"]),
            "activeTeachers": len([t for t in self.teachers if t["status"] == "active"])
        }

    def get_recent_activities(self, limit=10):
        return sorted(self.activities, key=lambda x: x["timestamp"], reverse=True)[:limit]

    def add_student(self, student_data):
        new_id = f"ST{len(self.students) + 1:03d}"
        
        # Extract parent data
        parents_data = student_data.pop('parents', {})
        
        # Create student record (remove address if present)
        student_info = {k: v for k, v in student_data.items() if k != 'address'}
        new_student = {
            "id": new_id,
            **student_info,
            "status": "active",
            "enrollmentDate": datetime.now().strftime("%Y-%m-%d")
        }
        
        # Create parent records (if any parents provided)
        parent_ids = []
        if parents_data:
            for parent_type, parent_info in parents_data.items():
                parent_id = f"P{len(self.parents) + 1:03d}"
                new_parent = {
                    "id": parent_id,
                    "name": parent_info["name"],
                    "email": parent_info["email"],
                    "phone": parent_info["phone"],
                    "address": parent_info["address"],
                    "children": [new_id],
                    "status": "active",
                    "registrationDate": datetime.now().strftime("%Y-%m-%d"),
                    "parentType": parent_type
                }
                self.parents.append(new_parent)
                parent_ids.append(parent_id)
        
        # Add parent IDs to student record (empty list if no parents)
        new_student["parentIds"] = parent_ids
        
        self.students.append(new_student)
        self.log_activity("student_registration", f"New student registered: {student_data['name']}", {"studentId": new_id, "studentName": student_data["name"]})
        return new_student
    
    def get_student_by_id(self, student_id):
        for student in self.students:
            if student['id'] == student_id:
                return student
        return None
    
    def get_parents_by_student_id(self, student_id):
        parents = []
        for parent in self.parents:
            if student_id in parent.get('children', []):
                parents.append(parent)
        return parents

    def get_assistants(self):
        return self.assistants
    
    def add_assistant(self, assistant_data):
        new_id = f"AS{len(self.assistants) + 1:03d}"
        new_assistant = {
            "id": new_id,
            "name": assistant_data["name"],
            "email": assistant_data["email"],
            "role": assistant_data["role"],
            "department": assistant_data["department"],
            "phone": assistant_data.get("phone", ""),
            "permissions": assistant_data.get("permissions", []),
            "status": "active",
            "createdDate": datetime.now().strftime("%Y-%m-%d")
        }
        self.assistants.append(new_assistant)
        self.log_activity("assistant_creation", f"New assistant created: {assistant_data['name']}", {"assistantId": new_id, "assistantName": assistant_data["name"]})
        return new_assistant
    
    def get_marks(self, semester=None, class_name=None):
        marks = self.marks
        if semester:
            marks = [m for m in marks if m['semester'] == semester]
        if class_name:
            # Filter by student class
            student_ids = [s['id'] for s in self.students if s['class'] == class_name]
            marks = [m for m in marks if m['studentId'] in student_ids]
        return marks
    
    def add_marks(self, marks_data):
        new_id = f"MK{len(self.marks) + 1:03d}"
        
        # Get student name
        student = next((s for s in self.students if s['id'] == marks_data['studentId']), None)
        student_name = student['name'] if student else 'Unknown Student'
        
        # Calculate total, average, and grade (0-20 scale)
        total = marks_data['arabic'] + marks_data['english'] + marks_data['math'] + marks_data['physics'] + marks_data['art']
        average = total / 5
        
        # Calculate grade based on 0-20 scale
        if average >= 18:
            grade = 'A'
        elif average >= 16:
            grade = 'B'
        elif average >= 14:
            grade = 'C'
        elif average >= 12:
            grade = 'D'
        else:
            grade = 'F'
        
        new_marks = {
            "id": new_id,
            "studentId": marks_data['studentId'],
            "studentName": student_name,
            "semester": marks_data['semester'],
            "arabic": marks_data['arabic'],
            "english": marks_data['english'],
            "math": marks_data['math'],
            "physics": marks_data['physics'],
            "art": marks_data['art'],
            "total": total,
            "average": round(average, 1),
            "grade": grade,
            "createdDate": datetime.now().strftime("%Y-%m-%d")
        }
        
        self.marks.append(new_marks)
        self.log_activity("marks_entry", f"Marks entered for student: {student_name}", {"marksId": new_id, "studentId": marks_data['studentId'], "semester": marks_data['semester']})
        return new_marks
    
    def add_teacher(self, teacher_data):
        new_id = f"T{len(self.teachers) + 1:03d}"
        new_teacher = {
            "id": new_id,
            "name": teacher_data["name"],
            "email": teacher_data["email"],
            "phone": teacher_data.get("phone", ""),
            "subject": teacher_data["subject"],
            "classes": teacher_data["classes"],
            "status": "active",
            "hireDate": datetime.now().strftime("%Y-%m-%d")
        }
        self.teachers.append(new_teacher)
        self.log_activity("teacher_creation", f"New teacher created: {teacher_data['name']}", {"teacherId": new_id, "teacherName": teacher_data["name"]})
        return new_teacher
    
    def get_teacher_by_id(self, teacher_id):
        for teacher in self.teachers:
            if teacher['id'] == teacher_id:
                return teacher
        return None
    
    def update_teacher(self, teacher_id, teacher_data):
        teacher = self.get_teacher_by_id(teacher_id)
        if not teacher:
            return None
        
        # Update teacher data
        teacher.update({
            "name": teacher_data["name"],
            "email": teacher_data["email"],
            "phone": teacher_data.get("phone", ""),
            "subject": teacher_data["subject"],
            "classes": teacher_data["classes"]
        })
        
        self.log_activity("teacher_update", f"Teacher updated: {teacher_data['name']}", {"teacherId": teacher_id, "teacherName": teacher_data["name"]})
        return teacher
    
    def get_contact_recipients(self, audience_type, class_filter=None, grade_filter=None):
        """Get list of recipients for contact emails"""
        recipients = []
        
        if audience_type == "students":
            for student in self.students:
                # Apply filters
                if class_filter and student.get("class") != class_filter:
                    continue
                if grade_filter and not student.get("class", "").startswith(f"Grade {grade_filter}"):
                    continue
                
                recipients.append({
                    "id": student["id"],
                    "name": student["name"],
                    "email": student.get("email", ""),
                    "class": student.get("class", ""),
                    "type": "student"
                })
        
        elif audience_type == "parents":
            for student in self.students:
                # Apply filters
                if class_filter and student.get("class") != class_filter:
                    continue
                if grade_filter and not student.get("class", "").startswith(f"Grade {grade_filter}"):
                    continue
                
                # Get parents for this student
                student_parents = self.get_parents_by_student_id(student["id"])
                for parent in student_parents:
                    recipients.append({
                        "id": parent["id"],
                        "name": parent["name"],
                        "email": parent.get("email", ""),
                        "student_name": student["name"],
                        "student_class": student.get("class", ""),
                        "type": "parent"
                    })
        
        return recipients
    
    def send_contact_email(self, email_data):
        """Simulate sending contact emails"""
        recipients = self.get_contact_recipients(
            email_data["audienceType"],
            email_data.get("classFilter"),
            email_data.get("gradeFilter")
        )
        
        # In a real application, this would integrate with an email service
        # For demo purposes, we'll just log the emails
        for recipient in recipients:
            # Replace variables in subject and message
            subject = email_data["subject"]
            message = email_data["message"]
            
            if recipient["type"] == "student":
                subject = subject.replace("{student}", recipient["name"])
                subject = subject.replace("{parent}", recipient["name"])
                message = message.replace("{student}", recipient["name"])
                message = message.replace("{parent}", recipient["name"])
                message = message.replace("{class}", recipient["class"])
            else:  # parent
                subject = subject.replace("{student}", recipient["student_name"])
                subject = subject.replace("{parent}", recipient["name"])
                message = message.replace("{student}", recipient["student_name"])
                message = message.replace("{parent}", recipient["name"])
                message = message.replace("{class}", recipient["student_class"])
            
            message = message.replace("{school}", "Sylverith School")
            
            # Log the email (in real app, this would send actual emails)
            print(f"Email sent to {recipient['email']}: {subject}")
        
        return {
            "success": True,
            "recipientCount": len(recipients),
            "message": f"Emails sent to {len(recipients)} recipients"
        }

    def add_parent(self, parent_data):
        new_id = f"P{len(self.parents) + 1:03d}"
        new_parent = {
            "id": new_id,
            **parent_data,
            "status": "active",
            "registrationDate": datetime.now().strftime("%Y-%m-%d")
        }
        self.parents.append(new_parent)
        self.log_activity("parent_registration", f"New parent registered: {parent_data['name']}", {"parentId": new_id, "parentName": parent_data["name"]})
        return new_parent

    def delete_student(self, student_id):
        student = next((s for s in self.students if s["id"] == student_id), None)
        if student:
            self.students = [s for s in self.students if s["id"] != student_id]
            self.log_activity("student_deletion", f"Student deleted: {student['name']}", {"studentId": student_id})
            return True
        return False

    def delete_parent(self, parent_id):
        parent = next((p for p in self.parents if p["id"] == parent_id), None)
        if parent:
            self.parents = [p for p in self.parents if p["id"] != parent_id]
            self.log_activity("parent_deletion", f"Parent deleted: {parent['name']}", {"parentId": parent_id})
            return True
        return False

    def log_activity(self, activity_type, description, details=None):
        activity = {
            "id": len(self.activities) + 1,
            "type": activity_type,
            "description": description,
            "userId": session.get("user", {}).get("email", "system"),
            "timestamp": datetime.now().isoformat(),
            "details": details or {}
        }
        self.activities.insert(0, activity)

# Initialize database
db = Database()

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('index.html')

@app.route('/admin')
def admin():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('admin.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    result = db.authenticate_user(email, password)
    if result['success']:
        session['user'] = result['user']
        return jsonify(result)
    else:
        return jsonify(result), 401

@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.pop('user', None)
    return jsonify({'success': True})

@app.route('/api/dashboard/stats')
def api_dashboard_stats():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    return jsonify(db.get_statistics())

@app.route('/api/dashboard/activities')
def api_dashboard_activities():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    limit = request.args.get('limit', 10, type=int)
    return jsonify(db.get_recent_activities(limit))

@app.route('/api/students', methods=['GET', 'POST'])
def api_students():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request.method == 'GET':
        return jsonify(db.students)
    elif request.method == 'POST':
        data = request.get_json()
        new_student = db.add_student(data)
        return jsonify(new_student), 201

@app.route('/api/students/<student_id>', methods=['GET', 'DELETE'])
def api_student_details(student_id):
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request.method == 'GET':
        student = db.get_student_by_id(student_id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        # Get parents for this student
        parents = db.get_parents_by_student_id(student_id)
        student['parents'] = parents
        
        return jsonify(student)
    
    elif request.method == 'DELETE':
        success = db.delete_student(student_id)
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Student not found'}), 404

@app.route('/api/parents', methods=['GET', 'POST'])
def api_parents():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request.method == 'GET':
        return jsonify(db.parents)
    elif request.method == 'POST':
        data = request.get_json()
        new_parent = db.add_parent(data)
        return jsonify(new_parent), 201

@app.route('/api/parents/<parent_id>', methods=['DELETE'])
def api_delete_parent(parent_id):
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    success = db.delete_parent(parent_id)
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Parent not found'}), 404

@app.route('/api/teachers', methods=['GET', 'POST'])
def api_teachers():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request.method == 'GET':
        return jsonify(db.teachers)
    elif request.method == 'POST':
        data = request.get_json()
        new_teacher = db.add_teacher(data)
        return jsonify(new_teacher), 201

@app.route('/api/teachers/<teacher_id>', methods=['GET', 'PUT', 'DELETE'])
def api_teacher_details(teacher_id):
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request.method == 'GET':
        teacher = db.get_teacher_by_id(teacher_id)
        if not teacher:
            return jsonify({'error': 'Teacher not found'}), 404
        return jsonify(teacher)
    
    elif request.method == 'PUT':
        data = request.get_json()
        updated_teacher = db.update_teacher(teacher_id, data)
        if not updated_teacher:
            return jsonify({'error': 'Teacher not found'}), 404
        return jsonify(updated_teacher)
    
    elif request.method == 'DELETE':
        # TODO: Implement delete teacher functionality
        return jsonify({'error': 'Delete functionality not implemented'}), 501

@app.route('/api/contact/send', methods=['POST'])
def api_contact_send():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    
    # Validate required fields
    if not data.get('subject') or not data.get('message'):
        return jsonify({'error': 'Subject and message are required'}), 400
    
    if not data.get('audienceType'):
        return jsonify({'error': 'Audience type is required'}), 400
    
    try:
        result = db.send_contact_email(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/assistants', methods=['GET', 'POST'])
def api_assistants():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request.method == 'GET':
        return jsonify(db.assistants)
    elif request.method == 'POST':
        data = request.get_json()
        new_assistant = db.add_assistant(data)
        return jsonify(new_assistant), 201

@app.route('/api/marks', methods=['GET', 'POST'])
def api_marks():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request.method == 'GET':
        semester = request.args.get('semester')
        class_name = request.args.get('class')
        marks = db.get_marks(semester, class_name)
        return jsonify(marks)
    elif request.method == 'POST':
        data = request.get_json()
        new_marks = db.add_marks(data)
        return jsonify(new_marks), 201

@app.route('/api/classes')
def api_classes():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    return jsonify(db.classes)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
