"""PanTrack CRUD operations"""
from datetime import datetime
from model import db, User, Appointment, AppointmentSlot, Household, connect_to_db


def create_user(fname, lname, email, password, phone_number):
    """Creates and returns a new user"""

    user = User(fname=fname, lname=lname, email=email,
                password=password, phone_number=phone_number)
    
    # print(user)
    db.session.add(user)
    db.session.commit()

    return user