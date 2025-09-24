# 🎓 Sylverith School Management System

A modern, comprehensive school management system built with Flask and featuring a beautiful, responsive web interface.

## ✨ Features

- **🏠 Home Page**: Modern landing page with services, plans, and contact information
- **🔐 Authentication**: Secure login system with role-based access
- **📊 Admin Dashboard**: Comprehensive management interface
- **👥 Student Management**: Add, edit, delete student records
- **👨‍👩‍👧‍👦 Parent Management**: Manage parent accounts and relationships
- **👨‍🏫 Teacher Management**: View teacher information and assignments
- **🏫 Class Management**: Organize classes and student assignments
- **📈 Analytics**: Real-time statistics and activity tracking
- **📱 Responsive Design**: Works perfectly on desktop, tablet, and mobile

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project**
   ```bash
   # If you have git
   git clone <repository-url>
   cd sylverith-ui
   
   # Or simply navigate to the project folder
   cd "path/to/Sylverith UI"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python run.py
   ```
   
   Or alternatively:
   ```bash
   python app.py
   ```

4. **Access the application**
   - Open your browser and go to: `http://localhost:5000`
   - The application will be running on port 5000

## 🔐 Test Credentials

Use these credentials to test the admin functionality:

### Super Administrator
- **Email:** `admin@sylverith.com`
- **Password:** `admin123`
- **Access:** Full system access

### Principal
- **Email:** `principal@sylverith.com`
- **Password:** `principal123`
- **Access:** Students, Teachers, Classes, Reports

### Registrar
- **Email:** `registrar@sylverith.com`
- **Password:** `registrar123`
- **Access:** Students, Parents, Classes

## 📁 Project Structure

```
Sylverith UI/
├── app.py                 # Main Flask application
├── run.py                 # Application runner script
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── home.html         # Landing page
│   ├── index.html        # Login page
│   └── admin.html        # Admin dashboard
└── static/               # Static assets
    ├── styles.css        # Main stylesheet
    ├── script.js         # Home/login JavaScript
    ├── admin-script.js   # Admin dashboard JavaScript
    ├── database.js       # Client-side database (legacy)
    └── sylverith-logov3c3png.png  # Logo
```

## 🎨 Design Features

- **Modern UI**: Clean, professional design with smooth animations
- **Brand Colors**: 
  - Primary Blue: `#4A90E2`
  - Deep Navy: `#072A53`
  - Accent Gold: `#D4AF37`
- **Responsive**: Mobile-first design that works on all devices
- **Interactive**: Hover effects, smooth transitions, and dynamic content

## 🔧 API Endpoints

The Flask application provides the following API endpoints:

- `GET /` - Home page
- `GET /login` - Login page
- `GET /admin` - Admin dashboard (requires authentication)
- `POST /api/login` - User authentication
- `POST /api/logout` - User logout
- `GET /api/dashboard/stats` - Dashboard statistics
- `GET /api/dashboard/activities` - Recent activities
- `GET /api/students` - Get all students
- `POST /api/students` - Create new student
- `DELETE /api/students/<id>` - Delete student
- `GET /api/parents` - Get all parents
- `POST /api/parents` - Create new parent
- `DELETE /api/parents/<id>` - Delete parent
- `GET /api/teachers` - Get all teachers
- `GET /api/classes` - Get all classes

## 🛠️ Development

### Running in Development Mode
```bash
python app.py
```
The application will run with debug mode enabled, allowing for automatic reloading when files change.

### Customizing the Application
- **Styling**: Edit `static/styles.css` to modify the appearance
- **Functionality**: Update `static/script.js` and `static/admin-script.js` for frontend logic
- **Backend**: Modify `app.py` to add new features or API endpoints
- **Templates**: Edit files in `templates/` to change page layouts

## 📊 Sample Data

The application comes pre-loaded with sample data:
- 5 Students across different grades
- 5 Parents linked to students
- 4 Teachers with different subjects
- 5 Classes with student assignments
- Recent activity logs

## 🔒 Security Notes

- This is a demo application with sample data
- In production, implement proper password hashing
- Use environment variables for sensitive configuration
- Implement proper session management
- Add CSRF protection for forms

## 🌐 Deployment

For production deployment:
1. Set `debug=False` in `app.py`
2. Use a production WSGI server like Gunicorn
3. Configure a reverse proxy (nginx)
4. Set up a proper database (PostgreSQL, MySQL)
5. Implement proper security measures

## 📞 Support

For questions or issues:
- Check the test credentials above
- Ensure all dependencies are installed
- Verify Python version compatibility
- Check the browser console for JavaScript errors

---

**Sylverith School Management System** - Empowering education through innovative technology solutions.
