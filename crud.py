"""PanTrack CRUD operations"""
from datetime import datetime, date
from model import db, User, Appointment, AppointmentSlot, Household, Admin, connect_to_db
from flask import session
from twilio.rest import Client
import os


def create_admin(fname, lname, email, username, password, super_admin=False):
    """Creates an admin user"""

    admin = Admin(fname=fname, lname=lname, email=email,
                    username=username, password=password,
                    super_admin=super_admin)
    
    db.session.add(admin)
    db.session.commit()

def create_user(fname, lname, email=None, username=None, password=None, phone_number=""):
    """Creates and returns a new user"""

    user = User(fname=fname, lname=lname, email=email, username=username,
                password=password, phone_number=phone_number)
    
    db.session.add(user)
    db.session.commit()

    return user


def create_appointment_slot(start_time, end_time, date):
    """Creates an available appointment slot"""

    appt_slot = AppointmentSlot(start_time=start_time, end_time=end_time, date=date)

    db.session.add(appt_slot)
    db.session.commit()

    return appt_slot


def create_household(user, num_people, wants_peanut_butter, picking_up_for_another=False,
                    another_pickup_name="", allergies=None, special_requests=None):
    """Creates a Household object for a user"""

    if another_pickup_name == None:
        another_pickup_name = ""
        
    household = Household(user_id=user.user_id,
                            num_people=num_people,
                            wants_peanut_butter=wants_peanut_butter,
                            picking_up_for_another=picking_up_for_another,
                            another_pickup_name=another_pickup_name,
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


def view_all_appt_slots():
    """Returns all appointment slots"""

    return AppointmentSlot.query.all()


def view_all_avail_appt_slots():
    """Returns a list of all available appointment slots"""

    all_appt_slots = view_all_appt_slots()
    avail_appt_slots = []

    for slot in all_appt_slots:
        if slot.appointment == []:
            avail_appt_slots.append(slot)

    return avail_appt_slots

def view_all_upcoming_appts():
    """Returns all appointments that have not yet passed"""

    all_appts = Appointment.query.all()
    upcoming_appts = [] #Appointment objects

    for appt in all_appts:
        if appt.appointment_slot.date >= date.today():
            upcoming_appts.append(appt)
    
    # <Appointment appointment_id=1 user_id=1 appointment_slot=2>

    def date_key(a):
        """Creates key for sorted function"""

        start_time = a.appointment_slot.start_time

        return start_time


    # return upcoming_appts

    return sorted(upcoming_appts, key=date_key)


def cancel_last_appt(user):
    """Deletes a user's last appointment object"""

    user_upcoming_appt = user.appointments[-1]
    user_upcoming_appt_id = user_upcoming_appt.appointment_id

    appt_to_delete = Appointment.query.get(user_upcoming_appt_id)

    db.session.delete(appt_to_delete)
    db.session.commit()

    return f'Successfully deleted {appt_to_delete}!'


def delete_ApptSlot(start_time):
    """Deletes an AppointmentSlot based on start time datetime"""

    appt_slot_to_delete = AppointmentSlot.query.filter(AppointmentSlot.start_time == start_time).first()

    db.session.delete(appt_slot_to_delete)
    db.session.commit()

    return f'You just deleted {appt_slot_to_delete}!'

def view_all_usernames():
    """Returns a list of all usernames"""

    all_users = view_all_users()

    all_usernames = []

    for user in all_users:
        username = user.username
        all_usernames.append(username)
    
    return all_usernames


def view_all_admin_usernames():
    """Returns a list of all Admin usernames"""

    all_admin = Admin.query.all()

    admin_usernames = []

    for admin in all_admin:
        username = admin.username
        admin_usernames.append(username)
    
    return admin_usernames

def find_user_by_username():
    """Finds a user associated with username in session"""

    user = User.query.filter_by(username=session['username']).first()

    return user


def string_to_ApptSlot(appt_slot_str):
    """Takes in string AppointmentSlot and turns into an object"""

    appt_slot_str = appt_slot_str
    date_format = "%Y-%m-%d %H:%M:%S"
    appt_slot_start = datetime.strptime(appt_slot_str, date_format)

    appt_slot = AppointmentSlot.query.filter_by(start_time=appt_slot_start).first()

    return appt_slot


def get_appt_phone_nums(appt_id_lst):
    """Takes in a list of appointment ids and returns a dict of phone numbers associated"""

    appt_phone_nums = {}

    for appt_id in appt_id_lst:
        appt_id = int(appt_id)
        appt = Appointment.query.get(appt_id)
        user = appt.user
        appt_phone_nums[f'{appt.user.fname} {appt.user.lname}'] = [user.phone_number, appt.appointment_slot.start_time.strftime("%B %d, %Y @ %I:%M%p")]

    return appt_phone_nums



def send_sms(to_num, msg_body):
    """Sends SMS via Twilio API"""

    # Your Account SID from twilio.com/console
    account_sid = os.environ['ACCOUNT_SID']
    # Your Auth Token from twilio.com/console
    auth_token  = os.environ['AUTH_TOKEN']

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=to_num, 
        from_=os.environ['FROM_PHONE_NUMBER'],
        body=msg_body)

    print(message.sid)


if __name__ == '__main__':
    from server import app
    connect_to_db(app)