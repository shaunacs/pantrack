"""Script to seed database for PanTrack"""

import os
from datetime import datetime
import crud
import model
import server

os.system('dropdb appointments')
os.system('createdb appointments')
model.connect_to_db(server.app)
model.db.create_all()