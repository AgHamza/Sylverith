from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'sylverith_secret_key_2024'  # Change this in production

# Configure file upload
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
                "id": 999,
                "email": "test@example.com",
                "password": "test123",
                "name": "Test User",
                "role": "teacher",
                "permissions": ["students", "marks", "reports"],
                "lastLogin": None,
                "createdAt": "2024-01-15"
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
            },
            {
                "id": 4,
                "email": "emily.johnson@teacher.sylverith.com",
                "password": "prof123",
                "name": "Dr. Emily Johnson",
                "role": "teacher",
                "permissions": ["students", "marks", "reports", "assignments"],
                "lastLogin": None,
                "createdAt": "2024-12-01",
                "teacherId": "T001"
            },
            {
                "id": 5,
                "email": "john.doe@student.sylverith.com",
                "password": "student123",
                "name": "John Doe",
                "role": "student",
                "permissions": ["assignments", "schedule"],
                "lastLogin": None,
                "createdAt": "2024-12-01",
                "studentId": "ST001"
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
        
        # Assignment Management Data
        self.assignments = [
            {
                "id": "ASG001",
                "title": "Math Homework - Chapter 5",
                "description": "Complete exercises 1-20 from chapter 5. Show all work and submit by Friday.",
                "teacherId": "T001",
                "teacherName": "Dr. Emily Johnson",
                "classId": "C001",
                "className": "Grade 5A",
                "subject": "Mathematics",
                "dueDate": "2024-12-20",
                "createdDate": "2024-12-15",
                "attachments": ["math_chapter5.pdf"],
                "status": "active"
            },
            {
                "id": "ASG002",
                "title": "English Essay - My Favorite Book",
                "description": "Write a 500-word essay about your favorite book. Include introduction, body paragraphs, and conclusion.",
                "teacherId": "T002",
                "teacherName": "Mr. James Brown",
                "classId": "C003",
                "className": "Grade 4A",
                "subject": "English Literature",
                "dueDate": "2024-12-22",
                "createdDate": "2024-12-16",
                "attachments": ["essay_guidelines.pdf"],
                "status": "active"
            },
            {
                "id": "ASG003",
                "title": "Physics Lab Report - Motion",
                "description": "Complete the motion experiment and write a detailed lab report including hypothesis, procedure, data analysis, and conclusions.",
                "teacherId": "T001",
                "teacherName": "Dr. Emily Johnson",
                "classId": "C001",
                "className": "Grade 5A",
                "subject": "Physics",
                "dueDate": "2024-12-18",
                "createdDate": "2024-12-10",
                "attachments": ["lab_instructions.pdf", "data_sheet.xlsx"],
                "status": "active"
            },
            {
                "id": "ASG004",
                "title": "Arabic Poetry Analysis",
                "description": "Analyze the poem 'Al-Qasida' and write a 500-word analysis focusing on themes, literary devices, and cultural significance.",
                "teacherId": "T003",
                "teacherName": "Dr. Ahmed Hassan",
                "classId": "C002",
                "className": "Grade 4A",
                "subject": "Arabic",
                "dueDate": "2024-12-25",
                "createdDate": "2024-12-12",
                "attachments": ["poem_text.pdf", "analysis_guide.docx"],
                "status": "active"
            },
            {
                "id": "ASG005",
                "title": "French Creative Writing",
                "description": "Write a short story (300-400 words) in French using the prompt: 'Une lettre mystérieuse arrive à votre porte.' Focus on character development and plot structure.",
                "teacherId": "T002",
                "teacherName": "Mr. James Brown",
                "classId": "C003",
                "className": "Grade 4A",
                "subject": "French",
                "dueDate": "2024-12-28",
                "createdDate": "2024-12-14",
                "attachments": ["writing_prompts.pdf", "rubric.docx"],
                "status": "active"
            },
            {
                "id": "ASG006",
                "title": "Math Problem Solving",
                "description": "Solve the advanced algebra problems from worksheet 3. Show step-by-step solutions and explain your reasoning for each problem.",
                "teacherId": "T001",
                "teacherName": "Dr. Emily Johnson",
                "classId": "C001",
                "className": "Grade 5A",
                "subject": "Mathematics",
                "dueDate": "2024-12-15",
                "createdDate": "2024-12-08",
                "attachments": ["worksheet3.pdf", "solution_template.docx"],
                "status": "expired"
            },
            {
                "id": "ASG007",
                "title": "Physics Homework - Forces",
                "description": "Complete problems 1-15 from the forces chapter. Include free-body diagrams and explain the physics concepts involved.",
                "teacherId": "T001",
                "teacherName": "Dr. Emily Johnson",
                "classId": "C001",
                "className": "Grade 5A",
                "subject": "Physics",
                "dueDate": "2024-12-16",
                "createdDate": "2024-12-09",
                "attachments": ["forces_problems.pdf"],
                "status": "expired"
            },
            {
                "id": "ASG008",
                "title": "Arabic Grammar Exercise",
                "description": "Complete the grammar exercises on verb conjugation and sentence structure. Practice writing sentences using the new grammar rules.",
                "teacherId": "T003",
                "teacherName": "Dr. Ahmed Hassan",
                "classId": "C002",
                "className": "Grade 4A",
                "subject": "Arabic",
                "dueDate": "2024-12-19",
                "createdDate": "2024-12-11",
                "attachments": ["grammar_exercises.pdf", "conjugation_table.pdf"],
                "status": "active"
            },
            {
                "id": "ASG009",
                "title": "English Vocabulary Quiz",
                "description": "Study the vocabulary list for Unit 3 and prepare for an oral presentation. Practice pronunciation and usage in sentences.",
                "teacherId": "T002",
                "teacherName": "Mr. James Brown",
                "classId": "C003",
                "className": "Grade 4A",
                "subject": "English Literature",
                "dueDate": "2024-12-17",
                "createdDate": "2024-12-13",
                "attachments": ["vocab_list.pdf", "pronunciation_guide.mp3"],
                "status": "draft"
            }
        ]
        
        self.assignment_submissions = [
            {
                "id": "SUB001",
                "assignmentId": "ASG001",
                "studentId": "ST001",
                "studentName": "John Doe",
                "submissionText": "I completed all the exercises. Here are my answers...",
                "attachments": ["john_math_homework.pdf"],
                "submittedDate": "2024-12-18",
                "status": "submitted",
                "grade": None,
                "feedback": None
            }
        ]
        
        self.class_schedules = [
            # Grade 5A Schedule
            {
                "id": "SCH001",
                "classId": "C001",
                "className": "Grade 5A",
                "teacherId": "T001",
                "teacherName": "Dr. Emily Johnson",
                "subject": "Mathematics",
                "day": "Monday",
                "startTime": "09:00",
                "endTime": "10:00",
                "room": "Room 201"
            },
            {
                "id": "SCH002",
                "classId": "C001",
                "className": "Grade 5A",
                "teacherId": "T004",
                "teacherName": "Mr. David Lee",
                "subject": "History",
                "day": "Monday",
                "startTime": "10:30",
                "endTime": "11:30",
                "room": "Room 201"
            },
            {
                "id": "SCH003",
                "classId": "C001",
                "className": "Grade 5A",
                "teacherId": "T001",
                "teacherName": "Dr. Emily Johnson",
                "subject": "Mathematics",
                "day": "Wednesday",
                "startTime": "09:00",
                "endTime": "10:00",
                "room": "Room 201"
            },
            {
                "id": "SCH004",
                "classId": "C001",
                "className": "Grade 5A",
                "teacherId": "T003",
                "teacherName": "Ms. Maria Garcia",
                "subject": "Science",
                "day": "Wednesday",
                "startTime": "10:30",
                "endTime": "11:30",
                "room": "Room 301"
            },
            {
                "id": "SCH005",
                "classId": "C001",
                "className": "Grade 5A",
                "teacherId": "T002",
                "teacherName": "Mr. James Brown",
                "subject": "English Literature",
                "day": "Friday",
                "startTime": "09:00",
                "endTime": "10:00",
                "room": "Room 101"
            },
            # Grade 4A Schedule
            {
                "id": "SCH006",
                "classId": "C003",
                "className": "Grade 4A",
                "teacherId": "T002",
                "teacherName": "Mr. James Brown",
                "subject": "English Literature",
                "day": "Tuesday",
                "startTime": "09:00",
                "endTime": "10:00",
                "room": "Room 101"
            },
            {
                "id": "SCH007",
                "classId": "C003",
                "className": "Grade 4A",
                "teacherId": "T001",
                "teacherName": "Dr. Emily Johnson",
                "subject": "Mathematics",
                "day": "Tuesday",
                "startTime": "10:30",
                "endTime": "11:30",
                "room": "Room 201"
            },
            {
                "id": "SCH008",
                "classId": "C003",
                "className": "Grade 4A",
                "teacherId": "T003",
                "teacherName": "Ms. Maria Garcia",
                "subject": "Science",
                "day": "Thursday",
                "startTime": "09:00",
                "endTime": "10:00",
                "room": "Room 301"
            },
            {
                "id": "SCH009",
                "classId": "C003",
                "className": "Grade 4A",
                "teacherId": "T004",
                "teacherName": "Mr. David Lee",
                "subject": "History",
                "day": "Thursday",
                "startTime": "10:30",
                "endTime": "11:30",
                "room": "Room 201"
            },
            {
                "id": "SCH010",
                "classId": "C003",
                "className": "Grade 4A",
                "teacherId": "T002",
                "teacherName": "Mr. James Brown",
                "subject": "English Literature",
                "day": "Friday",
                "startTime": "10:30",
                "endTime": "11:30",
                "room": "Room 101"
            }
        ]
        
        # Individual marks for assignments and tests
        self.individual_marks = [
            # Math marks
            {
                "id": 1,
                "student_id": "ST001",
                "subject": "Math",
                "description": "Chapter 5 Quiz",
                "value": 18,
                "max_value": 20,
                "date": "2024-01-15",
                "teacher_name": "Emily Johnson"
            },
            {
                "id": 2,
                "student_id": "ST001",
                "subject": "Math",
                "description": "Homework Assignment",
                "value": 16,
                "max_value": 20,
                "date": "2024-01-18",
                "teacher_name": "Emily Johnson"
            },
            {
                "id": 3,
                "student_id": "ST001",
                "subject": "Math",
                "description": "Midterm Exam",
                "value": 17,
                "max_value": 20,
                "date": "2024-01-25",
                "teacher_name": "Emily Johnson"
            },
            {
                "id": 4,
                "student_id": "ST001",
                "subject": "Math",
                "description": "Problem Solving Test",
                "value": 19,
                "max_value": 20,
                "date": "2024-02-01",
                "teacher_name": "Emily Johnson"
            },
            # French marks
            {
                "id": 5,
                "student_id": "ST001",
                "subject": "French",
                "description": "Vocabulary Test",
                "value": 15,
                "max_value": 20,
                "date": "2024-01-16",
                "teacher_name": "Emily Johnson"
            },
            {
                "id": 6,
                "student_id": "ST001",
                "subject": "French",
                "description": "Oral Presentation",
                "value": 17,
                "max_value": 20,
                "date": "2024-01-20",
                "teacher_name": "Emily Johnson"
            },
            {
                "id": 7,
                "student_id": "ST001",
                "subject": "French",
                "description": "Grammar Exercise",
                "value": 14,
                "max_value": 20,
                "date": "2024-01-28",
                "teacher_name": "Emily Johnson"
            },
            {
                "id": 8,
                "student_id": "ST001",
                "subject": "French",
                "description": "Writing Assignment",
                "value": 16,
                "max_value": 20,
                "date": "2024-02-05",
                "teacher_name": "Emily Johnson"
            },
            # English marks
            {
                "id": 9,
                "student_id": "ST001",
                "subject": "English",
                "description": "Reading Comprehension",
                "value": 14,
                "max_value": 20,
                "date": "2024-01-17",
                "teacher_name": "Sarah Wilson"
            },
            {
                "id": 10,
                "student_id": "ST001",
                "subject": "English",
                "description": "Essay Writing",
                "value": 15,
                "max_value": 20,
                "date": "2024-01-24",
                "teacher_name": "Sarah Wilson"
            },
            {
                "id": 11,
                "student_id": "ST001",
                "subject": "English",
                "description": "Literature Analysis",
                "value": 13,
                "max_value": 20,
                "date": "2024-01-31",
                "teacher_name": "Sarah Wilson"
            },
            # Physics marks
            {
                "id": 12,
                "student_id": "ST001",
                "subject": "Physics",
                "description": "Lab Report",
                "value": 19,
                "max_value": 20,
                "date": "2024-01-19",
                "teacher_name": "Michael Brown"
            },
            {
                "id": 13,
                "student_id": "ST001",
                "subject": "Physics",
                "description": "Theory Test",
                "value": 18,
                "max_value": 20,
                "date": "2024-01-26",
                "teacher_name": "Michael Brown"
            },
            {
                "id": 14,
                "student_id": "ST001",
                "subject": "Physics",
                "description": "Practical Exam",
                "value": 17,
                "max_value": 20,
                "date": "2024-02-02",
                "teacher_name": "Michael Brown"
            },
            # Arabic marks
            {
                "id": 15,
                "student_id": "ST001",
                "subject": "Arabic",
                "description": "Grammar Test",
                "value": 13,
                "max_value": 20,
                "date": "2024-01-14",
                "teacher_name": "Ahmed Hassan"
            },
            {
                "id": 16,
                "student_id": "ST001",
                "subject": "Arabic",
                "description": "Reading Test",
                "value": 12,
                "max_value": 20,
                "date": "2024-01-21",
                "teacher_name": "Ahmed Hassan"
            },
            {
                "id": 17,
                "student_id": "ST001",
                "subject": "Arabic",
                "description": "Writing Exercise",
                "value": 14,
                "max_value": 20,
                "date": "2024-01-29",
                "teacher_name": "Ahmed Hassan"
            }
        ]

    def authenticate_user(self, email, password):
        user = next((u for u in self.admin_users if u["email"] == email and u["password"] == password), None)
        if user:
            # Check if this is a first-time login (no previous login recorded)
            is_first_login = user.get("lastLogin") is None
            
            user["lastLogin"] = datetime.now().isoformat()
            
            return {
                "success": True,
                "user": {
                    "id": user["id"],
                    "email": user["email"],
                    "name": user["name"],
                    "role": user["role"],
                    "permissions": user["permissions"]
                },
                "is_first_login": is_first_login
            }
        return {"success": False, "message": "Invalid credentials"}

    def get_permissions_for_role(self, role):
        """Get permissions based on user role"""
        role_permissions = {
            "super_admin": ["all"],
            "principal": ["students", "teachers", "classes", "reports"],
            "registrar": ["students", "parents", "classes"],
            "teacher": ["students", "marks", "reports"],
            "assistant": ["students", "reports"]
        }
        return role_permissions.get(role, [])

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
    
    # Assignment Management Methods
    def get_assignments_by_teacher(self, teacher_id):
        return [a for a in self.assignments if a["teacherId"] == teacher_id and a["status"] == "active"]
    
    def get_assignments_by_student(self, student_id):
        # Get student's class
        student = next((s for s in self.students if s["id"] == student_id), None)
        if not student:
            return []
        
        student_class = student.get("class")
        if not student_class:
            return []
        
        # Get assignments for student's class
        class_assignments = [a for a in self.assignments if a["className"] == student_class and a["status"] == "active"]
        
        # Add submission status for each assignment
        for assignment in class_assignments:
            submission = next((s for s in self.assignment_submissions 
                             if s["assignmentId"] == assignment["id"] and s["studentId"] == student_id), None)
            assignment["submission"] = submission
            assignment["isSubmitted"] = submission is not None
        
        return class_assignments
    
    def get_class_schedule_by_teacher(self, teacher_id):
        return [s for s in self.class_schedules if s["teacherId"] == teacher_id]
    
    def get_class_schedule_by_student(self, student_id):
        # Get student's class
        student = next((s for s in self.students if s["id"] == student_id), None)
        if not student:
            return []
        
        student_class = student.get("class")
        if not student_class:
            return []
        
        return [s for s in self.class_schedules if s["className"] == student_class]
    
    def create_assignment(self, assignment_data):
        new_id = f"ASG{len(self.assignments) + 1:03d}"
        
        # Get teacher name
        teacher = next((t for t in self.teachers if t["id"] == assignment_data["teacherId"]), None)
        teacher_name = teacher["name"] if teacher else "Unknown Teacher"
        
        # Get class name
        class_info = next((c for c in self.classes if c["id"] == assignment_data["classId"]), None)
        class_name = class_info["name"] if class_info else "Unknown Class"
        
        new_assignment = {
            "id": new_id,
            "title": assignment_data["title"],
            "description": assignment_data["description"],
            "teacherId": assignment_data["teacherId"],
            "teacherName": teacher_name,
            "classId": assignment_data["classId"],
            "className": class_name,
            "subject": assignment_data.get("subject", ""),
            "dueDate": assignment_data["dueDate"],
            "createdDate": datetime.now().strftime("%Y-%m-%d"),
            "attachments": assignment_data.get("attachments", []),
            "allowReply": assignment_data.get("allowReply", True),
            "status": "active"
        }
        
        self.assignments.append(new_assignment)
        self.log_activity("assignment_creation", f"New assignment created: {assignment_data['title']}", 
                         {"assignmentId": new_id, "teacherId": assignment_data["teacherId"]})
        return new_assignment
    
    def submit_assignment(self, submission_data):
        new_id = f"SUB{len(self.assignment_submissions) + 1:03d}"
        
        # Get student name
        student = next((s for s in self.students if s["id"] == submission_data["studentId"]), None)
        student_name = student["name"] if student else "Unknown Student"
        
        new_submission = {
            "id": new_id,
            "assignmentId": submission_data["assignmentId"],
            "studentId": submission_data["studentId"],
            "studentName": student_name,
            "submissionText": submission_data.get("submissionText", ""),
            "attachments": submission_data.get("attachments", []),
            "submittedDate": datetime.now().strftime("%Y-%m-%d"),
            "status": "submitted",
            "grade": None,
            "feedback": None
        }
        
        self.assignment_submissions.append(new_submission)
        self.log_activity("assignment_submission", f"Assignment submitted by: {student_name}", 
                         {"submissionId": new_id, "assignmentId": submission_data["assignmentId"]})
        return new_submission
    
    def get_submissions_by_assignment(self, assignment_id):
        return [s for s in self.assignment_submissions if s["assignmentId"] == assignment_id]
    
    def get_marks_by_student(self, student_id):
        """Get all marks for a specific student"""
        return [mark for mark in self.individual_marks if mark["student_id"] == student_id]

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

@app.route('/email-verification')
def email_verification():
    return render_template('email_verification.html')

@app.route('/password-reset')
def password_reset():
    return render_template('password_reset.html')

@app.route('/user-profile')
def user_profile():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('user_profile.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/professor')
def professor_dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = session['user']
    if user['role'] != 'teacher':
        return redirect(url_for('admin'))
    
    return render_template('professor.html')

@app.route('/student')
def student_dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = session['user']
    if user['role'] != 'student':
        return redirect(url_for('admin'))
    
    return render_template('student.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    result = db.authenticate_user(email, password)
    if result['success']:
        user = result['user']
        
        # Add teacherId or studentId to user session if not present
        if user['role'] == 'teacher' and 'teacherId' not in user:
            # Find teacher by email
            teacher = next((t for t in db.teachers if t['email'] == email), None)
            if teacher:
                user['teacherId'] = teacher['id']
        elif user['role'] == 'student' and 'studentId' not in user:
            # Find student by email
            student = next((s for s in db.students if s['email'] == email), None)
            if student:
                user['studentId'] = student['id']
        
        session['user'] = user
        
        # Add redirect URL based on user role
        if user['role'] == 'teacher':
            result['redirect_url'] = '/professor'
        elif user['role'] == 'student':
            result['redirect_url'] = '/student'
        else:
            result['redirect_url'] = '/admin'
        
        return jsonify(result)
    else:
        return jsonify(result), 401

@app.route('/api/signup', methods=['POST'])
def api_signup():
    data = request.get_json()
    full_name = data.get('fullName')
    email = data.get('email')
    role = data.get('role')
    phone = data.get('phone', '')
    password = data.get('password')
    
    # Check if email already exists
    existing_user = next((u for u in db.admin_users if u["email"] == email), None)
    if existing_user:
        return jsonify({'success': False, 'message': 'Email already exists'}), 400
    
    # Create new user with first-time login flag
    new_user = {
        "id": len(db.admin_users) + 1,
        "email": email,
        "password": password,
        "name": full_name,
        "role": role,
        "permissions": db.get_permissions_for_role(role),
        "lastLogin": None,  # This ensures is_first_login will be True
        "createdAt": datetime.now().strftime("%Y-%m-%d"),
        "phone": phone
    }
    
    db.admin_users.append(new_user)
    
    return jsonify({
        'success': True,
        'message': 'Account created successfully',
        'user': {
            'id': new_user['id'],
            'email': new_user['email'],
            'name': new_user['name'],
            'role': new_user['role']
        }
    })

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
    
    user = session['user']
    
    if request.method == 'GET':
        # Check if this is a student request
        if user['role'] == 'student':
            student_id = user.get('studentId') or next((s['id'] for s in db.students if s['email'] == user['email']), None)
            if not student_id:
                return jsonify({'error': 'Student not found'}), 404
            
            marks = db.get_marks_by_student(student_id)
            return jsonify(marks)
        else:
            # Admin request - get marks by semester and class
            semester = request.args.get('semester')
            class_name = request.args.get('class')
            marks = db.get_marks(semester, class_name)
            return jsonify(marks)
    elif request.method == 'POST':
        # Only admin can add marks
        if user['role'] != 'admin':
            return jsonify({'error': 'Access denied'}), 403
        
        data = request.get_json()
        new_marks = db.add_marks(data)
        return jsonify(new_marks), 201

@app.route('/api/classes')
def api_classes():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    return jsonify(db.classes)

# Assignment Management API Endpoints
@app.route('/api/assignments', methods=['GET', 'POST'])
def api_assignments():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user = session['user']
    
    if request.method == 'GET':
        if user['role'] == 'teacher':
            # Get assignments created by this teacher
            teacher_id = user.get('teacherId') or next((t['id'] for t in db.teachers if t['email'] == user['email']), None)
            if not teacher_id:
                return jsonify({'error': 'Teacher not found'}), 404
            assignments = db.get_assignments_by_teacher(teacher_id)
        elif user['role'] == 'student':
            # Get assignments for this student's class
            student_id = user.get('studentId') or next((s['id'] for s in db.students if s['email'] == user['email']), None)
            if not student_id:
                return jsonify({'error': 'Student not found'}), 404
            assignments = db.get_assignments_by_student(student_id)
        else:
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        return jsonify(assignments)
    
    elif request.method == 'POST':
        if user['role'] != 'teacher':
            return jsonify({'error': 'Only teachers can create assignments'}), 403
        
        data = request.get_json()
        
        # Get teacher ID
        teacher_id = user.get('teacherId') or next((t['id'] for t in db.teachers if t['email'] == user['email']), None)
        if not teacher_id:
            return jsonify({'error': 'Teacher not found'}), 404
        
        data['teacherId'] = teacher_id
        new_assignment = db.create_assignment(data)
        return jsonify(new_assignment), 201

@app.route('/api/assignments/<assignment_id>/submissions', methods=['GET'])
def api_assignment_submissions(assignment_id):
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user = session['user']
    if user['role'] != 'teacher':
        return jsonify({'error': 'Only teachers can view submissions'}), 403
    
    submissions = db.get_submissions_by_assignment(assignment_id)
    return jsonify(submissions)

@app.route('/api/assignments/submit', methods=['POST'])
def api_submit_assignment():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user = session['user']
    if user['role'] != 'student':
        return jsonify({'error': 'Only students can submit assignments'}), 403
    
    # Get student ID
    student_id = user.get('studentId') or next((s['id'] for s in db.students if s['email'] == user['email']), None)
    if not student_id:
        return jsonify({'error': 'Student not found'}), 404
    
    # Handle file uploads
    uploaded_files = []
    if 'files' in request.files:
        files = request.files.getlist('files')
        for file in files:
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to avoid filename conflicts
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
                filename = timestamp + filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                uploaded_files.append(filename)
    
    # Prepare submission data
    submission_data = {
        'assignmentId': request.form.get('assignmentId'),
        'submissionText': request.form.get('submissionText', ''),
        'attachments': uploaded_files
    }
    
    submission_data['studentId'] = student_id
    new_submission = db.submit_assignment(submission_data)
    return jsonify(new_submission), 201

@app.route('/api/schedule', methods=['GET'])
def api_schedule():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user = session['user']
    
    if user['role'] == 'teacher':
        teacher_id = user.get('teacherId') or next((t['id'] for t in db.teachers if t['email'] == user['email']), None)
        if not teacher_id:
            return jsonify({'error': 'Teacher not found'}), 404
        schedule = db.get_class_schedule_by_teacher(teacher_id)
    elif user['role'] == 'student':
        student_id = user.get('studentId') or next((s['id'] for s in db.students if s['email'] == user['email']), None)
        if not student_id:
            return jsonify({'error': 'Student not found'}), 404
        schedule = db.get_class_schedule_by_student(student_id)
    else:
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    return jsonify(schedule)

@app.route('/api/admin/assignments', methods=['GET'])
def api_admin_assignments():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user = session['user']
    
    if user['role'] not in ['admin', 'super_admin']:
        return jsonify({'error': 'Access denied'}), 403
    
    # Return all assignments for admin view
    assignments = []
    for assignment in db.assignments:
        # Convert to admin format
        admin_assignment = {
            "id": assignment["id"],
            "title": assignment["title"],
            "description": assignment["description"],
            "subject": assignment["subject"],
            "className": assignment["className"],
            "teacherName": assignment["teacherName"],
            "dueDate": assignment["dueDate"],
            "createdDate": assignment["createdDate"],
            "attachments": assignment.get("attachments", []),
            "status": assignment.get("status", "active"),
            "allowReply": assignment.get("allowReply", True)
        }
        assignments.append(admin_assignment)
    
    return jsonify(assignments)

@app.route('/api/admin/assignments/<assignment_id>', methods=['DELETE'])
def api_delete_assignment(assignment_id):
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user = session['user']
    
    if user['role'] not in ['admin', 'super_admin']:
        return jsonify({'error': 'Access denied'}), 403
    
    # Find and remove assignment
    assignment_index = None
    for i, assignment in enumerate(db.assignments):
        if assignment["id"] == assignment_id:
            assignment_index = i
            break
    
    if assignment_index is None:
        return jsonify({'error': 'Assignment not found'}), 404
    
    # Remove assignment
    deleted_assignment = db.assignments.pop(assignment_index)
    
    # Log activity
    db.log_activity("assignment_deleted", f"Assignment deleted by admin: {deleted_assignment['title']}", 
                   {"assignmentId": assignment_id, "deletedBy": user['email']})
    
    return jsonify({'message': 'Assignment deleted successfully'})

@app.route('/api/assignments/upload', methods=['POST'])
def api_upload_assignment_files():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user = session['user']
    if user['role'] != 'teacher':
        return jsonify({'error': 'Only teachers can upload files'}), 403
    
    try:
        assignment_title = request.form.get('assignmentTitle')
        files = request.files.getlist('files')
        
        if not files or files[0].filename == '':
            return jsonify({'error': 'No files provided'}), 400
        
        uploaded_files = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Create a unique filename to avoid conflicts
                unique_filename = f"{assignment_title}_{filename}"
                file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
                file.save(file_path)
                uploaded_files.append(unique_filename)
        
        return jsonify({
            'message': f'Successfully uploaded {len(uploaded_files)} files',
            'files': uploaded_files
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
