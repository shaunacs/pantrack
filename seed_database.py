"""Script to seed database for PanTrack"""

import os
from datetime import datetime, date, timedelta, time
import crud
import model
import server
from random import choice, randint

os.system('dropdb appointments')
os.system('createdb appointments')
model.connect_to_db(server.app)
model.db.create_all()

# create test users
for n in range(10):
    fname = f'test{n}'
    lname = f'tester{n}'
    email = f'user{n}@test.com'
    username = f'user{n}'
    password = 'test'
    phone_number = '1212'

    user = crud.create_user(fname, lname, email, username, password, phone_number)

# create test appointment slots
date = date(2021, 6, 4)
# end_date = date(2021, 6, 14)
delta = timedelta(minutes=15)
start_time = datetime(2021, 6, 7, 9, 0)
end_appts = datetime(2021, 6, 7, 12, 0)

while start_time <= end_appts:
    end_time = start_time + delta
    appt_slot = crud.create_appointment_slot(start_time, end_time, date)
    start_time += delta


# Create test appointments

all_users = model.User.query.all()
for user in all_users:
    num_people = randint(1, 5)
    wants_peanut_butter = choice([True, False])
    picking_up_for_another = choice([True, False])

    user_household = crud.create_household(num_people, wants_peanut_butter,
                                        picking_up_for_another)
    
    available_appts = model.AppointmentSlot.query.all()
    user_appt_slot = available_appts[user.user_id]
    user_appt = crud.create_appointment(user, user_appt_slot, user_household)




