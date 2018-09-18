from datetime import datetime
from flask import Flask, session 
from flask_session import Session
from flask_sessionstore import SqlAlchemySessionInterface
from flask import request, render_template, redirect, url_for, escape
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
    # create and configure the app

app = Flask(__name__,)
Bootstrap(app)
app.config['SECRET_KEY'] = 'Thisisssecret!'
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///Users/alexandralee/Rendu/Coding-Academy/Python-Flask-API-articles/Flask_D02/LegalTech.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
Session(app)
SqlAlchemySessionInterface(app, db, "sessions", "S", use_signer=False,
             permanent=True)
@app.route('/set/')
def set():
    session['key'] = 'value'
    return 'ok'

@app.route('/get/')
def get():
    return session.get('key', 'not set')
  
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=5, max=20)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=20)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=5, max=20)])    

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80))
    def __repr__(self):
        return '<User %r>' % self.username

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(30), nullable=False)
    written_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)    
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    user = db.relationship('User',
        backref=db.backref('articles', lazy=True))

    def __repr__(self):
        return '<Post %r>' % self.title

class  Comment(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  commentator_id = db.Column(db.Integer, nullable=False)
  article_id = db.Column(db.Integer, nullable=False)
  content = db.Column(db.Text, nullable=False) 
  date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/index")
def index():
    return render_template('index.html') 

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                return redirect(url_for('articles'))
        return '<h1>Invalid username or password</h1>'
    return render_template('login.html', form=form)

# @app.before_request
# def csrf_protect():
#     session = Session()
#     if request.method == "POST":
#         token = session.pop('_csrf_token', None)
#         if not token or token != request.form.get('_csrf_token'):
#             abort(403)

# def generate_csrf_token():
#     if '_csrf_token' not in session:
#         session['_csrf_token'] = some_random_string()
#     return session['_csrf_token']

# app.jinja_env.globals['csrf_token'] = generate_csrf_token
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return '<h1> You have successfully registered </h1>'
    return render_template('register.html', form=form)

@app.route("/users", methods=["GET", "POST"])
def users():
    return render_template('users.html')

@app.route("/articles", methods=["GET", "POST"])
def articles():
    return render_template('articles.html')



@app.route("/add", methods=["GET", "POST"])
def add():
    return render_template('add.html')

@app.route("/addArticle", methods=["POST"])
def addArticle():
    author = request.form['author']
    date = datetime.strptime(request.form['date'], "%d/%m/%y")
    title = request.form['title']
    content = request.form['content']
    article = Article(author=author, written_date=date, title=title, content=content, date_posted=datetime.now())
    db.session.add(article)
    db.session.commit()
    return redirect(url_for('articles'))

@app.route('/comment')
def comment():
    return render_template('comment.html')

@app.route("/about", methods=["GET", "POST"])
def about():
    return render_template('about.html')

@app.route("/contact", methods=["GET", "POST"])
def contact():
    return render_template('contact.html')    

if (__name__ == "__main__"):
    app.run(debug=True)  
