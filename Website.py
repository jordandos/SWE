from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Read the database URI from the text file
with open('text.txt', 'r') as file:
    db_uri = file.read().strip()

# Configure the Flask app with the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

# Suppress a warning message
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create a SQLAlchemy database instance
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
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        # Validate user credentials
        user = User.query.filter_by(username=data['username'], password=data['password']).first()
        advisor = Advisor.query.filter_by(username=data['username'], password=data['password']).first()

        if user:
            return jsonify({'message': 'Login successful', 'user_type': 'student'}), 200
        elif advisor:
            return jsonify({'message': 'Login successful', 'user_type': 'advisor'}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
        course_list = [{'course_name': course.course_name, 'prerequisites': course.prerequisites} for course in courses]
        return jsonify({'courses': course_list}), 200
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
        # return jsonify({'message': 'Resource uploaded successfully'}), 200

        #returns the upload html page to upload resources
        return render_template('upload.html')
    except Exception as e:
        return jsonify({'error': str(e)}), 500
