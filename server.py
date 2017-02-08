


# Make sure to import all the things up here



app = Flask(__name__)

# Need this to use Flask sessions and super useful Flask debugging errors
app.secret_key = "soVewyVewySecretDoc"

# Initiates error if undefined var in Jinja2
# app.jinja_env.undfined = StrictUndefined

@app.route('/')
def main():
    """Homepage"""

    return render_template('homepage.html')

@app.route('/register', methods=['GET'])
def register_form():
    """Shows the form for registering for an account"""

    return render_template("register_form.html")

@app.route('/register', methods=['POST'])
def register_processing():
    """Processes the info from the register account form"""

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
    return redirect("" % user.user_id)
