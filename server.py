from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from datetime import datetime, timedelta
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
CORS(app)

# Production mode detection
import os
DEBUG_MODE = os.environ.get('FLASK_ENV') == 'development'

# Email Configuration
EMAIL_CONFIG = {
    'sender_email': 'chinabridge939@gmail.com',  # Change this to your email
    'sender_password': 'mvkfgsyxwvegnhpz',      # Use Gmail App Password
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587
}

# SQLite Database Configuration
DB_PATH = os.path.join(os.path.dirname(__file__), 'chinabridge.db')

def get_db_connection():
    """Create and return a database connection"""
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.row_factory = sqlite3.Row
        return connection
    except sqlite3.Error as e:
        print(f"Error connecting to SQLite Database: {e}")
        return None

def send_email(recipient_email, subject, body, is_html=False):
    """Send an email using SMTP"""
    try:
        # Create message
        message = MIMEMultipart()
        message['From'] = EMAIL_CONFIG['sender_email']
        message['To'] = recipient_email
        message['Subject'] = subject
        
        # Add body
        if is_html:
            message.attach(MIMEText(body, 'html'))
        else:
            message.attach(MIMEText(body, 'plain'))
        
        # Send email
        with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
            server.starttls()
            server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
            server.send_message(message)
        
        print(f"Email sent successfully to {recipient_email}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def init_db():
    """Initialize the database and create tables if they don't exist"""
    connection = get_db_connection()
    if connection is None:
        print(f"Failed to connect to database at {DB_PATH}")
        return False
    
    try:
        cursor = connection.cursor()
        
        # Check if students table already exists to avoid redundant operations
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='students'")
        if cursor.fetchone():
            print("✓ Database tables already exist")
            cursor.close()
            connection.close()
            return True
        
        # Create students table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                first_name TEXT,
                last_name TEXT,
                phone TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create enrollments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS enrollments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                subject TEXT,
                tutor_name TEXT,
                enrolled_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(id)
            )
        """)
        
        # Create sessions table for tutoring bookings
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tutoring_sessions (
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
        """)
        
        # Create password reset tokens table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS password_reset_tokens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                token TEXT UNIQUE NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                used INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(id)
            )
        """)
        
        connection.commit()
        cursor.close()
        connection.close()
        print("✓ Database tables created")
        return True
        
    except sqlite3.Error as e:
        print(f"✗ Error initializing database: {e}")
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        return False
    except Exception as e:
        print(f"✗ Unexpected error during init_db: {e}")
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        return False

# Initialize database on app startup
print("=" * 60)
print("⚡ ChinaBridge Server Starting...")
print(f"📁 Database: {DB_PATH}")
print("=" * 60)

init_start = datetime.now()
init_db()
init_end = datetime.now()
print(f"✓ Database initialized in {(init_end - init_start).total_seconds():.2f}s")
print("=" * 60)

# Health check endpoint
@app.route('/ping', methods=['GET'])
def ping():
    """Simple ping endpoint for keep-alive monitoring"""
    return jsonify({'status': 'pong', 'timestamp': datetime.now().isoformat()}), 200

@app.route('/api/health', methods=['GET'])
def health():
    """Check if database is initialized"""
    try:
        db_exists = os.path.exists(DB_PATH)
        print(f"[HEALTH] Database path: {DB_PATH}")
        print(f"[HEALTH] Database file exists: {db_exists}")
        
        connection = get_db_connection()
        if connection is None:
            return jsonify({
                'status': 'error', 
                'message': 'Cannot connect to database',
                'database_path': DB_PATH,
                'database_file_exists': db_exists
            }), 500
        
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"[HEALTH] Tables found: {tables}")
        
        students_table_exists = 'students' in tables
        cursor.close()
        connection.close()
        
        response = {
            'status': 'ok',
            'database_path': DB_PATH,
            'database_file_exists': db_exists,
            'students_table_exists': students_table_exists,
            'all_tables': tables
        }
        print(f"[HEALTH] Returning: {response}")
        return jsonify(response), 200
    except Exception as e:
        print(f"[HEALTH] Exception: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Serve static HTML files
@app.route('/')
def index():
    """Serve homepage"""
    try:
        with open(os.path.join(os.path.dirname(__file__), 'index.html'), 'r') as f:
            return f.read()
    except Exception as e:
        return jsonify({'error': f'Failed to load index.html: {str(e)}'}), 500

@app.route('/index.html')
def index_html():
    """Serve homepage explicitly"""
    try:
        with open(os.path.join(os.path.dirname(__file__), 'index.html'), 'r') as f:
            return f.read()
    except Exception as e:
        return jsonify({'error': f'Failed to load index.html: {str(e)}'}), 500

@app.route('/dashboard')
def dashboard():
    """Serve student dashboard"""
    try:
        with open(os.path.join(os.path.dirname(__file__), 'dashboard.html'), 'r') as f:
            return f.read()
    except Exception as e:
        return jsonify({'error': f'Failed to load dashboard.html: {str(e)}'}), 500

@app.route('/dashboard.html')
def dashboard_html():
    """Serve student dashboard explicitly"""
    try:
        with open(os.path.join(os.path.dirname(__file__), 'dashboard.html'), 'r') as f:
            return f.read()
    except Exception as e:
        return jsonify({'error': f'Failed to load dashboard.html: {str(e)}'}), 500

@app.route('/admin')
def admin():
    """Serve admin panel"""
    try:
        with open(os.path.join(os.path.dirname(__file__), 'admin.html'), 'r') as f:
            return f.read()
    except Exception as e:
        return jsonify({'error': f'Failed to load admin.html: {str(e)}'}), 500

@app.route('/admin.html')
def admin_html():
    """Serve admin panel explicitly"""
    try:
        with open(os.path.join(os.path.dirname(__file__), 'admin.html'), 'r') as f:
            return f.read()
    except Exception as e:
        return jsonify({'error': f'Failed to load admin.html: {str(e)}'}), 500

@app.route('/reset-password')
def reset_password_page():
    """Serve password reset page"""
    try:
        with open(os.path.join(os.path.dirname(__file__), 'reset-password.html'), 'r') as f:
            return f.read()
    except Exception as e:
        return jsonify({'error': f'Failed to load reset-password.html: {str(e)}'}), 500

@app.route('/reset-password.html')
def reset_password_html():
    """Serve password reset page explicitly"""
    try:
        with open(os.path.join(os.path.dirname(__file__), 'reset-password.html'), 'r') as f:
            return f.read()
    except Exception as e:
        return jsonify({'error': f'Failed to load reset-password.html: {str(e)}'}), 500

@app.route('/styles.css')
def styles():
    """Serve CSS file"""
    try:
        with open(os.path.join(os.path.dirname(__file__), 'styles.css'), 'r') as f:
            return f.read(), 200, {'Content-Type': 'text/css'}
    except Exception as e:
        return jsonify({'error': f'Failed to load styles.css: {str(e)}'}), 500

@app.route('/translations.js')
def translations():
    """Serve translations file"""
    try:
        with open(os.path.join(os.path.dirname(__file__), 'translations.js'), 'r') as f:
            return f.read(), 200, {'Content-Type': 'application/javascript'}
    except Exception as e:
        return jsonify({'error': f'Failed to load translations.js: {str(e)}'}), 500

@app.route('/api/register', methods=['POST'])
def register():
    """Register a new student"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        
        # Validation
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        connection = get_db_connection()
        if connection is None:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor()
        
        try:
            # Check if email already exists
            cursor.execute("SELECT id FROM students WHERE email = ?", (email,))
            if cursor.fetchone():
                return jsonify({'error': 'Email already registered'}), 400
            
            # Hash password
            hashed_password = generate_password_hash(password)
            
            # Insert new student
            cursor.execute("""
                INSERT INTO students (email, password, first_name, last_name)
                VALUES (?, ?, ?, ?)
            """, (email, hashed_password, first_name, last_name))
            
            connection.commit()
            student_id = cursor.lastrowid
            
            return jsonify({
                'message': 'Registration successful',
                'student_id': student_id,
                'email': email
            }), 201
            
        except sqlite3.IntegrityError:
            return jsonify({'error': 'Email already registered'}), 400
        finally:
            cursor.close()
            connection.close()
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """Login a student"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        connection = get_db_connection()
        if connection is None:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor()
        
        # Find student by email
        cursor.execute("SELECT id, email, password, first_name, last_name FROM students WHERE email = ?", (email,))
        student = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        if not student:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Check password
        if not check_password_hash(student['password'], password):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        return jsonify({
            'message': 'Login successful',
            'student_id': student['id'],
            'email': student['email'],
            'first_name': student['first_name'],
            'last_name': student['last_name']
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/student/<int:student_id>', methods=['GET'])
def get_student(student_id):
    """Get student profile"""
    try:
        connection = get_db_connection()
        if connection is None:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor()
        
        cursor.execute("SELECT id, email, first_name, last_name, created_at FROM students WHERE id = ?", (student_id,))
        student = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        return jsonify(dict(student)), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/student/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """Delete a student"""
    try:
        connection = get_db_connection()
        if connection is None:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor()
        
        # Check if student exists
        cursor.execute("SELECT id FROM students WHERE id = ?", (student_id,))
        if not cursor.fetchone():
            cursor.close()
            connection.close()
            return jsonify({'error': 'Student not found'}), 404
        
        # Delete student
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        connection.commit()
        
        cursor.close()
        connection.close()
        
        return jsonify({'message': 'Student deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sessions/<int:student_id>', methods=['GET'])
def get_student_sessions(student_id):
    """Get tutoring sessions for a student"""
    try:
        connection = get_db_connection()
        if connection is None:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT id, tutor_name, date_time, duration_hours, status, notes
            FROM tutoring_sessions
            WHERE student_id = ?
            ORDER BY date_time DESC
        """, (student_id,))
        
        sessions = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify([dict(row) for row in sessions]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/enrollments/<int:student_id>', methods=['GET'])
def get_student_enrollments(student_id):
    """Get enrollments for a student"""
    try:
        connection = get_db_connection()
        if connection is None:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT id, subject, tutor_name, enrolled_date
            FROM enrollments
            WHERE student_id = ?
            ORDER BY enrolled_date DESC
        """, (student_id,))
        
        enrollments = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify([dict(row) for row in enrollments]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sessions', methods=['POST'])
def book_session():
    """Book a tutoring session"""
    try:
        data = request.get_json()
        student_id = data.get('student_id')
        tutor_name = data.get('tutor_name')
        date_time = data.get('date_time')
        duration_hours = data.get('duration_hours', 1)
        notes = data.get('notes', '')
        
        if not all([student_id, tutor_name, date_time]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        connection = get_db_connection()
        if connection is None:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor()
        
        try:
            # Verify student exists
            cursor.execute("SELECT id FROM students WHERE id = ?", (student_id,))
            if not cursor.fetchone():
                return jsonify({'error': 'Student not found'}), 404
            
            # Insert session
            cursor.execute("""
                INSERT INTO tutoring_sessions (student_id, tutor_name, date_time, duration_hours, notes)
                VALUES (?, ?, ?, ?, ?)
            """, (student_id, tutor_name, date_time, duration_hours, notes))
            
            connection.commit()
            session_id = cursor.lastrowid
            
            cursor.close()
            connection.close()
            
            return jsonify({
                'message': 'Session booked successfully',
                'session_id': session_id
            }), 201
            
        finally:
            cursor.close()
            connection.close()
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok'}), 200

@app.route('/api/students', methods=['GET'])
def get_all_students():
    """Get all students (admin endpoint)"""
    try:
        connection = get_db_connection()
        if connection is None:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT id, email, first_name, last_name, phone, created_at 
            FROM students 
            ORDER BY created_at DESC
        """)
        
        students = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify([dict(row) for row in students]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    """Request password reset"""
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        connection = get_db_connection()
        if connection is None:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor()
        
        # Find student by email
        cursor.execute("SELECT id, email, first_name FROM students WHERE email = ?", (email,))
        student = cursor.fetchone()
        
        if not student:
            # Don't reveal if email exists (security best practice)
            return jsonify({'message': 'If an account exists with this email, a reset link has been sent'}), 200
        
        # Generate reset token
        reset_token = secrets.token_urlsafe(32)
        
        # Calculate expiration time (24 hours from now)
        expires_at = datetime.now() + timedelta(hours=24)
        
        # Store token in database
        cursor.execute("""
            INSERT INTO password_reset_tokens (student_id, token, expires_at)
            VALUES (?, ?, ?)
        """, (student['id'], reset_token, expires_at.isoformat()))
        
        connection.commit()
        cursor.close()
        connection.close()
        
        # Send email with reset link
        scheme = 'https' if request.host.endswith('.onrender.com') or request.host.endswith('.railway.app') else 'http'
        reset_url = f"{scheme}://{request.host}/reset-password.html?token={reset_token}"
        
        email_body = f"""
        <html>
          <body style="font-family: Arial, sans-serif;">
            <h2>Password Reset Request</h2>
            <p>Hello {student['first_name']},</p>
            <p>We received a request to reset your password. Click the link below to set a new password:</p>
            <p><a href="{reset_url}" style="background-color: #dc2626; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">Reset Password</a></p>
            <p>Or copy and paste this link in your browser:</p>
            <p>{reset_url}</p>
            <p><strong>This link will expire in 24 hours.</strong></p>
            <p>If you did not request a password reset, please ignore this email.</p>
            <p>Best regards,<br>ChinaBridge Academy Team</p>
          </body>
        </html>
        """
        
        send_email(email, 'Password Reset Request - ChinaBridge Academy', email_body, is_html=True)
        
        return jsonify({'message': 'If an account exists with this email, a reset link has been sent'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reset-password', methods=['POST'])
def reset_password():
    """Reset password with token"""
    try:
        data = request.get_json()
        token = data.get('token')
        new_password = data.get('password')
        
        if not token or not new_password:
            return jsonify({'error': 'Token and password are required'}), 400
        
        if len(new_password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        connection = get_db_connection()
        if connection is None:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor()
        
        # Find valid token
        cursor.execute("""
            SELECT id, student_id, expires_at, used FROM password_reset_tokens 
            WHERE token = ?
        """, (token,))
        
        reset_record = cursor.fetchone()
        
        if not reset_record:
            cursor.close()
            connection.close()
            return jsonify({'error': 'Invalid or expired reset token'}), 400
        
        if reset_record['used']:
            cursor.close()
            connection.close()
            return jsonify({'error': 'This reset link has already been used'}), 400
        
        # Check if token is expired
        expires_at = datetime.fromisoformat(reset_record['expires_at'])
        if datetime.now() > expires_at:
            cursor.close()
            connection.close()
            return jsonify({'error': 'Reset link has expired'}), 400
        
        # Hash new password
        hashed_password = generate_password_hash(new_password)
        
        # Update student password
        student_id = reset_record['student_id']
        cursor.execute("""
            UPDATE students SET password = ? WHERE id = ?
        """, (hashed_password, student_id))
        
        # Mark token as used
        cursor.execute("""
            UPDATE password_reset_tokens SET used = 1 WHERE id = ?
        """, (reset_record['id'],))
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({'message': 'Password reset successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Run Flask app (debug only in development)
    app.run(debug=DEBUG_MODE, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
