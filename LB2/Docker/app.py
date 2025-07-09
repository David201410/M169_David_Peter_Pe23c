from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.create_all() 

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(1000), nullable=False)
    complete = db.Column(db.Boolean) 
    user_id = db.Column(db.Integer)

@app.route('/')
def index():

    todoList = Todo.query.all()
    return render_template('base.html', todo_list=todoList)


# Task hinzufügen
@app.route('/add', methods=["POST"])
def add():
    
    # Tasknamen aus dem Formular holen
    title = request.form.get("title")

    # Wenn der Titel leer ist, zurück zur Startseite
    if title == "":
        return redirect(url_for("index"))
    # Erstelle ein neues Todo-Objekt
    newTask = Todo(task=title, complete=False)

    # Versuche, das Objekt in die Datenbank hinzuzufügen
    try:
        db.session.add(newTask)
        db.session.commit()
        return redirect(url_for("index"))
    except:
        return "Es gab ein Problem beim erstellen des Tasks."


# einen task löschen
@app.route('/delete/<int:todo_id>')
def delete(todo_id):

    # den task in der Datenbank suchen
    task = Todo.query.filter_by(id=todo_id).first()
    
    try:
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for("index"))
    except:
        return "Task kann nicht gelöscht werden."


# task löschen
@app.route('/update/<int:todo_id>')
def update(todo_id):

    # den task in der Datenbank suchen
    task = Todo.query.filter_by(id=todo_id).first()
    # toggle the complete value
    task.complete = not task.complete

    # versuche in die db zu schreiben
    try:
        db.session.commit()
        return redirect(url_for("index"))
    except:
        return "Task kann nicht gelöscht werden."


if __name__ == "__main__":
    
    db.create_all()
    port = int(os.environ.get('PORT', 5000))

    app.run(host = '0.0.0.0', port = port)















    '''




'''
