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
    
class DelAuthorForm(FlaskForm):
    id = HiddenField('id')
    name = HiddenField('Nom', validators=[DataRequired()])
    
class NewBookForm(FlaskForm):
    id = HiddenField('id')
    title = StringField('Titre', validators=[DataRequired()])
    price = StringField('Prix', validators=[DataRequired()])

class DelBookForm(FlaskForm):
    id = HiddenField('id')
    title = HiddenField('Titre', validators=[DataRequired()])
    price = HiddenField('Prix', validators=[DataRequired()])

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

@app.route('/search', methods=['GET'])
def search():
    recherche = request.args.get('query')
    authors = Author.query.filter(Author.name.ilike(f'%{query}%')).all()
    if authors:
        author_id = [author.id for author in authors]
        books = Book.query.filter(Book.author_id.in_(author_ids)).all()
    else:
        books = []

    return render_template('Search.html', author=authors, books=books)
    
@app.route("/detail/<id>")
def detail(id):
    books = get_sample()
    book = books[int(id)]
    return render_template(
    "detail.html",
    b=book)
    
@app.route("/list-author/")
def author():
    authors = Author.query.all()
    return render_template(
    "listeAuthor.html",
    author=authors)

@app.route("/new/author/")
@login_required
def new_author():
    form = AuthorForm()
    return render_template("new-author.html", form=form)
          
@app.route("/new/author/", methods =("POST" ,))
@login_required
def save_new_author():
        author = None
        form = AuthorForm()
        if form.validate_on_submit():
            author = Author(name=form.name.data)
            db.session.add(author)
            db.session.commit()
            return redirect(url_for('home', id=author.id))
        
        return render_template("new-author.html", form = form)
        
@app.route("/edit-author/<int:id>")
@login_required
def edit_author(id):
    a = get_author(id)
    f = AuthorForm(id=a.id, name=a.name)
    return render_template(
        "edit-author.html",
        author=a, form = f)
    
@app.route("/save/edit/author/", methods =("POST" ,))
def save_edit_author():
        a = None
        f = AuthorForm()
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

@app.route("/delete/author/<int:id>")
@login_required
def delete_author(id):
    a = get_author(id)
    form = DelAuthorForm(id=a.id, name=a.name)
    return render_template("delete-author.html", author=a, form=form)

@app.route("/save/delete/author/", methods=("POST",))
@login_required
def save_delete_author():
    a = None
    form = DelAuthorForm()
    if form.validate_on_submit():
        id = int(form.id.data)
        a = get_author(id)
        if a:
            db.session.delete(a)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template("delete-author.html", form=form, author=a)

@app.route("/edit-book/<int:id>")
@login_required
def edit_book(id):
    b = get_book(id)
    f = NewBookForm(id=b.id, title=b.title, price=b.price)
    return render_template(
        "edit-book.html",
        book = b, form = f)
    
@app.route("/save/edit/book/", methods =("POST" ,))
def save_edit_book():
        b = None
        f = NewBookForm()
        if f.validate_on_submit():
            id = int(f.id.data)
            b = get_book(id)
            b.title = f.title.data
            b.price = f.price.data
            db.session.commit()
            return redirect(url_for('home'))
        a = get_book(int(f.id.data))
        return render_template(
            "edit-book.html",
            book = b, form=f)
        
@app.route("/delete/book/<int:id>")
@login_required
def delete_book(id):
    b = get_book(id)
    form = DelBookForm(id=b.id, title=b.title, price=b.price)
    return render_template("delete-book.html", book=b, form=form)

@app.route("/save/delete/book/", methods=("POST",))
@login_required
def save_delete_book():
    b = None
    form = DelBookForm()
    if form.validate_on_submit():
        id = int(form.id.data)
        b = get_book(id)
        if b:
            db.session.delete(b)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template("delete-book.html", form=form, book=b)
        
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