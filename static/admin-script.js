// Admin Dashboard JavaScript

// Authentication Check
function checkAuthentication() {
    // Check if user is authenticated via Flask session
    fetch('/api/dashboard/stats')
        .then(response => {
            if (!response.ok) {
                showNotification('Please login to access the admin panel', 'error');
                setTimeout(() => {
                    window.location.href = '/login';
                }, 2000);
                return false;
            }
            return true;
        })
        .catch(error => {
            showNotification('Please login to access the admin panel', 'error');
            setTimeout(() => {
                window.location.href = '/login';
            }, 2000);
            return false;
        });
}

// Initialize dashboard with authentication
document.addEventListener('DOMContentLoaded', function() {
    const currentUser = checkAuthentication();
    if (!currentUser) return;
    
    // Update user info in navbar
    const userInfoElement = document.querySelector('.admin-user-info span');
    if (userInfoElement) {
        userInfoElement.textContent = currentUser.name;
    }
    
    // Load dashboard data
    loadDashboardData();
    
    // Initialize contact section
    initializeContactSection();
    
    // Set default active section
    showSection('dashboard');
    
    // Add loading animation to stats
    const statNumbers = document.querySelectorAll('.stat-content h3');
    statNumbers.forEach(stat => {
        const finalValue = stat.textContent;
        stat.textContent = '0';
        
        setTimeout(() => {
            animateNumber(stat, 0, parseInt(finalValue.replace(/,/g, '')), 1000);
        }, 500);
    });
});

// Load dashboard data from Flask API
function loadDashboardData() {
    // Load statistics
    fetch('/api/dashboard/stats')
        .then(response => response.json())
        .then(stats => {
            updateStatistics(stats);
        })
        .catch(error => console.error('Error loading stats:', error));
    
    // Load activities
    fetch('/api/dashboard/activities?limit=5')
        .then(response => response.json())
        .then(activities => {
            updateActivities(activities);
        })
        .catch(error => console.error('Error loading activities:', error));
    
    // Load table data
    loadTableData();
}

// Update statistics display
function updateStatistics(stats) {
    const statCards = document.querySelectorAll('.stat-card');
    const statValues = [
        stats.totalStudents,
        stats.totalTeachers,
        stats.totalClasses,
        stats.totalLevels
    ];
    
    statCards.forEach((card, index) => {
        const h3 = card.querySelector('h3');
        if (h3 && statValues[index] !== undefined) {
            h3.textContent = statValues[index].toLocaleString();
        }
    });
}

// Update activities display
function updateActivities(activities) {
    const activityList = document.querySelector('.activity-list');
    if (!activityList) return;
    
    activityList.innerHTML = '';
    
    activities.forEach(activity => {
        const activityItem = document.createElement('div');
        activityItem.className = 'activity-item';
        
        const icon = getActivityIcon(activity.type);
        const timeAgo = getTimeAgo(activity.timestamp);
        
        activityItem.innerHTML = `
            <i class="fas ${icon}"></i>
            <div>
                <p>${activity.description}</p>
                <span>${timeAgo}</span>
            </div>
        `;
        
        activityList.appendChild(activityItem);
    });
}

// Get activity icon based on type
function getActivityIcon(type) {
    const icons = {
        'student_registration': 'fa-user-plus',
        'student_update': 'fa-user-edit',
        'student_deletion': 'fa-user-minus',
        'parent_registration': 'fa-user-friends',
        'parent_update': 'fa-user-edit',
        'parent_deletion': 'fa-user-minus',
        'class_creation': 'fa-graduation-cap',
        'teacher_assignment': 'fa-chalkboard-teacher'
    };
    return icons[type] || 'fa-info-circle';
}

// Get time ago string
function getTimeAgo(timestamp) {
    const now = new Date();
    const time = new Date(timestamp);
    const diffInSeconds = Math.floor((now - time) / 1000);
    
    if (diffInSeconds < 60) return 'Just now';
    if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)} minutes ago`;
    if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)} hours ago`;
    return `${Math.floor(diffInSeconds / 86400)} days ago`;
}

// Load table data
function loadTableData() {
    loadStudentsTable();
    loadTeachersTable();
    loadAssistantsTable();
}

