from .app import app
from flask import render_template
from .models import get_sample, get_author
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
from wtforms.validators import DataRequired
from flask import url_for, redirect
from .app import db
from wtforms import PasswordField
from .models import User
from .models import Author
from hashlib import sha256
from flask_login import login_user, current_user
from flask import request
from flask_login import logout_user
from flask_login import login_required

class loginFrom(FlaskForm):
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
    
    
@app.route ("/sample")
def sample():
    return render_template(
        "home.html",
        title="My Books !",
        books=get_sample())
    
    
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
            return redirect(url_for('sample', id=a.id))
        a = get_author(int(f.id.data))
        return render_template(
            "edit-author.html",
            author =a, form=f)

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
            return redirect(url_for('/', id=author.id))
        
        return render_template("new-author.html", form = form)

@app.route("/delete/author/")
@login_required
def delete_author():
    form = AuthorForm()
    a = Author.query.all()
    form.name.choices = [(author.id, author.name) for author in a]
    return render_template("delete-author.html", form=form)

@app.route("/delete/author/", methods=("POST",))
@login_required
def save_delete_author():
    form = AuthorForm()
    authors = Author.query.all()
    form.name.choices = [(author.id, author.name) for author in authors]

    if form.validate_on_submit():
        author_id = form.name.data
        author = Author.query.get(author_id)
        if author:
            db.session.delete(author)
            db.session.commit()
            return redirect(url_for('/'))
    return render_template("delete-author.html", form=form)


        
@app.route("/login/",methods=("GET","POST" ,))
@login_required
def login():
    f = loginFrom()
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