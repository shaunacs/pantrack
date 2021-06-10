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


#create test admin
admin = crud.create_admin(fname='Adminy',
                    lname='Adminder',
                    email='admin@test.test',
                    username='admin',
                    password='test')

                    
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
# date = date(2021, 6, 15)
# end_date = date(2021, 6, 14)
delta = timedelta(minutes=10)
start_time = datetime(2021, 6, 15, 9, 0)
end_appts = datetime(2021, 6, 15, 12, 0)

while start_time <= end_appts:
    end_time = start_time + delta
    date = start_time.date()
    appt_slot = crud.create_appointment_slot(start_time, end_time, date)
    start_time += delta


# Create test appointments

all_users = crud.view_all_users()
for user in all_users:
    num_people = randint(1, 5)
    wants_peanut_butter = choice([True, False])
    picking_up_for_another = choice([True, False])

    user_household = crud.create_household(user, num_people, wants_peanut_butter,
                                        picking_up_for_another)
    
    available_appts = crud.view_all_appt_slots()
    user_appt_slot = available_appts[user.user_id]
    user_appt = crud.create_appointment(user, user_appt_slot, user_household)




