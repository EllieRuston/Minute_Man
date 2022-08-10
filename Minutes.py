from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, send_from_directory, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm #forms
from wtforms import StringField, PasswordField, BooleanField, EmailField
from wtforms.validators import DataRequired, Email, Length, InputRequired, EqualTo, email_validator
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user 


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///Minutes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']= 'my super secret key that no one is supposed to know'
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

#database
class User (UserMixin, db.Model):
    user_ID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    m_details = db.relationship('M_details', backref='user')
 
@login_manager.user_loader
def load_user(user_ID):
    return User.query.get(int(user_ID))

#Form Class
class LoginForm(FlaskForm):
    username = StringField("username", validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField ("password", validators=[InputRequired(), Length(min=8, max=80)])

class RegForm(FlaskForm):
    username =  StringField('username',validators=[Length(min=4, max=25)])
    email = EmailField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[DataRequired(),
            EqualTo('confirm', message='Passwords must Match')])
    confirm = PasswordField('Repeat Password')
 

# Normalised tables for meeting data
class M_details (UserMixin, db.Model):
    min_ID = db.Column(db.Integer, primary_key=True)
    user_ID = db.Column(db.Integer, db.ForeignKey('user.user_ID'))
    title = db.Column(db.String(25), nullable=False)
    date = db.Column(db.DateTime(10), default=datetime.now)
    start_T = db.Column(db.DateTime(5), nullable=False)
    end_T = db.Column(db.DateTime(5), nullable=False)
    a_present = db.Column(db.String(), nullable=False)
    a_absent = db.Column(db.String(), nullable=True)
    m_topic = db.relationship('M_topic', backref='M_details')
    
class M_topic(UserMixin, db.Model):
    min_ID = db.Column(db.Integer, db.ForeignKey('M_details.min_ID'))
    topic_ID = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(50), nullable=True)
    raised_by = db.Column(db.String(), nullable=False)
    m_action = db.relationship('M_action', backref='M_topic')
    
class M_action(UserMixin, db.Model):
    topic_ID = db.Column(db.Integer, db.ForeignKey('M_topic.topic_ID'))
    action_ID= db.Column(db.Integer, primary_key = True)
    action = db.Column(db.String(), nullable=False)
    person_R = db.Column(db.String(), nullable=False)
    extra_data = db.Column(db.String(), nullable=True)
    deadline = db.Column(db.DateTime(), nullable=False) 

#images
@app.route('/images/<path:path>')
def images(path):
    return send_from_directory('images', path)

#Views
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return '<h1>' + form.username.data + '' + form.password.data + '</h1>'
    return render_template('Login.html', form=form)
    
@app.route('/register')
def register():
    form = RegForm()
    if form.validate_on_submit():
        return '<h1>'+ form.email.data + '' + form.username.data + '' + form.password.data + '</h1>'
    return render_template('Register.html', form=form)

@app.route('/home')
def home():
    return render_template('Home.html')

@app.route('/search')
def search_page():
    items = RegForm.query.all()
    return render_template('Search.html', items=items)

# @app.route('/login', methods=['GET', 'Post'])
# def register():
#     form = RegForm(request.form)
#     if request.method == 'POST' and form.validate():
#         user = User(form.username.data, form.email.data, form.password.data)
#         db.session.add(user)
#         flash('Thanks for Registering')
#         return redirect(url_for('login'))
#     return render_template('login.html', form=form)

