"""Models for PanTrack app"""

from flask import Flask
from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class Admin(db.Model):
    """An administrative user"""

    __tablename__ = "admins"

    admin_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    fname = db.Column(db.String(15), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Admin admin_id={self.admin_id} fname={self.fname} lname={self.lname}>'


class User(db.Model, UserMixin):
    """A food pantry user"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    fname = db.Column(db.String(15), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)
    # household_id = db.Column(db.Integer, db.ForeignKey('households.household_id'))

    # household = a list of household objects
    appointments = db.relationship('Appointment', backref='user')


    def get_id(self):
        """Override UserMixin.get_id"""

        return str(self.user_id)


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
    household_id = db.Column(db.Integer, db.ForeignKey('households.household_id'))

    appointment_slot = db.relationship('AppointmentSlot', backref='appointment')
    household = db.relationship('Household', backref='appointment')

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
    date = db.Column(db.Date)

    #appointment = appointment made for the slot

    def __repr__(self):
        return f'<AppointmentSlot date={self.date} start_time={self.start_time} end_time={self.end_time}>'


class Household(db.Model):
    """Contains information regarding a user's household"""

    __tablename__ = "households"

    household_id = db.Column(db.Integer,
                                autoincrement=True,
                                primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    num_people = db.Column(db.Integer, nullable=False)
    wants_peanut_butter = db.Column(db.Boolean, nullable=False)
    picking_up_for_another = db.Column(db.Boolean, nullable=False)
    allergies = db.Column(db.String(30))
    special_requests = db.Column(db.Text)

    #appointment = appointment for this household
    user = db.relationship('User', backref="household")


    def __repr__(self):
        return f'<Household household_id={self.household_id} num_people={self.num_people}>'


def create_sample_data():
    """Create some sample data for PanTrack"""

    AppointmentSlot.query.delete()
    Household.query.delete()
    User.query.delete()
    Appointment.query.delete()
    Admin.query.delete()

    #Test Admin
    admin = Admin(fname='Adminy',
                    lname='Adminder',
                    email='admin@test.test',
                    username='admin',
                    password='test')
    
    db.session.add(admin)
    db.session.commit()


    #Test User
    user = User(fname='Test',
                lname='Tester',
                email='test@test.test',
                username='testy',
                password='testttt',
                phone_number='5555555555')
    
    db.session.add(user)
    db.session.commit()
    print(f'user= {user}')

    #Test AppointmentSlot
    appt_slot = AppointmentSlot(start_time=datetime(2021, 6, 3, 10, 30),
                                end_time=datetime(2021, 6, 3, 10, 45),
                                date=date(2021, 6, 3))

    db.session.add(appt_slot)
    db.session.commit()
    print(f'appt_slot= {appt_slot}')
    
    #Test Household
    household = Household(user_id=user.user_id,
                            num_people=4,
                            wants_peanut_butter=False,
                            allergies='peanuts',
                            picking_up_for_another=False)
    
    db.session.add(household)
    db.session.commit()
    print(f'household= {household}')

    
    #Test Appointment
    appt = Appointment(user_id=user.user_id,
                        appointment_slot_id=appt_slot.appointment_slot_id,
                        household_id=household.household_id)
    
    db.session.add(appt)
    db.session.commit()
    print(f'appt= {appt}')




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