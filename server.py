"""Project Miniverse"""

from jinja2 import StrictUndefined  # makes StrictUndefined work below

# Makes all the flask commands work
from flask import Flask, redirect, session, render_template, request, flash
# This imports the debug toolbar witch will give useful error messages
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User  # , Model3d, Favorite, UserImage


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

    email = request.form.get("email")
    password = request.form.get("password")
    username = request.form.get("username")
    country = request.form.get("country")
    state = request.form.get("state")
    newsletter = request.form.get("newsletter", False)

    new_user = User(email=email, password=password, username=username,
                    country=country, state=state, newsletter=newsletter)

    db.session.add(new_user)
    db.session.commit()

    flash("User %s has been registered" % email)
    return redirect("/")


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
    return redirect("/")
    # ("/%s" % user.user_id) use if decide to direct directly to user page


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("You have logged out")
    return redirect("/")


@app.route('/explore')
def explore_page():
    """Goes to search/explore page"""

    return render_template('explore.html')
    # return ajax?


@app.route('/about')
def about_page():
    """Goes to about page"""

    return render_template('about.html')


@app.route("/dashboard/<int:user_id>")
def user_dashboard(user_id):
    """Users personal dashboard"""

    user = User.query.get(user_id)

    # if not user_id:
    #     raise Exception("Log in to see your Dashboard")
    # else:
    return render_template('user.html', user=user)


# @app.route('/dashboard')
# def explore_page():
#     """Goes to user's dashboard page"""

#     return render_template("/%s" % user.user_id)


# @app.route('/3d_file')
# def 3d_file():

if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)


    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
