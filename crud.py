"""PanTrack CRUD operations"""
from datetime import datetime
from model import (db, User, Appointment, AppointmentSlot,
                    Household, connect_to_db)