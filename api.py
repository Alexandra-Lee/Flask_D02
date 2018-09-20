from datetime import datetime
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
api = Api(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/alexandralee/Rendu/Coding-Academy/Python-Flask-API-articles/Flask_D02/legalTech.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80))
    occupation = db.Column(db.String(30), nullable=True)
    country = db.Column(db.String(40), nullable=True)
    
    def __init__(self, username, occupation, country):
        self.username = username
        self.email = email
        self.password = password
        self.occupation = occupation
        self.country = country

class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('username', 'occupation', 'country')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(30), nullable=False)
    written_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)    
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=True)
    user = db.relationship('User',
        backref=db.backref('articles', lazy=True))

    def __init__(self, title, author, written_date, content, date_posted):
            self.title = title
            self.author = author
            self.written_date = written_date
            self.content = content
            self.user_id = user_id

class ArticleSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('title', 'author', 'written_date', 'content', 'date_posted')

article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)      

# endpoint to create new user
@app.route("/login")
    return jsonify(user) {"user": "username"}

@app.route("/article", methods=["POST"])
def add_article():
    title = request.json['title']
    author = request.json['author']
    written_date = request.json['written_date']
    content = request.json['content'
    ]
    new_article = Article(title, author, written_date, content, user_id, date_posted)

    db.session.add(new_article)
    db.session.commit()

    return jsonify(new_article)


# endpoint to show all users
@app.route("/article", methods=["GET"])
def get_article():
    all_articles = Article.query.all()
    result = articles_schema.dump(all_articles)
    return jsonify(result.data)


# endpoint to get user detail by id
@app.route("/article/<id>", methods=["GET"])
def article_detail(id):
    article = Article.query.get(id)
    return article_schema.jsonify(article)


# endpoint to update user
@app.route("/article/<id>", methods=["PUT"])
def article_update(id):
    article = Article.query.get(id)
    title = request.json['title']
    author = request.json['author']
    written_date = request.json['written_date']
    content = request.json['content']

    article.title = title
    article.author = author
    article.written_date = written_date
    article.content = content
    article.date_posted = datetime.utcnow

    db.session.commit()
    return article_schema.jsonify(article)


# endpoint to delete user
@app.route("/article/<id>", methods=["DELETE"])
def article_delete(id):
    article = Article.query.get(id)
    db.session.delete(article)
    db.session.commit()

    return article_schema.jsonify(article)

if __name__ == '__main__':
    app.run(debug=True)
