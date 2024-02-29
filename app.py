from datetime import datetime
import os
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail  import Mail, Message

app = Flask( __name__ )

"""Specifying a series of parameter using app.config, which is a dictionary
and out of this dictionary we should access the keys of this dictionary 
So, app.config is dictipnary
secret key for signing cookies and sessions
"""
app.config["SECRET_KEY"] = "myapplication123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db" # SQLite database file on disk
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"]  = "suryaprakashsharma453@gmail.com"
app.config['MAIL_PASSWORD'] = "aoyx jiql haex uaye"

db = SQLAlchemy(app)

mail =  Mail(app)


class FormDatabase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(120))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(50))


@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        occupation = request.form["occupation"]

        form = FormDatabase(first_name = first_name, last_name = last_name,
                            email = email, date = date_obj, occupation = occupation)
        db.session.add(form)
        db.session.commit()

        message_body = f"Thank you for your submission {first_name}." \
                       f"We get your data " \
                       f"We connect you soon if your qualification and skill are matching with our requirements!" \
                       f"Thanks a lot!"
        message = Message(subject = "New from submission", sender = app.config["MAIL_USERNAME"],
                          recipients=[email], body = message_body)
        mail.send(message)

        flash(f"{first_name}, Your information has been recorded!", "success")


        
    return render_template("index.html", title="Home")


if __name__ == "__main__":
    with  app.app_context():
        db.create_all()
        app.run(debug = True, port = 5001)
