"""Project Miniverse"""
import os
from jinja2 import StrictUndefined  # makes StrictUndefined work below
# Makes all the flask commands work
from flask import Flask, redirect, session, render_template, request, flash, send_from_directory, current_app
# from flaskext.uploads import configure_uploads
# , IMAGES, ALL
from werkzeug.utils import secure_filename
# This imports the debug toolbar witch will give useful error messages
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Model3d, Favorite, UserImage


app = Flask(__name__)
# Need this to use Flask sessions and super useful Flask debugging errors
app.secret_key = "soVewyVewySecretDoc"

# Initiates error if undefined variable in Jinja
app.jinja_env.undfined = StrictUndefined

app.jinja_env.auto_reload = True  # delete for "production" copy


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


########### UPLOADS ############
IMG_UPLOAD_FOLDER = 'uploaded/images'
IMG_ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

STL_UPLOAD_FOLDER = 'uploaded/stl_files'
STL_ALLOWED_EXTENSIONS = ('stl')

app.config['IMG_UPLOAD_FOLDER'] = IMG_UPLOAD_FOLDER
app.config['STL_UPLOAD_FOLDER'] = STL_UPLOAD_FOLDER


# these two functions make sure the file exension is correct
def img_allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in IMG_ALLOWED_EXTENSIONS


def stl_allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in STL_ALLOWED_EXTENSIONS


@app.route('/upload_file_img', methods=['GET', 'POST'])
def upload_file_img():
    if request.method == 'POST':
        # check if the post request has the file ending
        if 'img' not in request.files:
            flash('Incorrect file ending')
            return redirect("/upload_file_img")
        img_file = request.files['img']
        if img_file.filename == '':
            flash("You didn\'t select a file")
            return redirect("/upload_file_img")
        if request.method == 'POST' and img_file and img_allowed_file(img_file.filename):
            filename = secure_filename(img_file.filename)
            img_file.save(os.path.join(app.config['IMG_UPLOAD_FOLDER'], filename))
            flash("%s has been uploaded" % filename)
            return filename

    return render_template('upload_img.html')


@app.route('/upload_file_stl', methods=['GET'])
def upload_form():
    """Shows stl upload form"""

    return render_template("upload_stl.html")


@app.route('/upload_file_stl', methods=['POST'])
def upload_file_stl():
    """Processes and uploads the file securely"""

    # check if the post request has the file ending
    if 'stl' not in request.files:
        flash('Incorrect file ending')
        return redirect("/upload_file_stl")
    stl_file = request.files['stl']
    if stl_file.filename == '':
        flash('You didn\'t select the correct file type')
        return redirect("/upload_file_stl")
    if stl_file and stl_allowed_file(stl_file.filename):
        filename = secure_filename(stl_file.filename)
        stl_file.save(os.path.join(app.config['STL_UPLOAD_FOLDER'], filename))

        user_id = session['user_id']
        filepath_3d = "uploaded/stl_files/" + filename
        title = request.form.get("title")
        owns_file = request.form.get("owns_file", False)
        downloadable = request.form.get("downloadable", False)

        new_stl = Model3d(filepath_3d=filepath_3d, user_id=user_id, title=title,
                          owns_file=owns_file, downloadable=downloadable)
        db.session.add(new_stl)
        db.session.commit()

        user = User.query.get(user_id)
        stl = filepath_3d

        # model_3d = Model3d.query.get(model_3d_id)

        flash("%s has been uploaded!" % filename)
        return render_template('stl.html', user=user, stl=stl, title=title, downloadable=downloadable)


@app.route('/uploaded/stl_files/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(current_app.root_path, app.config['STL_UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)


if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
