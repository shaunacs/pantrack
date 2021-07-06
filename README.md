# PanTrack

Learn more about the developer: https://www.linkedin.com/in/shauna-saunders/

## Project Description
PanTrack is a full stack web application designed for a local food pantry to simplify the process of scheduling times for clients to pick up food. PanTrack replaces a workflow of making phone calls to schedule appointments with a simple, user-friendly, appointment scheduling process for clients. Users can create an account and are then given the flexibility to schedule their own appointments or receive reminders of their upcoming appointment.

PanTrack also consists of an Admin panel that provides the food pantry with easy access to the details of appointments scheduled, control over when food is available to pick up, and the ability to send SMS appointment reminders using the Twilio API.

## Technologies Used
- Python
- Flask
- Jinja
- React
- JavaScript
- jQuery
- HTML
- Bootstrap
- CSS
- SQLAlchemy
- PostgreSQL
- Twilio API

## How to Use PanTrack Flask App
1. Create and activate a python virtual environment
2. Install all dependencies
    * `pip install -r requirements.txt`
3. Create a PostgreSQL database named *appointments*
    * `createdb appointments`
4. Create the tables in your database:
    * Run *model.py* interactively: `python -i model.py`
    * Create tables: `db.create_all()`

**If you would like to seed the database with fake data:**
Run `python seed_database.py` or `python demo_seed.py`

5. Quit interactive mode and start the server
    * `python server.py`
6. Navigate to `localhost` to access PanTrack

### Twilio API
**If you would like to use the SMS Appointment Reminder feature:**
* Sign up for Twilio, and obtain an AUTH_TOKEN, ACCOUNT_SID, and PHONE_NUMBER
* Save these keys in a file called `secrets.sh` using this format:
```python
export ACCOUNT_SID="YOUR_ACCOUNT_SID_HERE"
export AUTH_TOKEN="YOUR_AUTH_TOKEN_HERE"
export FROM_PHONE_NUMBER="YOUR_TWILIO_PHONE_NUMBER"
```

* Source your keys from your `secrets.sh` file into your virtual environment:
    * `source secrets.sh`
* Run the server `python server.py`
