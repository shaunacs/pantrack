"""Script to seed database for PanTrack demo"""

import os
from datetime import datetime, date, timedelta, time
import crud
import model
import server
from faker import Faker
from random import choice, randint

os.system('dropdb appointments')
os.system('createdb appointments')
model.connect_to_db(server.app)
model.db.create_all()


#create test admin
admin = crud.create_admin(fname='Adminy',
                    lname='Adminder',
                    email='admin@test.test',
                    username='admin',
                    password='test',
                    super_admin=True)

fake = Faker()
# create test users
for n in range(10):
    full_name = fake.name().split(' ')
    fname = full_name[0]
    lname = full_name[1]
    email = fake.email()
    username = f'{fname[0]}{lname}{n}'
    password = 'test'

    user = crud.create_user(fname, lname, email, username, password)

# create test appointment slots
delta = timedelta(minutes=15)
start_time = datetime(2030, 7, 13, 9, 0)
end_appts = datetime(2030, 7, 13, 15, 0)

while start_time <= end_appts:
    end_time = start_time + delta
    date = start_time.date()
    appt_slot = crud.create_appointment_slot(start_time, end_time, date)
    start_time += delta


# create test appointments
all_users = crud.view_all_users()
for user in all_users:
    num_people = randint(1, 6)
    wants_peanut_butter = choice([True, False])
    picking_up_for_another = choice([True, False])

    if picking_up_for_another == True:
        another_pickup_name = fake.name()
    else:
        another_pickup_name = ""

    user_household = crud.create_household(user, num_people, wants_peanut_butter,
                                        picking_up_for_another, another_pickup_name)
    
    available_appts = crud.view_all_avail_appt_slots()
    user_appt_slot = choice(available_appts)
    user_appt = crud.create_appointment(user, user_appt_slot, user_household)