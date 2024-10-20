from .app import db
from flask_login import UserMixin
from .app import login_manager

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)

livre_favoris = db.Table('livre_favoris',
    db.Column('user_id', db.String(50), db.ForeignKey('user.username'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(64))
    favoris = db.relationship('Book', secondary=livre_favoris, lazy='subquery', backref='favorited_by')

    
    def get_id(self):
        if isinstance(self, User):
            return self.username
        else:
            raise AttributeError("L'objet n'est pas une instance de User.")
    

class Author(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100))
    books = db.relationship('Book', back_populates='author', lazy=True)
    
    def __repr__ (self ):
        return "<Author (%d) %s>" % (self.id , self.name)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    price = db.Column(db.Float)
    url = db.Column(db.String(200))
    image = db.Column(db.String(200))
    title = db.Column(db.String(100))
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    author = db.relationship('Author', back_populates='books')
    def __repr__ (self):
        return "<Book (%d) %s>" % (self.id , self.title)

def get_sample():
    return Book.query.limit(10).all() 

def get_author(id):
    return Author.query.get(id) 

def get_book(id):
    return Book.query.get(id) 

def get_book_from_author(author_name):
    author = Author.query.filter(Author.name.ilike(f'%{author_name}%')).first()
    if author:
        return author.books
    else:
        return []
