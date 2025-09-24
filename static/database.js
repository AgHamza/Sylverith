// Sample Database for Sylverith School Management System

// Sample Admin Users
const adminUsers = [
    {
        id: 1,
        email: "admin@sylverith.com",
        password: "admin123",
        name: "System Administrator",
        role: "super_admin",
        permissions: ["all"],
        lastLogin: null,
        createdAt: "2024-01-01"
    },
    {
        id: 2,
        email: "principal@sylverith.com",
        password: "principal123",
        name: "Dr. Sarah Johnson",
        role: "principal",
        permissions: ["students", "teachers", "classes", "reports"],
        lastLogin: null,
        createdAt: "2024-01-01"
    },
    {
        id: 3,
        email: "registrar@sylverith.com",
        password: "registrar123",
        name: "Michael Chen",
        role: "registrar",
        permissions: ["students", "parents", "classes"],
        lastLogin: null,
        createdAt: "2024-01-01"
    }
];

// Sample Students
const students = [
    {
        id: "ST001",
        name: "John Doe",
        email: "john.doe@student.sylverith.com",
        class: "Grade 5A",
        parentId: "P001",
        phone: "+1 234-567-8901",
        address: "123 Main Street, City, State 12345",
        status: "active",
        enrollmentDate: "2024-01-15",
        dateOfBirth: "2013-05-20"
    },
    {
        id: "ST002",
        name: "Sarah Smith",
        email: "sarah.smith@student.sylverith.com",
        class: "Grade 4B",
        parentId: "P002",
        phone: "+1 234-567-8902",
        address: "456 Oak Avenue, City, State 12345",
        status: "active",
        enrollmentDate: "2024-01-20",
        dateOfBirth: "2014-03-15"
    },
    {
        id: "ST003",
        name: "Michael Johnson",
        email: "michael.johnson@student.sylverith.com",
        class: "Grade 6A",
        parentId: "P003",
        phone: "+1 234-567-8903",
        address: "789 Pine Road, City, State 12345",
        status: "active",
        enrollmentDate: "2024-02-01",
        dateOfBirth: "2012-11-10"
    },
    {
        id: "ST004",
        name: "Emily Davis",
        email: "emily.davis@student.sylverith.com",
        class: "Grade 5B",
        parentId: "P004",
        phone: "+1 234-567-8904",
        address: "321 Elm Street, City, State 12345",
        status: "active",
        enrollmentDate: "2024-02-10",
        dateOfBirth: "2013-08-25"
    },
    {
        id: "ST005",
        name: "David Wilson",
        email: "david.wilson@student.sylverith.com",
        class: "Grade 4A",
        parentId: "P005",
        phone: "+1 234-567-8905",
        address: "654 Maple Lane, City, State 12345",
        status: "active",
        enrollmentDate: "2024-02-15",
        dateOfBirth: "2014-01-12"
    }
];

// Sample Parents
const parents = [
    {
        id: "P001",
        name: "Jane Doe",
        email: "jane.doe@email.com",
        phone: "+1 234-567-8900",
        children: ["ST001"],
        address: "123 Main Street, City, State 12345",
        status: "active",
        registrationDate: "2024-01-15"
    },
    {
        id: "P002",
        name: "Mike Smith",
        email: "mike.smith@email.com",
        phone: "+1 234-567-8901",
        children: ["ST002"],
        address: "456 Oak Avenue, City, State 12345",
        status: "active",
        registrationDate: "2024-01-20"
    },
    {
        id: "P003",
        name: "Lisa Johnson",
        email: "lisa.johnson@email.com",
        phone: "+1 234-567-8902",
        children: ["ST003"],
        address: "789 Pine Road, City, State 12345",
        status: "active",
        registrationDate: "2024-02-01"
    },
    {
        id: "P004",
        name: "Robert Davis",
        email: "robert.davis@email.com",
        phone: "+1 234-567-8903",
        children: ["ST004"],
        address: "321 Elm Street, City, State 12345",
        status: "active",
        registrationDate: "2024-02-10"
    },
    {
        id: "P005",
        name: "Jennifer Wilson",
        email: "jennifer.wilson@email.com",
        phone: "+1 234-567-8904",
        children: ["ST005"],
        address: "654 Maple Lane, City, State 12345",
        status: "active",
        registrationDate: "2024-02-15"
    }
];

