"""Models for PanTrack app"""

import datetime
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
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)
    last_appointment = db.Column(db.DateTime)
    is_admin = db.Column(db.Boolean)
    user_household_id = db.Column(db.Integer, db.ForeignKey('user_households.user_household_id'))

    def __repr__(self):
        return f'<User user_id={self.user_id} name={fname} {lname}>'


class Appointment(db.Model):
    """A user's appointment"""

    __tablename__ = "appointments"

    appointment_id = db.Column(db.Integer,
                                autoincrement=True,
                                primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    appointment_slot_id = db.Column(db.Integer, db.ForeignKey('appointment_slots.appointment_slot_id'))

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

    def __repr__(self):
        return f'<AppointmentSlot date={self.date} start_time={self.start_time} end_time={self.end_time}>'


class UserHousehold(db.Model):
    """Contains information regarding a user's household"""

    __tablename__ = "user_households"

    user_household_id = db.Column(db.Integer,
                                autoincrement=True,
                                primary_key=True)
    num_people = db.Column(db.Integer, nullable=False)
    wants_peanut_butter = db.Column(db.Boolean)
    allergies = db.Column(db.String(30))
    picking_up_for_another = db.Column(db.Boolean)
    special_requests = db.Column(db.Text)

    def __repr__(self):
        return f'<UserHousehold user_household_id={self.user_household_id} num_people={self.num_people}>'
