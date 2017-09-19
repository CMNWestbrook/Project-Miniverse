"""Utility file to seed a few users from seed_data/"""

from sqlalchemy import func

from model import User, connect_to_db, db
from application import application


def load_users():
    """Load users from u.user into database."""

    print "Users"

    for i, row in enumerate(open("seed_data/u.user")):
        row = row.rstrip()
        user_id, email, password, username, country, state, newsletter = row.split("|")

        user = User(email=email,
                    password=password,
                    username=username,
                    country=country,
                    state=state,
                    newsletter=newsletter)

        # Add to the session or it won't be stored
        db.session.add(user)

        # show progress
        if i % 100 == 0:
            print i

    # commit this session to the database
    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1 so Postgres wont try to override
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(application)
    db.create_all()

    load_users()
    set_val_user_id()
