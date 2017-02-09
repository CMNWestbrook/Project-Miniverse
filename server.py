"""Project Miniverse"""

from jinja2 import StrictUndefined  # makes StrictUndefined work below

# Makes all the flask commands work
from flask import Flask, redirect, session, render_template, request, flash
# This imports the debug toolbar witch will give useful error messages
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Model3d, Favorite, UserImage


app = Flask(__name__)
# Need this to use Flask sessions and super useful Flask debugging errors
app.secret_key = "soVewyVewySecretDoc"

# Initiates error if undefined variable in Jinja
app.jinja_env.undfined = StrictUndefined


@app.route('/')
def index():
    """Homepage"""

    return render_template('homepage.html')

@app.route('/register', methods=['GET'])
def register_form():
    """Shows the form for registering for an account"""

    return render_template("register_form.html")

@app.route('/register', methods=['POST'])
def register_processing():
    """Processes the info from the register account form"""
    # email = request.form["email"]
    # password = request.form["password"]
    # username = int(request.form["username"])
    # country = request.form["country"]
    # state = request.form["state"]
    # newsletter = request.form["newsletter"]

    # new_user = User(email=email, password=password, age=age, zipcode=zipcode)

    # db.session.add(new_user)
    # db.session.commit()

    # flash("User %s added." % email)
    # return redirect("/")

@app.route('/login', methods=['GET'])
def login_form():
    """Shows the form for logging into user account"""

    return render_template("login_form.html")

@app.route('/login', methods=['POST'])
def login_processing():
    """Processes the info from login form"""

    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()  # would .one() work the same?

    if not user:
        flash("Are you sure you are who you think you are?")
        return redirect("/login")

    if user.password != password:
        flash("Ooppsie! Incorrect password. Try again")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Yay, you made it into the Miniverse! Welcome.")
    return redirect("/%s" % user.user_id)

@app.route('/explore')
def explore_page():
    """Goes to search/explore page"""

    return render_template('explore.html')
    # return ajax?

# @app.route('/dashboard')
# def explore_page():
#     """Goes to user's dashboard page"""

#     return render_template('dashboard.html') %


# @app.route('/3d_file')
# def 3d_file():

if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)

    app.run(port=5000, host='0.0.0.0')

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()