// Load students table
function loadStudentsTable() {
    fetch('/api/students')
        .then(response => response.json())
        .then(students => {
            const tbody = document.querySelector('#students-section .data-table tbody');
            if (!tbody) return;
            
            tbody.innerHTML = '';
            
            students.forEach(student => {
                const row = document.createElement('tr');
                row.style.cursor = 'pointer';
                row.onclick = () => openStudentDetailsModal(student.id);
                row.innerHTML = `
                    <td>${student.id}</td>
                    <td>${student.name}</td>
                    <td>${student.class}</td>
                    <td>${student.email || 'N/A'}</td>
                    <td>${student.phone || 'N/A'}</td>
                    <td><span class="status-badge active">${student.status}</span></td>
                    <td>
                        <button class="action-btn edit" onclick="event.stopPropagation(); editStudent('${student.id}')">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="action-btn delete" onclick="event.stopPropagation(); deleteStudent('${student.id}')">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        })
        .catch(error => console.error('Error loading students:', error));
}

// Load assistants table
function loadAssistantsTable() {
    fetch('/api/assistants')
        .then(response => response.json())
        .then(assistants => {
            const tbody = document.querySelector('#assistants-section .data-table tbody');
            if (!tbody) return;
            
            tbody.innerHTML = '';
            
            assistants.forEach(assistant => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${assistant.id}</td>
                    <td>${assistant.name}</td>
                    <td>${assistant.email || 'N/A'}</td>
                    <td><span class="role-badge ${assistant.role}">${assistant.role}</span></td>
                    <td>${assistant.department || 'N/A'}</td>
                    <td><span class="status-badge active">${assistant.status}</span></td>
                    <td>
                        <button class="action-btn edit" onclick="editAssistant('${assistant.id}')">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="action-btn delete" onclick="deleteAssistant('${assistant.id}')">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        })
        .catch(error => console.error('Error loading assistants:', error));
}


// Load teachers table
function loadTeachersTable() {
    fetch('/api/teachers')
        .then(response => response.json())
        .then(teachers => {
            const tbody = document.querySelector('#teachers-section .data-table tbody');
            if (!tbody) return;
            
            tbody.innerHTML = '';
            
            teachers.forEach(teacher => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${teacher.id}</td>
                    <td>${teacher.name}</td>
                    <td>${teacher.subject}</td>
                    <td>${teacher.classes.join(', ')}</td>
                    <td><span class="status-badge active">${teacher.status}</span></td>
                    <td>
                        <button class="action-btn edit" onclick="editTeacher('${teacher.id}')">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="action-btn delete" onclick="deleteTeacher('${teacher.id}')">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        })
        .catch(error => console.error('Error loading teachers:', error));
}


// Helper functions
function getParentName(parentId) {
    const parent = window.database.getParentById(parentId);
    return parent ? parent.name : 'N/A';
}

function getTeacherName(teacherId) {
    const teacher = window.database.getTeacherById(teacherId);
    return teacher ? teacher.name : 'N/A';
}

// Show different sections
function showSection(sectionName) {
    // Hide all sections
    const sections = document.querySelectorAll('.admin-section');
    sections.forEach(section => {
        section.classList.remove('active');
    });
    
    // Remove active class from all sidebar items
    const sidebarItems = document.querySelectorAll('.sidebar-item');
    sidebarItems.forEach(item => {
        item.classList.remove('active');
    });
    
    // Show selected section
    const targetSection = document.getElementById(sectionName + '-section');
    if (targetSection) {
        targetSection.classList.add('active');
    }
    
    // Add active class to clicked sidebar item
    const clickedItem = document.querySelector(`[onclick="showSection('${sectionName}')"]`);
    if (clickedItem) {
        clickedItem.classList.add('active');
    }
}

// Student Modal Functions
function openStudentModal() {
    document.getElementById('studentModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
    // Reset parent data
    window.studentParents = {};
    updateParentStatus();
}

function closeStudentModal() {
    document.getElementById('studentModal').style.display = 'none';
    document.body.style.overflow = 'auto';
    document.getElementById('studentForm').reset();
    // Reset parent data
    window.studentParents = {};
    updateParentStatus();
}

// Student Details Modal Functions
function openStudentDetailsModal(studentId) {
    // Fetch student details from the backend
    fetch(`/api/students/${studentId}`)
        .then(response => response.json())
        .then(student => {
            // Populate student information
            document.getElementById('detailStudentId').textContent = student.id || '-';
            document.getElementById('detailStudentName').textContent = student.name || '-';
            document.getElementById('detailStudentClass').textContent = student.class || '-';
            document.getElementById('detailStudentEmail').textContent = student.email || '-';
            document.getElementById('detailStudentPhone').textContent = student.phone || '-';
            document.getElementById('detailStudentStatus').textContent = student.status || '-';
            document.getElementById('detailStudentEnrollment').textContent = student.enrollmentDate || '-';
            
            // Update modal title
            document.getElementById('studentDetailsTitle').textContent = `Student Details - ${student.name}`;
            
            // Populate parents information
            const parentsContainer = document.getElementById('parentsDetailsContainer');
            if (student.parents && student.parents.length > 0) {
                parentsContainer.innerHTML = '';
                student.parents.forEach(parent => {
                    const parentCard = document.createElement('div');
                    parentCard.className = 'parent-detail-card';
                    parentCard.innerHTML = `
                        <h4>
                            <i class="fas ${getParentIcon(parent.parentType)}"></i>
                            ${parent.parentType.charAt(0).toUpperCase() + parent.parentType.slice(1)}
                        </h4>
                        <div class="parent-detail-grid">
                            <div class="detail-item">
                                <label>Name:</label>
                                <span>${parent.name || '-'}</span>
                            </div>
                            <div class="detail-item">
                                <label>Phone:</label>
                                <span>${parent.phone || '-'}</span>
                            </div>
                            <div class="detail-item">
                                <label>Email:</label>
                                <span>${parent.email || '-'}</span>
                            </div>
                            <div class="detail-item">
                                <label>Address:</label>
                                <span>${parent.address || '-'}</span>
                            </div>
                        </div>
                    `;
                    parentsContainer.appendChild(parentCard);
                });
            } else {
                parentsContainer.innerHTML = '<p class="no-parents">No parents information available</p>';
            }
            
            // Show the modal
            document.getElementById('studentDetailsModal').style.display = 'block';
            document.body.style.overflow = 'hidden';
        })
        .catch(error => {
            console.error('Error fetching student details:', error);
            showNotification('Failed to load student details', 'error');
        });
}

function closeStudentDetailsModal() {
    document.getElementById('studentDetailsModal').style.display = 'none';
    document.body.style.overflow = 'auto';
}

function getParentIcon(parentType) {
    const icons = {
        'mother': 'fa-female',
        'father': 'fa-male',
        'supervisor': 'fa-user-tie'
    };
    return icons[parentType] || 'fa-user';
}

// Assistant Modal Functions
function openAssistantModal() {
    document.getElementById('assistantModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function closeAssistantModal() {
    document.getElementById('assistantModal').style.display = 'none';
    document.body.style.overflow = 'auto';
    document.getElementById('assistantForm').reset();
}

function editAssistant(assistantId) {
    // TODO: Implement edit assistant functionality
    showNotification('Edit assistant functionality coming soon', 'info');
}

function deleteAssistant(assistantId) {
    if (confirm('Are you sure you want to delete this assistant?')) {
        // TODO: Implement delete assistant functionality
        showNotification('Delete assistant functionality coming soon', 'info');
    }
}

// Teacher Modal Functions
function openTeacherModal(teacherId = null) {
    document.getElementById('teacherModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
    
    if (teacherId) {
        // Edit mode
        document.getElementById('teacherModalTitle').textContent = 'Edit Teacher';
        document.querySelector('#teacherForm button[type="submit"]').textContent = 'Update Teacher';
        loadTeacherForEdit(teacherId);
    } else {
        // Add mode
        document.getElementById('teacherModalTitle').textContent = 'Add New Teacher';
        document.querySelector('#teacherForm button[type="submit"]').textContent = 'Add Teacher';
        document.getElementById('teacherForm').reset();
        window.selectedTeacherClasses = [];
        updateSelectedClassesDisplay();
    }
}

function closeTeacherModal() {
    document.getElementById('teacherModal').style.display = 'none';
    document.body.style.overflow = 'auto';
    document.getElementById('teacherForm').reset();
    delete document.getElementById('teacherForm').dataset.teacherId;
}

function editTeacher(teacherId) {
    openTeacherModal(teacherId);
}

function deleteTeacher(teacherId) {
    if (confirm('Are you sure you want to delete this teacher?')) {
        // TODO: Implement delete teacher functionality
        showNotification('Delete teacher functionality coming soon', 'info');
    }
}

function loadTeacherForEdit(teacherId) {
    fetch(`/api/teachers/${teacherId}`)
        .then(response => response.json())
        .then(teacher => {
            // Populate form fields
            
            document.getElementById('teacherName').value = teacher.name || '';
            document.getElementById('teacherEmail').value = teacher.email || '';
            document.getElementById('teacherPhone').value = teacher.phone || '';
            document.getElementById('teacherSubject').value = teacher.subject || '';
            
            // Load selected classes
            if (teacher.classes && Array.isArray(teacher.classes)) {
                window.selectedTeacherClasses = [...teacher.classes];
                updateSelectedClassesDisplay();
            } else {
                window.selectedTeacherClasses = [];
                updateSelectedClassesDisplay();
            }
            
            // Store teacher ID for update
            document.getElementById('teacherForm').dataset.teacherId = teacherId;
        })
        .catch(error => {
            console.error('Error loading teacher:', error);
            showNotification('Failed to load teacher data', 'error');
        });
}

// Class Selection Modal Functions
function openClassSelectionModal() {
    document.getElementById('classSelectionModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
    
    // Clear all checkboxes first
    document.querySelectorAll('input[name="classSelection"]').forEach(checkbox => {
        checkbox.checked = false;
    });
    
    // Check already selected classes
    if (window.selectedTeacherClasses) {
        window.selectedTeacherClasses.forEach(className => {
            const checkbox = document.querySelector(`input[name="classSelection"][value="${className}"]`);
            if (checkbox) {
                checkbox.checked = true;
            }
        });
    }
}

function closeClassSelectionModal() {
    document.getElementById('classSelectionModal').style.display = 'none';
    document.body.style.overflow = 'auto';
}

function confirmClassSelection() {
    const selectedCheckboxes = document.querySelectorAll('input[name="classSelection"]:checked');
    window.selectedTeacherClasses = Array.from(selectedCheckboxes).map(cb => cb.value);
    updateSelectedClassesDisplay();
    closeClassSelectionModal();
}

function updateSelectedClassesDisplay() {
    const container = document.getElementById('selectedClasses');
    
    if (!window.selectedTeacherClasses || window.selectedTeacherClasses.length === 0) {
        container.innerHTML = '<p class="no-classes">No classes selected yet</p>';
        return;
    }
    
    container.innerHTML = '';
    window.selectedTeacherClasses.forEach(className => {
        const tag = document.createElement('span');
        tag.className = 'selected-class-tag';
        tag.innerHTML = `
            ${className}
            <button type="button" class="remove-class-btn" onclick="removeClass('${className}')">
                <i class="fas fa-times"></i>
            </button>
        `;
        container.appendChild(tag);
    });
}

function removeClass(className) {
    if (window.selectedTeacherClasses) {
        window.selectedTeacherClasses = window.selectedTeacherClasses.filter(c => c !== className);
        updateSelectedClassesDisplay();
    }
}

// Load teachers table
function loadTeachersTable() {
    fetch('/api/teachers')
        .then(response => response.json())
        .then(teachers => {
            const tbody = document.querySelector('#teachers-section .data-table tbody');
            if (!tbody) return;
            
            tbody.innerHTML = '';
            
            teachers.forEach(teacher => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${teacher.id}</td>
                    <td>${teacher.name}</td>
                    <td>${teacher.subject || 'N/A'}</td>
                    <td>${teacher.classes ? teacher.classes.join(', ') : 'N/A'}</td>
                    <td><span class="status-badge active">${teacher.status}</span></td>
                    <td>
                        <button class="action-btn edit" onclick="editTeacher('${teacher.id}')">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="action-btn delete" onclick="deleteTeacher('${teacher.id}')">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        })
        .catch(error => console.error('Error loading teachers:', error));
}

// Marks Modal Functions
function openMarksModal() {
    document.getElementById('marksModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
    // Load students for the dropdown
    loadStudentsForMarks();
}

function closeMarksModal() {
    document.getElementById('marksModal').style.display = 'none';
    document.body.style.overflow = 'auto';
    document.getElementById('marksForm').reset();
    resetMarksSummary();
}

function editMarks(studentId) {
    // TODO: Implement edit marks functionality
    showNotification('Edit marks functionality coming soon', 'info');
}

function deleteMarks(studentId) {
    if (confirm('Are you sure you want to delete these marks?')) {
        // TODO: Implement delete marks functionality
        showNotification('Delete marks functionality coming soon', 'info');
    }
}

function loadStudentsForMarks() {
    fetch('/api/students')
        .then(response => response.json())
        .then(students => {
            const select = document.getElementById('marksStudent');
            select.innerHTML = '<option value="">Select Student</option>';
            students.forEach(student => {
                const option = document.createElement('option');
                option.value = student.id;
                option.textContent = `${student.id} - ${student.name}`;
                select.appendChild(option);
            });
        })
        .catch(error => console.error('Error loading students:', error));
}

function loadMarksTable() {
    const semester = document.getElementById('semesterSelect').value;
    const classSelect = document.getElementById('classSelect').value;
    
    if (!semester || !classSelect) {
        return;
    }
    
    const params = new URLSearchParams({
        semester: semester,
        class: classSelect
    });
    
    fetch(`/api/marks?${params}`)
        .then(response => response.json())
        .then(marks => {
            const tbody = document.querySelector('#marks-section .data-table tbody');
            if (!tbody) return;
            
            tbody.innerHTML = '';
            
            marks.forEach(mark => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${mark.studentId}</td>
                    <td>${mark.studentName}</td>
                    <td><span class="mark-cell">${mark.arabic}</span></td>
                    <td><span class="mark-cell">${mark.english}</span></td>
                    <td><span class="mark-cell">${mark.math}</span></td>
                    <td><span class="mark-cell">${mark.physics}</span></td>
                    <td><span class="mark-cell">${mark.art}</span></td>
                    <td><span class="total-mark">${mark.total}</span></td>
                    <td><span class="average-mark">${mark.average}</span></td>
                    <td><span class="grade-badge ${getGradeClass(mark.grade)}">${mark.grade}</span></td>
                    <td>
                        <button class="action-btn edit" onclick="editMarks('${mark.studentId}')">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="action-btn delete" onclick="deleteMarks('${mark.studentId}')">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        })
        .catch(error => console.error('Error loading marks:', error));
}

function getGradeClass(grade) {
    switch(grade) {
        case 'A': return 'excellent';
        case 'B': return 'good';
        case 'C': 
        case 'D': return 'average';
        case 'F': return 'poor';
        default: return '';
    }
}

function resetMarksSummary() {
    document.getElementById('totalMarks').textContent = '0';
    document.getElementById('averageMarks').textContent = '0.0';
    document.getElementById('gradeMarks').textContent = '-';
    document.getElementById('gradeMarks').className = 'grade-badge';
}

function calculateMarksSummary() {
    const arabic = parseInt(document.getElementById('arabicMark').value) || 0;
    const english = parseInt(document.getElementById('englishMark').value) || 0;
    const math = parseInt(document.getElementById('mathMark').value) || 0;
    const physics = parseInt(document.getElementById('physicsMark').value) || 0;
    const art = parseInt(document.getElementById('artMark').value) || 0;
    
    const total = arabic + english + math + physics + art;
    const average = total / 5;
    
    document.getElementById('totalMarks').textContent = total;
    document.getElementById('averageMarks').textContent = average.toFixed(1);
    
    // Calculate grade (0-20 scale)
    let grade, gradeClass;
    if (average >= 18) {
        grade = 'A';
        gradeClass = 'excellent';
    } else if (average >= 16) {
        grade = 'B';
        gradeClass = 'good';
    } else if (average >= 14) {
        grade = 'C';
        gradeClass = 'average';
    } else if (average >= 12) {
        grade = 'D';
        gradeClass = 'average';
    } else {
        grade = 'F';
        gradeClass = 'poor';
    }
    
    const gradeElement = document.getElementById('gradeMarks');
    gradeElement.textContent = grade;
    gradeElement.className = `grade-badge ${gradeClass}`;
}

// Parent Modal Functions
function openParentModal(parentType) {
    document.getElementById('parentModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
    
    // Set parent type and title
    document.getElementById('parentType').value = parentType;
    const titles = {
        'mother': 'Add Mother',
        'father': 'Add Father',
        'supervisor': 'Add Supervisor'
    };
    document.getElementById('parentModalTitle').textContent = titles[parentType];
    
    // Reset form
    document.getElementById('parentForm').reset();
    document.getElementById('parentType').value = parentType;
}

function closeParentModal() {
    document.getElementById('parentModal').style.display = 'none';
    document.body.style.overflow = 'auto';
    document.getElementById('parentForm').reset();
}

// Parent status management
function updateParentStatus() {
    const parentStatus = document.getElementById('parentStatus');
    const parentButtons = document.querySelectorAll('.parent-btn');
    
    if (!window.studentParents) {
        window.studentParents = {};
    }
    
    const addedParents = Object.keys(window.studentParents);
    const totalParents = 3;
    
    // Update button states
    parentButtons.forEach(btn => {
        const parentType = btn.onclick.toString().match(/openParentModal\('(\w+)'\)/)[1];
        if (addedParents.includes(parentType)) {
            btn.classList.add('added');
            btn.innerHTML = `<i class="fas fa-check"></i><span>${parentType.charAt(0).toUpperCase() + parentType.slice(1)} Added</span>`;
        } else {
            btn.classList.remove('added');
            const icons = {
                'mother': 'fa-female',
                'father': 'fa-male',
                'supervisor': 'fa-user-tie'
            };
            btn.innerHTML = `<i class="fas ${icons[parentType]}"></i><span>Add ${parentType.charAt(0).toUpperCase() + parentType.slice(1)}</span>`;
        }
    });
    
    // Update status text
    if (addedParents.length === 0) {
        parentStatus.textContent = 'No parents added yet. click the buttons above to add them.';
    } else if (addedParents.length === totalParents) {
        parentStatus.innerHTML = `<i class="fas fa-check-circle" style="color: #28a745;"></i> All parents added successfully!`;
    } else {
        parentStatus.textContent = `${addedParents.length} of ${totalParents} parents added. Parents are optional.`;
    }
}




// Edit Functions
function editStudent(studentId) {
    showNotification(`Edit student ${studentId} - Coming soon!`, 'info');
}


// Delete Functions
function deleteStudent(studentId) {
    if (confirm(`Are you sure you want to delete student ${studentId}?`)) {
        fetch(`/api/students/${studentId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification(`Student ${studentId} deleted successfully!`, 'success');
                loadStudentsTable(); // Refresh table
                loadDashboardData(); // Refresh dashboard
            } else {
                showNotification('Failed to delete student', 'error');
            }
        })
        .catch(error => {
            console.error('Error deleting student:', error);
            showNotification('Failed to delete student', 'error');
        });
    }
}


// Form Handling
document.addEventListener('DOMContentLoaded', function() {
    // Student Form
    const studentForm = document.getElementById('studentForm');
    if (studentForm) {
        studentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const studentData = {
                name: formData.get('studentName'),
                email: formData.get('studentEmail'),
                class: formData.get('studentClass'),
                phone: formData.get('studentPhone'),
                parents: window.studentParents || {}
            };
            
            // Validation
            if (!studentData.name || !studentData.class) {
                showNotification('Please fill in all required student fields', 'error');
                return;
            }
            
            if (studentData.email && !isValidEmail(studentData.email)) {
                showNotification('Please enter a valid student email address', 'error');
                return;
            }
            
            // Parents are optional - no validation required
            
            // Add student with parents via Flask API
            showNotification('Creating student account with parents...', 'info');
            
            fetch('/api/students', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(studentData)
            })
            .then(response => response.json())
            .then(newStudent => {
                showNotification(`Student "${newStudent.name}" and parents created successfully!`, 'success');
                closeStudentModal();
                loadStudentsTable(); // Refresh table
                loadDashboardData(); // Refresh dashboard
            })
            .catch(error => {
                console.error('Error creating student:', error);
                showNotification('Failed to create student', 'error');
            });
        });
    }
    
    // Parent Form
    const parentForm = document.getElementById('parentForm');
    if (parentForm) {
        parentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const parentType = formData.get('parentType');
            const parentData = {
                name: formData.get('parentName'),
                phone: formData.get('parentPhone'),
                email: formData.get('parentEmail'),
                address: formData.get('parentAddress')
            };
            
            // Validation
            if (!parentData.name || !parentData.phone || !parentData.email || !parentData.address) {
                showNotification('Please fill in all required fields', 'error');
                return;
            }
            
            if (!isValidEmail(parentData.email)) {
                showNotification('Please enter a valid email address', 'error');
                return;
            }
            
            if (!isValidPhone(parentData.phone)) {
                showNotification('Please enter a valid phone number', 'error');
                return;
            }
            
            // Store parent data
            if (!window.studentParents) {
                window.studentParents = {};
            }
            window.studentParents[parentType] = parentData;
            
            // Update UI
            updateParentStatus();
            closeParentModal();
            
            showNotification(`${parentType.charAt(0).toUpperCase() + parentType.slice(1)} added successfully!`, 'success');
        });
    }
    
    // Assistant Form
    const assistantForm = document.getElementById('assistantForm');
    if (assistantForm) {
        assistantForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const assistantData = {
                name: formData.get('assistantName'),
                email: formData.get('assistantEmail'),
                role: formData.get('assistantRole'),
                department: formData.get('assistantDepartment'),
                phone: formData.get('assistantPhone'),
                permissions: formData.getAll('permissions')
            };
            
            // Validation
            if (!assistantData.name || !assistantData.email || !assistantData.role || !assistantData.department) {
                showNotification('Please fill in all required fields', 'error');
                return;
            }
            
            if (!isValidEmail(assistantData.email)) {
                showNotification('Please enter a valid email address', 'error');
                return;
            }
            
            // Add assistant via Flask API
            showNotification('Creating assistant account...', 'info');
            
            fetch('/api/assistants', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(assistantData)
            })
            .then(response => response.json())
            .then(newAssistant => {
                showNotification(`Assistant "${newAssistant.name}" created successfully!`, 'success');
                closeAssistantModal();
                loadAssistantsTable(); // Refresh table
                loadDashboardData(); // Refresh dashboard
            })
            .catch(error => {
                console.error('Error creating assistant:', error);
                showNotification('Failed to create assistant', 'error');
            });
        });
    }
    
    // Teacher Form
    const teacherForm = document.getElementById('teacherForm');
    if (teacherForm) {
        teacherForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const teacherData = {
                name: formData.get('teacherName'),
                email: formData.get('teacherEmail'),
                phone: formData.get('teacherPhone'),
                subject: formData.get('teacherSubject'),
                classes: window.selectedTeacherClasses || []
            };
            
            // Validation
            if (!teacherData.name || !teacherData.email || !teacherData.subject) {
                showNotification('Please fill in all required fields', 'error');
                return;
            }
            
            if (!isValidEmail(teacherData.email)) {
                showNotification('Please enter a valid email address', 'error');
                return;
            }
            
            if (teacherData.classes.length === 0) {
                showNotification('Please select at least one class', 'error');
                return;
            }
            
            const teacherId = document.getElementById('teacherForm').dataset.teacherId;
            const isEdit = !!teacherId;
            
            if (isEdit) {
                // Update existing teacher
                showNotification('Updating teacher...', 'info');
                
                fetch(`/api/teachers/${teacherId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(teacherData)
                })
                .then(response => response.json())
                .then(updatedTeacher => {
                    showNotification(`Teacher "${updatedTeacher.name}" updated successfully!`, 'success');
                    closeTeacherModal();
                    loadTeachersTable(); // Refresh table
                    loadDashboardData(); // Refresh dashboard
                })
                .catch(error => {
                    console.error('Error updating teacher:', error);
                    showNotification('Failed to update teacher', 'error');
                });
            } else {
                // Create new teacher
                showNotification('Creating teacher account...', 'info');
                
                fetch('/api/teachers', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(teacherData)
                })
                .then(response => response.json())
                .then(newTeacher => {
                    showNotification(`Teacher "${newTeacher.name}" created successfully!`, 'success');
                    closeTeacherModal();
                    loadTeachersTable(); // Refresh table
                    loadDashboardData(); // Refresh dashboard
                })
                .catch(error => {
                    console.error('Error creating teacher:', error);
                    showNotification('Failed to create teacher', 'error');
                });
            }
        });
    }
    
    // Marks Form
    const marksForm = document.getElementById('marksForm');
    if (marksForm) {
        marksForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const marksData = {
                studentId: formData.get('marksStudent'),
                semester: formData.get('marksSemester'),
                arabic: parseInt(formData.get('arabicMark')) || 0,
                english: parseInt(formData.get('englishMark')) || 0,
                math: parseInt(formData.get('mathMark')) || 0,
                physics: parseInt(formData.get('physicsMark')) || 0,
                art: parseInt(formData.get('artMark')) || 0
            };
            
            // Validation
            if (!marksData.studentId || !marksData.semester) {
                showNotification('Please select student and semester', 'error');
                return;
            }
            
            // Validate marks (0-20)
            const marks = [marksData.arabic, marksData.english, marksData.math, marksData.physics, marksData.art];
            for (let mark of marks) {
                if (mark < 0 || mark > 20) {
                    showNotification('All marks must be between 0 and 20', 'error');
                    return;
                }
            }
            
            // Add marks via Flask API
            showNotification('Saving student marks...', 'info');
            
            fetch('/api/marks', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(marksData)
            })
            .then(response => response.json())
            .then(newMarks => {
                showNotification(`Marks saved successfully for ${newMarks.studentName}!`, 'success');
                closeMarksModal();
                loadMarksTable(); // Refresh table
            })
            .catch(error => {
                console.error('Error saving marks:', error);
                showNotification('Failed to save marks', 'error');
            });
        });
        
        // Add event listeners for real-time calculation
        const markInputs = ['arabicMark', 'englishMark', 'mathMark', 'physicsMark', 'artMark'];
        markInputs.forEach(inputId => {
            document.getElementById(inputId).addEventListener('input', calculateMarksSummary);
        });
    }
});

// Validation Functions
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function isValidStudentId(id) {
    const idRegex = /^[A-Z]{2}\d{3}$/i;
    return idRegex.test(id);
}

function isValidParentId(id) {
    const idRegex = /^[A-Z]\d{3}$/i;
    return idRegex.test(id);
}

function isValidPhone(phone) {
    const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
    return phoneRegex.test(phone.replace(/\s/g, ''));
}

// Notification System
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notification => notification.remove());
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas ${getNotificationIcon(type)}"></i>
            <span>${message}</span>
        </div>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${getNotificationColor(type)};
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        z-index: 10000;
        transform: translateX(400px);
        transition: transform 0.3s ease;
        max-width: 300px;
        word-wrap: break-word;
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Auto remove after 4 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(400px)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 300);
    }, 4000);
}

function getNotificationIcon(type) {
    switch (type) {
        case 'success': return 'fa-check-circle';
        case 'error': return 'fa-exclamation-circle';
        case 'warning': return 'fa-exclamation-triangle';
        default: return 'fa-info-circle';
    }
}

function getNotificationColor(type) {
    switch (type) {
        case 'success': return '#4A90E2';
        case 'error': return '#e74c3c';
        case 'warning': return '#D4AF37';
        default: return '#072A53';
    }
}

// Close modal when clicking outside
window.addEventListener('click', function(event) {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        if (event.target === modal) {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    });
});

// Keyboard shortcuts
document.addEventListener('keydown', function(event) {
    // Escape key to close modals
    if (event.key === 'Escape') {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            if (modal.style.display === 'block') {
                modal.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        });
    }
});


// Animate numbers
function animateNumber(element, start, end, duration) {
    const startTime = performance.now();
    
    function updateNumber(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const current = Math.floor(start + (end - start) * progress);
        element.textContent = current.toLocaleString();
        
        if (progress < 1) {
            requestAnimationFrame(updateNumber);
        }
    }
    
    requestAnimationFrame(updateNumber);
}

// Contact Section Functions
let emailTemplates = {
    student_greeting: {
        subject: "Welcome to Sylverith School, {student}!",
        message: `Hello {student},

Welcome to Sylverith School! We are excited to have you as part of our {class} class.

We look forward to supporting your educational journey and helping you achieve your goals.

Best regards,
Sylverith School Administration`
    },
    parent_greeting: {
        subject: "Welcome to Sylverith School Community, {parent}!",
        message: `Dear {parent},

Welcome to the Sylverith School community! We are delighted to have {student} join our {class} class.

We believe in fostering strong partnerships between school and home to ensure the best educational experience for your child.

Please don't hesitate to reach out if you have any questions or concerns.

Best regards,
Sylverith School Administration`
    },
    announcement: {
        subject: "Important Announcement from Sylverith School",
        message: `Dear {parent},

We hope this message finds you well. We have an important announcement regarding upcoming events and activities at Sylverith School.

Please stay tuned for more details and updates.

Best regards,
Sylverith School Administration`
    },
    reminder: {
        subject: "Reminder: Upcoming Event at Sylverith School",
        message: `Dear {parent},

This is a friendly reminder about an upcoming event at Sylverith School.

Please mark your calendar and join us for this special occasion.

Best regards,
Sylverith School Administration`
    },
    event: {
        subject: "You're Invited: Special Event at Sylverith School",
        message: `Dear {parent},

You and {student} are cordially invited to join us for a special event at Sylverith School.

We look forward to seeing you there!

Best regards,
Sylverith School Administration`
    }
};

// Update audience count based on filters
function updateAudienceCount() {
    const audienceType = document.querySelector('input[name="audienceType"]:checked').value;
    const classFilter = document.getElementById('classFilter').value;
    const gradeFilter = document.getElementById('gradeFilter').value;
    
    // This would normally fetch from the API, but for demo purposes we'll simulate
    let count = 0;
    
    if (audienceType === 'students') {
        // Simulate student count based on filters
        if (classFilter) {
            count = 25; // Average students per class
        } else if (gradeFilter) {
            count = 50; // Average students per grade (2 classes)
        } else {
            count = 250; // Total students
        }
    } else {
        // Simulate parent count (roughly 2 parents per student)
        if (classFilter) {
            count = 50; // Average parents per class
        } else if (gradeFilter) {
            count = 100; // Average parents per grade
        } else {
            count = 500; // Total parents
        }
    }
    
    document.getElementById('audienceCount').textContent = `${count} recipients selected`;
}

// Load email template
function loadEmailTemplate() {
    const templateSelect = document.getElementById('emailTemplate');
    const template = templateSelect.value;
    
    if (template === 'custom') {
        document.getElementById('emailSubject').value = '';
        document.getElementById('emailMessage').value = '';
        return;
    }
    
    if (emailTemplates[template]) {
        document.getElementById('emailSubject').value = emailTemplates[template].subject;
        document.getElementById('emailMessage').value = emailTemplates[template].message;
    }
}

// Insert variable into message
function insertVariable(variable) {
    const messageTextarea = document.getElementById('emailMessage');
    const cursorPos = messageTextarea.selectionStart;
    const textBefore = messageTextarea.value.substring(0, cursorPos);
    const textAfter = messageTextarea.value.substring(messageTextarea.selectionEnd);
    
    messageTextarea.value = textBefore + variable + textAfter;
    messageTextarea.focus();
    messageTextarea.setSelectionRange(cursorPos + variable.length, cursorPos + variable.length);
}

// Preview email
function previewEmail() {
    const subject = document.getElementById('emailSubject').value;
    const message = document.getElementById('emailMessage').value;
    const audienceType = document.querySelector('input[name="audienceType"]:checked').value;
    const classFilter = document.getElementById('classFilter').value;
    const gradeFilter = document.getElementById('gradeFilter').value;
    
    if (!subject || !message) {
        showNotification('Please fill in both subject and message', 'error');
        return;
    }
    
    // Update preview content
    document.getElementById('previewSubject').textContent = subject;
    document.getElementById('previewMessage').textContent = message;
    
    // Update recipient count
    const count = document.getElementById('audienceCount').textContent;
    document.getElementById('previewRecipients').textContent = count;
    
    // Show preview modal
    document.getElementById('emailPreviewModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
}

// Close email preview
function closeEmailPreview() {
    document.getElementById('emailPreviewModal').style.display = 'none';
    document.body.style.overflow = 'auto';
}

// Send email from preview
function sendEmailFromPreview() {
    const subject = document.getElementById('emailSubject').value;
    const message = document.getElementById('emailMessage').value;
    const audienceType = document.querySelector('input[name="audienceType"]:checked').value;
    const classFilter = document.getElementById('classFilter').value;
    const gradeFilter = document.getElementById('gradeFilter').value;
    
    const emailData = {
        subject: subject,
        message: message,
        audienceType: audienceType,
        classFilter: classFilter,
        gradeFilter: gradeFilter
    };
    
    showNotification('Sending emails...', 'info');
    
    fetch('/api/contact/send', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(emailData)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            showNotification(`Emails sent successfully to ${result.recipientCount} recipients!`, 'success');
            closeEmailPreview();
            // Reset form
            document.getElementById('contactForm').reset();
            updateAudienceCount();
        } else {
            showNotification('Failed to send emails: ' + result.error, 'error');
        }
    })
    .catch(error => {
        console.error('Error sending emails:', error);
        showNotification('Failed to send emails', 'error');
    });
}

// Contact form submission
function handleContactFormSubmit(e) {
    e.preventDefault();
    previewEmail();
}

// Initialize contact section
function initializeContactSection() {
    // Add event listeners
    document.querySelectorAll('input[name="audienceType"]').forEach(radio => {
        radio.addEventListener('change', updateAudienceCount);
    });
    
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', handleContactFormSubmit);
    }
    
    // Initial audience count
    updateAudienceCount();
}
