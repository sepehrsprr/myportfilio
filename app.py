from flask import Flask, render_template, request, flash, redirect, url_for
import os
from flask_mail import Mail, Message
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

# Secret key for flash messages
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')

# Configure upload folder
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize Flask-Mail
mail = Mail(app)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    # Add your projects data here
    projects = [
        {
            'title': 'Tic-Tac-Toe',
            'description': """The Tic-Tac-Toe project is a classic game developed using Python. The game provides an interactive user
interface and allows two players to compete against each other on a digital board""",
            'images': ['project1-1.jpg'],
            'github_url': 'https://github.com/sepehrsprr',
        },
        {
            'title': 'ToDo App',
            'description': """"The ToDO App is a simple yet effective Django-based application used to manage to-do lists. It offers 
features such as adding, editing, and deleting tasks to help streamline everyday organization""",
            'images': ['project2-1.jpg', 'project2-2.jpg'],
            'github_url': 'https://github.com/sepehrsprr',
        },
        {
            'title': 'Berliner Shop',
            'description': """The E-Commerce project is an online shop developed using Django, HTML, and CSS. It aims to enhance my 
programming skills and tackle challenges in web development, particularly in user management and 
shopping cart functionality.""",
            'images': ['project3-1.png', 'project3-2.png'],
            'github_url': 'https://github.com/sepehrsprr',
        }
    ]
    return render_template('index.html', projects=projects)

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        msg = Message(
            subject=f"Portfolio Contact: {subject}",
            recipients=[app.config['MAIL_USERNAME']],
            body=f"""
            From: {name} <{email}>
            
            {message}
            """
        )
        
        mail.send(msg)
        flash('Your message has been sent successfully!', 'success')
    except Exception as e:
        print(f"Error sending email: {str(e)}")  # For debugging
        flash('An error occurred while sending your message. Please try again.', 'error')
    
    return redirect(url_for('home', _anchor='contact'))

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.getenv('PORT', 5002))
    app.run(host="0.0.0.0", port=port, debug=False)