// Sample Teachers
const teachers = [
    {
        id: "T001",
        name: "Dr. Emily Johnson",
        email: "emily.johnson@teacher.sylverith.com",
        phone: "+1 234-567-9001",
        subject: "Mathematics",
        classes: ["Grade 5A", "Grade 5B"],
        experience: "8 years",
        qualification: "PhD in Mathematics",
        status: "active",
        hireDate: "2020-08-15"
    },
    {
        id: "T002",
        name: "Mr. James Brown",
        email: "james.brown@teacher.sylverith.com",
        phone: "+1 234-567-9002",
        subject: "English Literature",
        classes: ["Grade 4A", "Grade 4B"],
        experience: "6 years",
        qualification: "Master's in English",
        status: "active",
        hireDate: "2021-01-10"
    },
    {
        id: "T003",
        name: "Ms. Maria Garcia",
        email: "maria.garcia@teacher.sylverith.com",
        phone: "+1 234-567-9003",
        subject: "Science",
        classes: ["Grade 6A", "Grade 6B"],
        experience: "10 years",
        qualification: "Master's in Biology",
        status: "active",
        hireDate: "2019-09-01"
    },
    {
        id: "T004",
        name: "Mr. David Lee",
        email: "david.lee@teacher.sylverith.com",
        phone: "+1 234-567-9004",
        subject: "History",
        classes: ["Grade 5A", "Grade 6A"],
        experience: "5 years",
        qualification: "Master's in History",
        status: "active",
        hireDate: "2022-08-20"
    }
];

// Sample Classes
const classes = [
    {
        id: "C001",
        name: "Grade 5A",
        gradeLevel: "5th Grade",
        teacherId: "T001",
        studentCount: 25,
        maxStudents: 30,
        room: "Room 201",
        schedule: "Monday-Friday, 8:00 AM - 3:00 PM",
        status: "active"
    },
    {
        id: "C002",
        name: "Grade 5B",
        gradeLevel: "5th Grade",
        teacherId: "T001",
        studentCount: 23,
        maxStudents: 30,
        room: "Room 202",
        schedule: "Monday-Friday, 8:00 AM - 3:00 PM",
        status: "active"
    },
    {
        id: "C003",
        name: "Grade 4A",
        gradeLevel: "4th Grade",
        teacherId: "T002",
        studentCount: 28,
        maxStudents: 30,
        room: "Room 101",
        schedule: "Monday-Friday, 8:00 AM - 3:00 PM",
        status: "active"
    },
    {
        id: "C004",
        name: "Grade 4B",
        gradeLevel: "4th Grade",
        teacherId: "T002",
        studentCount: 26,
        maxStudents: 30,
        room: "Room 102",
        schedule: "Monday-Friday, 8:00 AM - 3:00 PM",
        status: "active"
    },
    {
        id: "C005",
        name: "Grade 6A",
        gradeLevel: "6th Grade",
        teacherId: "T003",
        studentCount: 24,
        maxStudents: 30,
        room: "Room 301",
        schedule: "Monday-Friday, 8:00 AM - 3:00 PM",
        status: "active"
    }
];

// Sample Activities/Logs
const activities = [
    {
        id: 1,
        type: "student_registration",
        description: "New student registered: John Doe",
        userId: "admin@sylverith.com",
        timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2 hours ago
        details: { studentId: "ST001", studentName: "John Doe" }
    },
    {
        id: 2,
        type: "parent_update",
        description: "Parent profile updated: Sarah Smith",
        userId: "registrar@sylverith.com",
        timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000), // 4 hours ago
        details: { parentId: "P002", parentName: "Sarah Smith" }
    },
    {
        id: 3,
        type: "class_creation",
        description: "New class created: Grade 5A",
        userId: "principal@sylverith.com",
        timestamp: new Date(Date.now() - 24 * 60 * 60 * 1000), // 1 day ago
        details: { classId: "C001", className: "Grade 5A" }
    },
    {
        id: 4,
        type: "teacher_assignment",
        description: "Teacher assigned to class: Dr. Emily Johnson to Grade 5A",
        userId: "admin@sylverith.com",
        timestamp: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000), // 2 days ago
        details: { teacherId: "T001", teacherName: "Dr. Emily Johnson", classId: "C001" }
    }
];

