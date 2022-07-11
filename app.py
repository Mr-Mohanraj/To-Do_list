from flask import Flask, request
from flask import redirect,url_for
from flask import render_template

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class TODO(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    # plan = db.Column(db.String(100))
    # add_time = db.Column(db.String(20))
    complete = db.Column(db.Boolean)


@app.route('/add', methods=["POST"])
def add():
    title = request.form.get("title")
    print(title)
    if title == " ":
        return redirect(url_for('error'))
    new_todo = TODO(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("todo"))


@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo = TODO.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('todo'))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = TODO.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('todo'))


@app.route('/')
def todo():
    todo_list = TODO.query.all()
    return render_template('index.html', todo_list=todo_list)


@app.route('/error')
def error():
    error = "empty string!!"
    return render_template('error.html', error=error)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
