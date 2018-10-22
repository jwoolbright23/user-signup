from flask import Flask, redirect, request
import cgi
import os
import jinja2
import re

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/")
def index():
    template = jinja_env.get_template("index_form.html")
    return template.render()

@app.route("/", methods = ["POST"])
def user_signup():
    template_go = jinja_env.get_template("index_form.html")
    template_now = jinja_env.get_template("welcome_form.html")

    username = request.form["username"]
    password = request.form["password"]
    verify = request.form["verify"]
    email = request.form["email"]

    username_error = ""
    password_error = ""
    verify_error = ""
    email_error = ""

    if username == "":
        username_error = "You must enter a valid Username."
    elif len(username) > 20 or len(username) <= 3:
        username_error = "Your username must be bettwen 3 and 20 characters."
        username = ""
    elif " " in username:
        username_error = "You cannot use spaces in your Username."
        username = ""
    
    if password == "":
        password_error = "You must enter a valid password."
    elif len(password) > 20 or len(password) < 3:
        password_error = "Your password must be between 3 and 20 characters."
    elif " " in password:
        password_error = "You cannot have spaces in your password"

    if verify == "" or verify != password:
        verify_error = "Your passwords do not match."
        verify = ""
    
    if email != "":
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            email_error = "You must enter a valid email"
    
    if not username_error and not password_error and not verify_error and not email_error:
        return template_now.render(username = username)
    else:
        return template_go.render(
        username = username,
        username_error = username_error,
        password_error = password_error,
        verify_error = verify_error,
        email = email,
        email_error = email_error
        )



app.run()   

