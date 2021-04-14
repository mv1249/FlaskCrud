from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# creating a database class


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    desc = db.Column(db.String(555), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

#    repr method is used for representing the string,its a built in method used in python!

    def __repr__(self):
        return f"{self.sno}-{self.title}"


@app.route('/', methods=['GET', 'POST'])
def hello_world():

    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']

        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)


# here in this delete we want to delete an record,so from the frontend,we have the delete button mapped with "delete/sno",so here the sno is the int,so we have to get even that,so that is why "<int:sno>" is used!,so for deleting first get that record which we wanna delete,by using Query.filter_by,then once we get that record we will simply run "db.session.delete(<record_selected_after_filtering>)",then we commit!

@app.route('/delete/<int:sno>')
def delete(sno):

    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect('/')


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)


if __name__ == "__main__":
    app.run(debug=True)
