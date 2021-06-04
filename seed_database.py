"""Script to seed database for PanTrack"""

import os
from datetime import datetime, date, timedelta
import crud
import model
import server

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
start_date = date(2021, 6, 4)
end_date = date(2021, 6, 14)
delta = timedelta(days=1)

while start_date <= end_date:
    
    appt_slot = crud.create_appointment_slot()