// Database Functions
class Database {
    constructor() {
        this.adminUsers = [...adminUsers];
        this.students = [...students];
        this.parents = [...parents];
        this.teachers = [...teachers];
        this.classes = [...classes];
        this.activities = [...activities];
    }

    // Authentication
    authenticateUser(email, password) {
        const user = this.adminUsers.find(u => u.email === email && u.password === password);
        if (user) {
            // Update last login
            user.lastLogin = new Date().toISOString();
            return {
                success: true,
                user: {
                    id: user.id,
                    email: user.email,
                    name: user.name,
                    role: user.role,
                    permissions: user.permissions
                }
            };
        }
        return { success: false, message: "Invalid credentials" };
    }

    // Get user by email
    getUserByEmail(email) {
        return this.adminUsers.find(u => u.email === email);
    }

    // Students
    getAllStudents() {
        return this.students;
    }

    getStudentById(id) {
        return this.students.find(s => s.id === id);
    }

    addStudent(studentData) {
        const newStudent = {
            id: `ST${String(this.students.length + 1).padStart(3, '0')}`,
            ...studentData,
            status: "active",
            enrollmentDate: new Date().toISOString().split('T')[0]
        };
        this.students.push(newStudent);
        this.logActivity("student_registration", `New student registered: ${studentData.name}`, { studentId: newStudent.id, studentName: studentData.name });
        return newStudent;
    }

    updateStudent(id, studentData) {
        const index = this.students.findIndex(s => s.id === id);
        if (index !== -1) {
            this.students[index] = { ...this.students[index], ...studentData };
            this.logActivity("student_update", `Student updated: ${studentData.name || this.students[index].name}`, { studentId: id });
            return this.students[index];
        }
        return null;
    }

    deleteStudent(id) {
        const index = this.students.findIndex(s => s.id === id);
        if (index !== -1) {
            const student = this.students[index];
            this.students.splice(index, 1);
            this.logActivity("student_deletion", `Student deleted: ${student.name}`, { studentId: id });
            return true;
        }
        return false;
    }

    // Parents
    getAllParents() {
        return this.parents;
    }

    getParentById(id) {
        return this.parents.find(p => p.id === id);
    }

    addParent(parentData) {
        const newParent = {
            id: `P${String(this.parents.length + 1).padStart(3, '0')}`,
            ...parentData,
            status: "active",
            registrationDate: new Date().toISOString().split('T')[0]
        };
        this.parents.push(newParent);
        this.logActivity("parent_registration", `New parent registered: ${parentData.name}`, { parentId: newParent.id, parentName: parentData.name });
        return newParent;
    }

    updateParent(id, parentData) {
        const index = this.parents.findIndex(p => p.id === id);
        if (index !== -1) {
            this.parents[index] = { ...this.parents[index], ...parentData };
            this.logActivity("parent_update", `Parent updated: ${parentData.name || this.parents[index].name}`, { parentId: id });
            return this.parents[index];
        }
        return null;
    }

    deleteParent(id) {
        const index = this.parents.findIndex(p => p.id === id);
        if (index !== -1) {
            const parent = this.parents[index];
            this.parents.splice(index, 1);
            this.logActivity("parent_deletion", `Parent deleted: ${parent.name}`, { parentId: id });
            return true;
        }
        return false;
    }

    // Teachers
    getAllTeachers() {
        return this.teachers;
    }

    getTeacherById(id) {
        return this.teachers.find(t => t.id === id);
    }

    // Classes
    getAllClasses() {
        return this.classes;
    }

    getClassById(id) {
        return this.classes.find(c => c.id === id);
    }

    // Activities
    getRecentActivities(limit = 10) {
        return this.activities
            .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
            .slice(0, limit);
    }

    logActivity(type, description, details = {}) {
        const activity = {
            id: this.activities.length + 1,
            type,
            description,
            userId: "system",
            timestamp: new Date(),
            details
        };
        this.activities.unshift(activity);
    }

    // Statistics
    getStatistics() {
        return {
            totalStudents: this.students.length,
            totalParents: this.parents.length,
            totalTeachers: this.teachers.length,
            totalClasses: this.classes.length,
            activeStudents: this.students.filter(s => s.status === "active").length,
            activeParents: this.parents.filter(p => p.status === "active").length,
            activeTeachers: this.teachers.filter(t => t.status === "active").length
        };
    }
}

// Create global database instance
window.database = new Database();

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { Database, adminUsers, students, parents, teachers, classes, activities };
}
