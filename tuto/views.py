from .app import app
from flask import render_template
from .models import get_sample, get_author, get_book
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
from wtforms import SelectField
from wtforms.validators import DataRequired
from flask import url_for, redirect
from .app import db
from wtforms import PasswordField
from .models import User
from .models import Author
from .models import Book
from hashlib import sha256
from flask_login import login_user, current_user
from flask import request
from flask_login import logout_user
from flask_login import login_required

class loginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    next = HiddenField()
    def get_authenticated_user(self):
        user = User.query.get(self.username.data)
        if user is None:
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return user if passwd == user.password else None

class AuthorForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('Nom', validators=[DataRequired()])
    author = SelectField('Choisir un auteur', validators=[DataRequired()])
    
class NewAuthorForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('Nom', validators=[DataRequired()])
    
class NewBookForm(FlaskForm):
    id = HiddenField('id')
    price = StringField('Prix', validators=[DataRequired()])
    title = StringField('Titre', validators=[DataRequired()])
    author = SelectField('Auteur', validators=[DataRequired()])

@app.route ("/")
def home():
    return render_template(
        "home.html",
        title="Bibliothèque",
        books=get_sample())
    
    
@app.route ("/name")
def show_name():
    return render_template(
        "home.html",
        title="name",
        names=["Pierre", "Jean", "Axel"]) 
    
@app.route("/detail/<id>")
def detail(id):
    books = get_sample()
    book = books[int(id)]
    return render_template(
    "detail.html",
    b=book)
    
@app.route("/edit-author/<int:id>")
@login_required
def edit_author(id):
    a = get_author(id)
    f = NewAuthorForm(id=a.id, name=a.name)
    return render_template(
        "edit-author.html",
        author=a, form = f)
    
@app.route("/save/edit/author/", methods =("POST" ,))
def save_edit_author():
        a = None
        f = NewAuthorForm()
        if f.validate_on_submit():
            id = int(f.id.data)
            a = get_author(id)
            a.name = f.name.data
            db.session.commit()
            return redirect(url_for('home'))
        a = get_author(int(f.id.data))
        return render_template(
            "edit-author.html",
            author =a, form=f)

@app.route("/new/author/")
@login_required
def new_author():
    form = NewAuthorForm()
    return render_template("new-author.html", form=form)
          
@app.route("/new/author/", methods =("POST" ,))
@login_required
def save_new_author():
        author = None
        form = NewAuthorForm()
        if form.validate_on_submit():
            author = Author(name=form.name.data)
            db.session.add(author)
            db.session.commit()
            return redirect(url_for('/', id=author.id))
        
        return render_template("new-author.html", form = form)

@app.route("/delete/author/")
@login_required
def delete_author():
    a = Author.query.all()
    form = AuthorForm()
    form.name.choices = [(author.id, author.name) for author in a]
    return render_template("delete-author.html", authors=a, form=form)

@app.route("/delete/author/", methods=("POST",))
@login_required
def save_delete_author():
    form = AuthorForm()
    authors = Author.query.all()
    form.name.choices = [(author.id, author.name) for author in authors]
    author_id = form.id.data
    
    if form.validate_on_submit():
        
        author = Author.query.get(author_id)
        if author:
            db.session.delete(author)
            db.session.commit()
            return redirect(url_for('/'))
    return render_template("delete-author.html", form=form)

@app.route("/edit-book/<int:id>")
@login_required
def edit_book(id):
    b = get_book(id)
    f = NewBookForm(id=b.id, price=b.price, title=b.title, author=b.author)
    return render_template(
        "edit-book.html",
        book = b, form = f)
    
@app.route("/save/edit/book/", methods =("POST" ,))
def save_edit_book():
        b = None
        f = NewBookForm()
        if f.validate_on_submit():
            id = int(f.id.data)
            b = get_author(id)
            b.price = f.price.data
            b.title = f.title.data
            b.author = f.author.data
            db.session.commit()
            return redirect(url_for('home'))
        a = get_author(int(f.id.data))
        return render_template(
            "edit-book.html",
            author =a, form=f)
        
@app.route("/login/",methods=("GET","POST" ,))
def login():
    f = loginForm()
    if not f.is_submitted():
        f.next.data = request.args.get("next")
    elif f.validate_on_submit():
        user = f.get_authenticated_user()
        if user:
            login_user(user)
            next = f.next.data or url_for("home")
            return redirect(next)
    return render_template("login.html", form=f)


@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for('home'))

# denys baz