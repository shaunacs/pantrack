"""Server for PanTrack app"""

from flask import (Flask, render_template, request, flash, session,
                    redirect)
from model import connect_to_db, User, AppointmentSlot, Household, Admin
from jinja2 import StrictUndefined
import crud
from flask_login import (LoginManager, login_user, login_required,
                        logout_user, current_user)
from datetime import datetime


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# @login_manager.user_loader
# def load_admin(admin_id):
#     return Admin.query.get(admin_id) # ***


@app.route('/')
def render_hompeage():
    """Displays the homepage is user in session"""

    if current_user.is_authenticated:
        if session['admin'] == True:
            return render_template('admin.html')


    if current_user.is_authenticated:
        user = crud.find_user_by_username()

        if len(user.appointments) != 0:
            user_next_appt = user.appointments[-1].appointment_slot.start_time
            if datetime.now() <= user_next_appt:
                has_appt = True
            else:
                user_next_appt = "You do not yet have an appointment. Schedule one now."
                has_appt = False
        else:
            has_appt = False
            user_next_appt = "You do not yet have an appointment. Schedule one now."
        return render_template('homepage.html', user_next_appt=user_next_appt,
                                has_appt=has_appt)
    else:
        return render_template('log_in_page.html')



@app.route('/log-in', methods=["POST"])
def handle_log_in():
    """Save session and return to homepage and process log in"""

    username = request.form.get("username")
    password = request.form.get("password")

    
    user = User.query.filter_by(username=username).first()


    if user == None:
        # admin = Admin.query.filter_by(username=username).first()
        # if admin is None:
        #     flash("No user with that username")
        return redirect("/")
        # else:
        #     if admin.password == password:
        #         login_user(admin) # ***
        #         session['admin'] = True
        #         return render_template('admin.html')


    if user.password == password:
        # Call flask_login.login_user to login a user
        login_user(user)

        flash("Logged in successfully!")

        #Add user to session
        session['username'] = request.form.get('username')
        session['password'] = request.form.get('password')
        session['admin'] = False

        return redirect('/')
    
    flash("Sorry try again.")
    return redirect("/")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('log_in_page.html')

@app.route('/create-account')
def render_create_account_form():
    """Renders form for user to create an account"""

    return render_template('create_account.html')


@app.route('/handle-create-account', methods=["POST"])
def create_user_account():
    """Creates user account based off info provided in form"""

    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    phone_number = request.form.get('phone-number')

    new_user = crud.create_user(fname, lname, email, username, password, phone_number)

    login_user(new_user)
    session['username'] = request.form.get('username')
    session['password'] = request.form.get('password')

    return redirect('/')


@app.route('/household-info')
def render_household_form():
    """Renders form to get info about household"""

    return render_template('household_form.html')



@app.route('/handle-household-info', methods=["POST"])
def handle_household_info():
    """Creates a household using user input"""

    user = crud.find_user_by_username()
    num_people = request.form.get('num-people')
    wants_peanut_butter = bool(request.form.get('wants-peanut-butter'))
    picking_up_for_another = bool(request.form.get('picking-up-for-another'))
    
    user_household = crud.create_household(user, num_people, wants_peanut_butter,
                        picking_up_for_another)
    
    available_appts = []
    all_appt_slots = crud.view_all_appt_slots()
    for appt_slot in all_appt_slots:
        if appt_slot.appointment == []:
            available_appts.append(appt_slot)
    
    return render_template('schedule_appointment.html',
                            available_appts=available_appts)



@app.route('/handle-schedule-appt', methods=["POST"])
def handle_schedule_appointment():
    """Schedules user for appointment at selected appointment time"""

    user = crud.find_user_by_username()

    selected_appt_slot_str = request.form.get('appt_slot')
    
    selected_appt_slot = crud.string_to_ApptSlot(selected_appt_slot_str)
    household = Household.query.filter_by(user_id=user.user_id)[-1]

    appt = crud.create_appointment(user, selected_appt_slot, household)

    return redirect('/')
 

@app.route('/appointments')
@login_required
def render_appts_page():
    """Renders the appointments page"""
    if session['admin'] == True:
        upcoming_appts = crud.view_all_upcoming_appts()

        return render_template('appointments.html', upcoming_appts=upcoming_appts)
    else:
        flash("You do not have access to this page")
        return redirect('/')




if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug=True, use_reloader=True, use_debugger=True)