"""PanTrack CRUD operations"""
from datetime import datetime, date
from model import db, User, Appointment, AppointmentSlot, Household, connect_to_db


def create_user(fname, lname, email, username, password, phone_number):
    """Creates and returns a new user"""

    user = User(fname=fname, lname=lname, email=email, username=username,
                password=password, phone_number=phone_number)
    
    # print(user)
    db.session.add(user)
    db.session.commit()

    return user


def create_appointment_slot(start_time, end_time, date):
    """Creates an available appointment slot"""

    appt_slot = AppointmentSlot(start_time=start_time, end_time=end_time, date=date)

    db.session.add(appt_slot)
    db.session.commit()

    return appt_slot


def create_household(num_people, wants_peanut_butter, picking_up_for_another,
                    allergies=None, special_requests=None):
    """Creates a Household object for a user"""

    household = Household(num_people=num_people,
                            wants_peanut_butter=wants_peanut_butter,
                            picking_up_for_another=picking_up_for_another,
                            allergies=allergies,
                            special_requests=special_requests)
    
    db.session.add(household)
    db.session.commit()

    return household



def create_appointment(user, appt_slot, household):
    """Creates an appointment for a user"""

    appt = Appointment(user_id=user.user_id,
                        appointment_slot_id=appt_slot.appointment_slot_id,
                        household_id=household.household_id)

    db.session.add(appt)
    db.session.commit()

    return appt


def view_all_users():
    """Returns all users"""

    return User.query.all()



if __name__ == '__main__':
    from server import app
    connect_to_db(app)