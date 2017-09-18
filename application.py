"""Project Miniverse"""
import os
from jinja2 import StrictUndefined  # makes StrictUndefined work below
# Makes all the flask commands work
from flask import Flask, redirect, session, render_template, request, flash, send_from_directory, current_app, url_for, jsonify
# from flaskext.uploads import configure_uploads
# , IMAGES, ALL
from werkzeug.utils import secure_filename
# This imports the debug toolbar witch will give useful error messages
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Model3d, UserImage

####### changed app. to application. for Amazon EB (Elastic Beanstalk) reccomendations
application = Flask(__name__)
# Need this to use Flask sessions and super useful Flask debugging errors
application.secret_key = "soVewyVewySecretDoc"

# Initiates error if undefined variable in Jinja
application.jinja_env.undfined = StrictUndefined

application.jinja_env.auto_reload = True  # delete for "production" copy


@application.route('/')
def index():
    """Homepage"""

    return render_template('homepage.html')


@application.route('/register', methods=['GET'])
def register_form():
    """Shows the form for registering for an account"""

    return render_template("register_form.html")


@application.route('/register', methods=['POST'])
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


@application.route('/login', methods=['GET'])
def login_form():
    """Shows the form for logging into user account"""

    return render_template("login_form.html")


@application.route('/login', methods=['POST'])
def login_processing():
    """Processes the info from login form"""

    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

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


@application.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("You have logged out")
    return redirect("/")


@application.route('/explore', methods=['GET'])
def explore():
    """Goes to search/explore page"""

    explore_input = request.form.get("explore-input")
    img = db.session.query(UserImage.filepath_img).all()
    results = Model3d.query.filter(Model3d.title.ilike('%'+str(explore_input)+'%'))

    return render_template('explore.html', results=results, explore_input=explore_input, img=img)


@application.route('/explore', methods=['POST'])
def explore_results():
    """Returns results on search/explore page using ilike for case insensitive results"""

    explore_input = request.form.get("explore-input")
    img = db.session.query(UserImage.filepath_img).all()
    results = Model3d.query.filter(Model3d.title.ilike('%'+str(explore_input)+'%'))

    return render_template('explore.html', results=results, explore_input=explore_input, img=img)

# @app.route('/explore-results.json', methods=['POST'])
# def exploreResults():
#     """Search and return search results"""
#     explore_input = request.form.get("explore-input")
#     img = db.session.query(UserImage.filepath_img).all()
#     results = Model3d.query.filter(Model3d.title.ilike('%'+str(explore_input)+'%'))
#     return jsonify({'explore_input': explore_input, 'img': img, 'results': results})


@application.route('/about')
def about_page():
    """Goes to about page"""

    return render_template('about.html')


@application.route("/dashboard/<int:user_id>")
def user_dashboard(user_id):
    """Users personal dashboard"""

    user = User.query.get(user_id)
    # fix this
    img = db.session.query(UserImage.filepath_img).all()

    return render_template('user.html', user=user, img=img)


########### UPLOADS ############
IMG_UPLOAD_FOLDER = 'static/uploaded/images'
IMG_ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

#STL_UPLOAD_FOLDER = '/uploaded/stl_files'
STL_UPLOAD_FOLDER = 'uploaded/stl_files'
STL_ALLOWED_EXTENSIONS = ('stl')

application.config['IMG_UPLOAD_FOLDER'] = IMG_UPLOAD_FOLDER
application.config['STL_UPLOAD_FOLDER'] = STL_UPLOAD_FOLDER


# these two functions make sure the file exension is correct, don't rename 'filename'
def img_allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in IMG_ALLOWED_EXTENSIONS


def stl_allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in STL_ALLOWED_EXTENSIONS


@application.route('/upload_file_stl', methods=['GET'])
def upload_form():
    """Shows stl upload form"""

    return render_template("upload_stl.html")


@application.route('/upload_file_stl', methods=['POST'])
def upload_file_stl():
    """Processes and uploads the file securely and generates confirmation page"""

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
        stl_file.save(os.path.join(application.config['STL_UPLOAD_FOLDER'], filename))

        user_id = session['user_id']
        # filepath_3d = "uploaded/stl_files/" + filename
        filepath_3d = filename
        title = request.form.get("title")
        owns_file = request.form.get("owns_file", False)
        downloadable = request.form.get("downloadable", False)

        new_stl = Model3d(filepath_3d=filepath_3d, user_id=user_id, title=title,
                          owns_file=owns_file, downloadable=downloadable)
        db.session.add(new_stl)
        db.session.commit()

        user = User.query.get(user_id)
        stl = filepath_3d

        flash("%s has been uploaded!" % filename)
        return render_template('stl.html', user=user, stl=stl, title=title, downloadable=downloadable)


@application.route('/model_3d_page/<int:model_3d_id>', methods=['GET'])
def model_3d_page(model_3d_id):
    """Shows the page for an individual 3D model and allows image uploads"""

    model3d = Model3d.query.get(model_3d_id)
    user = User.query.get(model3d.user_id)
    img = db.session.query(UserImage).filter_by(model_3d_id=model3d.model_3d_id).first()

    # import pdb
    # pdb.set_trace()

    if 'user_id' in session:
        return render_template('model_3d_page.html',
                               user=user,
                               model3d=model3d,
                               img=img)
    flash("Log in to view user pages!!!")
    return redirect("/")


@application.route('/model_3d_page/<int:model_3d_id>', methods=['POST'])
def upload_file_img(model_3d_id):
    """Processes and uploads the image file securely and reloads model_3d_page.html page"""

    # check if the post request has the file ending
    if 'img' not in request.files:
        flash('Incorrect file ending')
        return redirect('/model_3d_page/' + str(model_3d_id))
    img_file = request.files['img']
    if img_file.filename == '':
        flash('You didn\'t select the correct file type')
        return redirect("/model_3d_page/" + str(model_3d_id))
    if img_file and img_allowed_file(img_file.filename):
        filename = secure_filename(img_file.filename)
        img_file.save(os.path.join(application.config['IMG_UPLOAD_FOLDER'], filename))

        user_id = session['user_id']
        filepath_img = filename

        model3d = Model3d.query.get(model_3d_id)

        new_img = UserImage(filepath_img=filepath_img, user_id=user_id, model_3d_id=model_3d_id)
        db.session.add(new_img)
        db.session.commit()
        user = User.query.get(user_id)
        img = db.session.query(UserImage).filter_by(model_3d_id=model3d.model_3d_id).first()

        flash("The image %s has been uploaded!" % filename)
        return render_template('model_3d_page.html',
                               user=user,
                               model3d=model3d,
                               img=img)


@application.route('/uploaded/stl_files/<path:filepath_3d>', methods=['GET'])
def download(filepath_3d):
    """Download files"""

    uploads = os.path.join(application.config['STL_UPLOAD_FOLDER'])

    return send_from_directory(directory=uploads, filename=filepath_3d)

# if __name__ == "__main__":
#     # app.debug = True

#     app.run(port=5000, host='0.0.0.0')
# http://127.0.0.1:5000/

###### Elastic Beanstalk reccomendations ###
# EB looks for an 'application' callable by default.
# application = Flask(__name__) (SEE line 14)

# run the app.
if __name__ == "__main__":

    connect_to_db(application)

    #     # Use the DebugToolbar
    DebugToolbarExtension(application)

    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    # application.debug = True
    application.run(port=5000, host='0.0.0.0')
