from flask import Flask, render_template, request, flash, redirect, url_for
import os
from flask_mail import Mail, Message
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Email configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
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
        },
        {
            'title': 'YT Downloader',
            'description': """The YT Downloader is a Python project that uses the Tkinter library to create a GUI application for 
downloading video and audio from YouTube. It provides a user-friendly interface for entering links and 
managing downloads easily.""",
            'images': ['project4.png'],
            'github_url': 'https://github.com/sepehrsprr',
        },
        {
            'title': 'leaning partner system',
            'description': """it is a system that helps students to find a partner to study with.
            it is one of my first ever projects that I have done in my life.
            used custom TKinter library to create the GUI""",
            'images': ['project5.png', 'project5-2.png'],
            'github_url': 'https://github.com/sepehrsprr',
        }
    ]
    return render_template('index.html', projects=projects)

@app.route('/send_message', methods=['POST'])
def send_message():
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']
    
    msg = Message(subject, sender=email, recipients=[os.getenv('MAIL_USERNAME')])
    msg.body = f"From: {name} <{email}>\n\n{message}"
    
    try:
        mail.send(msg)
        flash('Message sent successfully!', 'success')
    except Exception as e:
        flash(f'Failed to send message: {str(e)}', 'danger')
    
    return redirect(url_for('home', _anchor='contact'))

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.getenv('PORT', 5002))
    app.run(host="0.0.0.0", port=port, debug=False)