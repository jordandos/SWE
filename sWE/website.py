# Import necessary libraries and modules
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize Flask application
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Configure the database (use SQLite in this example)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/ightnow/dayz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define database models (replace 'User', 'Course', and 'Advisor' with your actual models)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    courses = db.relationship('Course', backref='user', lazy=True)  # Relationship with Course model

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(120), nullable=False)
    prerequisites = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key relationship

class Advisor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
# Define routes and endpoints
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login form submission
        data = request.form
        username = data.get('username')
        password = data.get('password')
        is_admin = 'admin' in data  # Check if the 'admin' checkbox is selected

        # Your login logic here
        # Example: Check credentials and user type
        user = User.query.filter_by(username=username, password=password).first()
        advisor = Advisor.query.filter_by(username=username, password=password).first()

        if user:
            user_type = 'student'
            if is_admin:
                user_type = 'admin'
            return jsonify({'message': 'Login successful', 'user_type': user_type}), 200
        elif advisor:
            return jsonify({'message': 'Login successful', 'user_type': 'advisor'}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401

    # Render the login form for GET requests
    return render_template('login.html')


@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()

        # Check if the username is already taken
        if User.query.filter_by(username=data['username']).first() or Advisor.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username is already taken'}), 400

        # Create a new user or advisor in the database based on user_type
        if data['user_type'] == 'student':
            new_user = User(username=data['username'], password=data['password'])
            db.session.add(new_user)
        elif data['user_type'] == 'advisor':
            new_advisor = Advisor(username=data['username'], password=data['password'])
            db.session.add(new_advisor)

        db.session.commit()
        return jsonify({'message': 'Registration successful'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.session.close()

@app.route('/courses', methods=['GET'])
def get_courses():
    try:
        # Fetch and return a list of courses from the database
        courses = Course.query.all()
        return render_template('index.html', course=courses)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/user_profile', methods=['GET'])
def get_user_profile():
    try:
        data = request.get_json()

        # Fetch user profile information based on username
        user = User.query.filter_by(username=data['username']).first()
        if user:
            user_profile = {
                'username': user.username,
                'courses': [{'course_name': course.course_name, 'prerequisites': course.prerequisites} for course in user.courses]
            }
            return jsonify({'user_profile': user_profile}), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/advisor_profile', methods=['GET'])
def get_advisor_profile():
    try:
        data = request.get_json()

        # Fetch advisor profile information based on username
        advisor = Advisor.query.filter_by(username=data['username']).first()
        if advisor:
            advisor_profile = {
                'username': advisor.username,
                'students': [user.username for user in User.query.all()]  # Get all students for simplicity
            }
            return jsonify({'advisor_profile': advisor_profile}), 200
        else:
            return jsonify({'error': 'Advisor not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload_resource', methods=['POST'])
def upload_resource():
    try:
        data = request.get_json()

        # Save uploaded resource to the database or file system
        # (Implementation details depend on where and how you want to store the resources)
        # For simplicity, we'll just return a success message here
        return jsonify({'message': 'Resource uploaded successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def populate_database():
    # Check if the sample user already exists
    existing_user = User.query.filter_by(username='sample_user').first()

    # If the user doesn't exist, create and add it to the database
    if not existing_user:
        sample_user = User(username='sample_user', password='password')
        db.session.add(sample_user)

        # Sample courses for the sample user
        cs_courses = [
            {'course_name': 'Introduction to Computer Science', 'prerequisites': None},
            {'course_name': 'Data Structures and Algorithms', 'prerequisites': 'Introduction to Computer Science'},
            {'course_name': 'Database Management Systems', 'prerequisites': 'Data Structures and Algorithms'},
            {'course_name': 'Operating Systems', 'prerequisites': 'Data Structures and Algorithms'},
            {'course_name': 'Computer Networks', 'prerequisites': 'Data Structures and Algorithms'},
            # Add more courses as needed
        ]

        # Add computer science courses associated with the sample user to the database
        for course_data in cs_courses:
            course = Course(course_name=course_data['course_name'], prerequisites=course_data['prerequisites'], user_id=sample_user.id)
            db.session.add(course)

        # Commit changes to the database
        db.session.commit()



@app.route('/')
def index():
    return render_template('index.html')

# Check if the script is run directly
if __name__ == '__main__':
    # Run the database creation and population script
    with app.app_context():
        db.create_all()
        populate_database()

    # Run the Flask application
    app.run(debug=True)
