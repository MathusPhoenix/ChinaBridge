# ChinaBridge Academy - Setup Guide

This is a complete tutoring platform with student registration, login, and database functionality using SQLite.

## Project Structure

```
ChinaBridge/
├── index.html          # Main website with login/register forms
├── dashboard.html      # Student dashboard (only visible when logged in)
├── admin.html          # Admin dashboard to view all students
├── styles.css          # Website styling
├── server.py           # Flask backend with API endpoints
├── requirements.txt    # Python dependencies
├── chinabridge.db      # SQLite database (created automatically)
└── README.md          # This file
```

## Prerequisites

Before you begin, make sure you have the following installed:

1. **Python 3.8+** - [Download here](https://www.python.org/downloads/)
2. **A code editor** - VS Code, PyCharm, etc.

**Note:** SQLite comes built-in with Python, so no separate database server installation is needed!

## Setup Instructions

### Step 1: Install Python Dependencies

Open a terminal in the ChinaBridge folder and run:

```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- Flask-CORS (for cross-origin requests)
- Werkzeug (for password hashing)

### Step 2: Run the Flask Server

In your terminal, run:

```bash
python server.py
```

You should see output like:
```
Database initialized successfully
 * Running on http://localhost:5000
 * Debug mode: on
```

The `chinabridge.db` file will be created automatically in your project folder.

### Step 3: Open the Website

1. Open `index.html` in your web browser
2. **Register or Login** to access your personalized dashboard
3. Once logged in, you'll be automatically redirected to `dashboard.html`

## Student Dashboard Features

The **personalized student dashboard** is only accessible after logging in and provides:

- **Welcome greeting** with the student's name
- **My Courses section** - Shows all enrolled courses with tutor information  
- **Available Courses** - If you haven't enrolled yet, automatically displays all available courses
- **Tutoring Sessions** - View all upcoming and completed tutoring sessions
- **Quick Actions** - Book new sessions or manage enrollments

**Key Feature:** If a student has no enrollments yet, the dashboard automatically displays all available courses to encourage sign-ups!

### Step 4: Access the Admin Dashboard

Once the server is running, you can view all registered students by opening:
```
admin.html
```

The admin dashboard displays:
- **Total number of students**
- **New students this month**
- **Active users count**
- **Table of all students** with their details
- **Delete functionality** to remove students from the system

You can also access it by adding a link to your main website.

## Admin Dashboard Features

The `admin.html` file provides a complete admin interface where you can:

1. **View all students** - See a table of registered students with their information
2. **View student details** - Click "View" to see individual student information
3. **Delete students** - Remove students from the database
4. **Statistics** - Monitor total students and registration trends

Simply open `admin.html` in your browser to access it anytime!

## API Endpoints

The Flask server provides the following API endpoints:

### User Registration
- **POST** `/api/register`
- Body:
  ```json
  {
    "email": "student@example.com",
    "password": "password123",
    "first_name": "John",
    "last_name": "Doe"
  }
  ```

### User Login
- **POST** `/api/login`
- Body:
  ```json
  {
    "email": "student@example.com",
    "password": "password123"
  }
  ```

### Get All Students (Admin)
- **GET** `/api/students`
- Returns: List of all students with ID, email, name, phone, and creation date

### Delete a Student
- **DELETE** `/api/student/{student_id}`

### Book a Tutoring Session
- **POST** `/api/sessions`
- Body:
  ```json
  {
    "student_id": 1,
    "tutor_name": "Phoenix",
    "date_time": "2025-02-15 14:00:00",
    "duration_hours": 1,
    "notes": "Prepare for SAT"
  }
  ```

### Get Student Sessions
- **GET** `/api/sessions/{student_id}`

### Get Student Enrollments
- **GET** `/api/enrollments/{student_id}`
- Returns: List of courses the student is enrolled in

## Database Schema

### students table
```sql
CREATE TABLE students (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  first_name TEXT,
  last_name TEXT,
  phone TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### tutoring_sessions table
```sql
CREATE TABLE tutoring_sessions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_id INTEGER NOT NULL,
  tutor_name TEXT,
  date_time TEXT,
  duration_hours INTEGER,
  status TEXT DEFAULT 'scheduled',
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (student_id) REFERENCES students(id)
)
```

### enrollments table
```sql
CREATE TABLE enrollments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_id INTEGER NOT NULL,
  subject TEXT,
  tutor_name TEXT,
  enrolled_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (student_id) REFERENCES students(id)
)
```

## Features

✅ User Registration with email validation
✅ Secure Login with password hashing
✅ **Personalized Student Dashboard** - only visible when logged in
✅ Available courses display when no enrollments yet
✅ Student profile management
✅ Tutoring session booking system
✅ **Admin Dashboard to view all students**
✅ Responsive design
✅ Error handling and validation
✅ Local storage for session management

## Troubleshooting

### Database not created
- The `chinabridge.db` file will be created automatically when you run the server
- Make sure the server has permission to write files in the ChinaBridge folder

### Port 5000 Already in Use
- Change the port in `server.py` last line: `app.run(debug=True, host='localhost', port=5001)`

### CORS Errors
- Make sure the Flask server is running on `http://localhost:5000`
- Check browser console for error details

### Module Not Found
- Make sure you ran `pip install -r requirements.txt`
- Try: `pip install Flask Flask-Cors Werkzeug`

## Next Steps

1. Test registration and login functionality
2. Add more features like payment processing
3. Create a student dashboard to view sessions
4. Add email verification
5. Implement password reset functionality

## Support

For issues or questions about the setup, check the server console for error messages.

---

Happy teaching! 🎓
