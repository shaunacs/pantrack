"""Models for PanTrack app"""

from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A food pantry user"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    fname = db.Column(db.String(15), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)
    last_appointment = db.Column(db.DateTime)
    is_admin = db.Column(db.Boolean)
    household_id = db.Column(db.Integer, db.ForeignKey('households.household_id'))

    household = db.relationship('Household', backref='user')
    appointment = db.relationship('Appointment', backref='user')

    def __repr__(self):
        return f'<User user_id={self.user_id} name={self.fname} {self.lname}>'


class Appointment(db.Model):
    """A user's appointment"""

    __tablename__ = "appointments"

    appointment_id = db.Column(db.Integer,
                                autoincrement=True,
                                primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    appointment_slot_id = db.Column(db.Integer, db.ForeignKey('appointment_slots.appointment_slot_id'))

    appointment_slot = db.relationship('AppointmentSlot', backref='appointment')

    # user = user associated with appointment

    def __repr__(self):
        return f'<Appointment appointment_id={self.appointment_id} user_id={self.user_id} appointment_slot={self.appointment_slot_id}>'
    

class AppointmentSlot(db.Model):
    """Time slots available for appointments"""

    __tablename__ = "appointment_slots"

    appointment_slot_id = db.Column(db.Integer,
                                    autoincrement=True,
                                    primary_key=True)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    date = db.Column(db.DateTime)

    #appointment = appointment made for the slot

    def __repr__(self):
        return f'<AppointmentSlot date={self.date} start_time={self.start_time} end_time={self.end_time}>'


class Household(db.Model):
    """Contains information regarding a user's household"""

    __tablename__ = "households"

    household_id = db.Column(db.Integer,
                                autoincrement=True,
                                primary_key=True)
    num_people = db.Column(db.Integer, nullable=False)
    wants_peanut_butter = db.Column(db.Boolean)
    allergies = db.Column(db.String(30))
    picking_up_for_another = db.Column(db.Boolean)
    special_requests = db.Column(db.Text)

    # user = a list of users in household

    def __repr__(self):
        return f'<Household household_id={self.household_id} num_people={self.num_people}>'


def connect_to_db(app, db_uri='postgresql:///appointments'):
    """Connect to database"""

    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = app
    db.init_app(app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    connect_to_db(app)