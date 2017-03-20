"""Models and database functions for Project Miniverse"""

from flask_sqlalchemy import SQLAlchemy

# Connects this to the PostgreSQL database

db = SQLAlchemy()

####################################################

# database model definitions to make tables in database


class User(db.Model):
    """User of Project Miniverse site"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(15), nullable=False)
    country = db.Column(db.String(45), nullable=True)
    state = db.Column(db.String(5), nullable=True)
    newsletter = db.Column(db.Boolean)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<User user_id=%s email=%s username=%s country=%s state=%s newsletter=%s>") % (
            self.user_id,
            self.email,
            self.username,
            self.country,
            self.state,
            self.newsletter)


class Model3d(db.Model):
    """3D model on Project Miniverse site"""

    __tablename__ = "models_3d"

    model_3d_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    downloadable = db.Column(db.Boolean, default=False)
    title = db.Column(db.String(40), nullable=True)
    filepath_3d = db.Column(db.String(80), nullable=True)
    owns_file = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))  # Foriegn Key

    user = db.relationship('User',
                            backref=db.backref('models_3d'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Model_3d model_3d_id=%s downloadable=%s title=%s filepath_3d=%s owns_file=%s>" % (
                            self.model_3d_id,
                            self.downloadable,
                            self.title,
                            self.filepath_3d,
                            self.owns_file)


class Favorite(db.Model):
    """Favorited 3D models of each user"""

    __tablename__ = "favorites"

    fav_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))  # Foriegn Key
    model_3d_id = db.Column(db.Integer, db.ForeignKey('models_3d.model_3d_id'))  # Foriegn Key

    user = db.relationship('User',
                           backref=db.backref('favorites'))
    model_3d = db.relationship('Model3d',
                               backref=db.backref('favorites'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Favorite fav_id=%s>" % (self.fav_id)


# check if this class is ok with capitol I in images for model name or keep lower i
class UserImage(db.Model):
    """Image(s) for each seperate 3D model page"""

    __tablename__ = "user_images"

    img_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    filepath_img = db.Column(db.String(80), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))  # Foriegn Key
    model_3d_id = db.Column(db.Integer, db.ForeignKey('models_3d.model_3d_id'))  # Foriegn Key

    user = db.relationship('User',
                           backref=db.backref('user_images'))
    model_3d = db.relationship('Model3d',
                               backref=db.backref('user_images'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User_Image img_id=%s filepath_img=%s>" % (self.img_id,
                                                           self.filepath_img)


def example_data():
    user = User(email="userdatatest@testy.com",
                password="testy",
                username="User testz",
                country="United States",
                state="CA"
                )
    db.session.add(user)
    db.session.commit()


#####################################################################


# def connect_to_db(app):
#     """Connects the database to the Flask app"""

#     # Configure to use our PostgreSQL database
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///miniverse'
#     db.app = app
#     db.init_app(app)

# changed for testing
def connect_to_db(app, db_uri="postgresql:///miniverse"):
    """Connects database to Flask"""
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    db.app = app
    db.init_app(app)


if __name__ == '__main__':

    from server import app
    connect_to_db(app)
    print "Connected to DB!!"
