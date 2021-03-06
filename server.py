"""Server for PanTrack app"""

from flask import (Flask, render_template, request, flash, session,
                    redirect, jsonify)
from model import connect_to_db, User, AppointmentSlot, Household, Admin
from jinja2 import StrictUndefined
import crud
from flask_login import (LoginManager, login_user, login_required,
                        logout_user, current_user)
from datetime import datetime, timedelta


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
    print(current_user)

    if current_user.is_authenticated:
        if session['admin'] == True:
            admin = Admin.query.filter_by(username=session['username']).first()
            @login_manager.user_loader
            def load_admin(admin_id):
                return Admin.query.get(admin_id)
            login_user(admin)
            return render_template('admin.html')


    if current_user.is_authenticated:
        user = crud.find_user_by_username()

        if len(user.appointments) != 0:
            user_next_appt = user.appointments[-1].appointment_slot.start_time
            if datetime.now() <= user_next_appt:
                has_appt = True
                user_next_appt = user_next_appt.strftime("%B %d, %Y @ %I:%M%p")
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
        admin = Admin.query.filter_by(username=username).first()
        if admin is None:
            flash("No user with that username")
            return redirect("/")
        else:
            if admin.password == password:
                @login_manager.user_loader
                def load_admin(admin_id):
                    return Admin.query.get(admin_id)
                login_user(admin) # ***
                session['username'] = request.form.get('username')
                session['admin'] = True
                if admin.super_admin:
                    super_admin = True
                    return render_template('admin.html', super_admin=super_admin)
                else:
                    super_admin = False
                    return render_template('admin.html', super_admin=super_admin)


    if user.password == password:
        # Call flask_login.login_user to login a user
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(user_id)
        login_user(user)


        #Add user to session
        session['username'] = request.form.get('username')
        session['password'] = request.form.get('password')
        session['admin'] = False

        return redirect('/')
    
    flash("Incorrect username and/or password.")
    return redirect("/")


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

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

    if username in crud.view_all_usernames():
        flash('Username already taken')
        return redirect('/create-account')
    new_user = crud.create_user(fname, lname, email, username, password, phone_number)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    login_user(new_user)
    session['username'] = request.form.get('username')
    session['password'] = request.form.get('password')
    session['admin'] = False

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
    wants_peanut_butter = request.form.get('wants-peanut-butter')
    picking_up_for_another = request.form.get('picking-up-for-another')
    another_pickup_name = request.form.get('pickup-for')
    allergies = request.form.get('allergies')
    special_requests = request.form.get('special-requests')
    
    # Changing strings to appropriate data type to create instance
    if allergies == "":
        allergies = None
    if special_requests == "":
        special_requests = None
    
    if wants_peanut_butter == "True":
        wants_peanut_butter = True
    else:
        wants_peanut_butter = False
    
    if picking_up_for_another == "true":
        picking_up_for_another = True
    else:
        picking_up_for_another = False
    
    user_household = crud.create_household(user, num_people, wants_peanut_butter,
                        picking_up_for_another, another_pickup_name, allergies, special_requests)

    available_appts = {}
    all_appt_slots = crud.view_all_appt_slots()
    for appt_slot in all_appt_slots:
        if appt_slot.appointment == []:
            available_appts[appt_slot] = appt_slot.start_time.strftime("%B %d, %Y at %I:%M%p")
    
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

    flash("Your appointment was successfully scheduled.")

    return redirect('/')


@app.route('/handle-cancel-appt')
@login_required
def handle_cancel_appt():
    """Cancels a user's upcoming appointment"""

    user = crud.find_user_by_username()
    crud.cancel_last_appt(user)

    flash("Your appointment has been cancelled.")

    return redirect('/')



@app.route('/admin')
@login_required
def render_admin_page():
    """Renders admin homepage"""

    if session['admin'] == True:
        admin = Admin.query.filter_by(username=session['username']).first()
        if admin.super_admin:
            super_admin = True
            return render_template('admin.html', super_admin=super_admin)
        else:
            super_admin = False
            return render_template('admin.html', super_admin=super_admin)
    else:
        flash('You do not have access to this page')
        return redirect('/')


@app.route('/appointments')
@login_required
def render_appts_page():
    """Renders the appointments page"""

    if session['admin'] == True:
        upcoming_appts = {}
        all_upcoming = crud.view_all_upcoming_appts()
        
        for appt in all_upcoming:
            upcoming_appts[appt] = appt.appointment_slot.start_time.strftime("%B %d, %Y %I:%M%p")

        return render_template('appointments.html', upcoming_appts=upcoming_appts)
    else:
        flash("You do not have access to this page")
        return redirect('/')



@app.route('/create-appointment-slots')
@login_required
def renders_create_appt_slot_page():
    """Renders page to allow admins to create available appointment slots"""

    if session['admin'] == True:
        return render_template('admin_appt_slots.html')
    else:
        flash("You do not have access to this page")
        return redirect('/')


@app.route('/handle-create-appt-slots', methods=["POST"])
@login_required
def handle_create_appt_slots():
    """Creates appointment slots defined by admin"""

    start_time_str = request.form.get('start-time')
    end_appts_str = request.form.get('end-time')

    # Changing start time and end times to datetime objects
    date_format = "%Y-%m-%dT%H:%M"
    start_time = datetime.strptime(start_time_str, date_format)
    end_appts = datetime.strptime(end_appts_str, date_format)

    if int(request.form.get('time-delta')) < 0:
        flash('Please enter a positive number')
        return redirect('/create-appointment-slots')

    desired_delta = int(request.form.get('time-delta'))
    delta = timedelta(minutes=desired_delta)
    
    while start_time <= end_appts:
        end_time = start_time + delta
        date = start_time.date()
        appt_slot = crud.create_appointment_slot(start_time, end_time, date)
        start_time += delta
    
    flash('Appointment slots created.')
    
    return redirect('/admin')


@app.route('/delete-appointment-slots')
@login_required
def render_delete_appt_slot_page():
    """Allows admins to delete selected available appointment slots"""

    if session['admin'] == True:
        available_appts = {}
        all_appt_slots = crud.view_all_appt_slots()
        for appt_slot in all_appt_slots:
            if appt_slot.appointment == []:
                available_appts[appt_slot] = appt_slot.start_time.strftime("%B %d, %Y at %I:%M%p")
  
        return render_template('admin_delete_appt_slots.html',
                                available_appts=available_appts)
    else:
        flash('You do not have access to this page.')
        return redirect('/')


@app.route('/handle-delete-appt-slots', methods=["POST"])
@login_required
def handle_delete_appt_slots():
    """Deletes appointment slots selected by admin"""

    slots = request.form.getlist('avail-slot')
    
    slots_to_delete = []

    for slot_to_delete in slots:
        slot = crud.string_to_ApptSlot(slot_to_delete)
        slots_to_delete.append(slot)
    
    for slot in slots_to_delete:
        print("*" * 20)
        print(slot.start_time)
        start_time = slot.start_time
        crud.delete_ApptSlot(slot.start_time)
    
    flash('Selected appointment slots deleted.')

    return redirect('/')


@app.route('/create-new-admin')
@login_required
def render_new_admin_form():
    """Renders form to create new Admin"""

    if session['admin'] == True:
        return render_template('admin_create_admin.html')
    else:
        flash('You do not have access to this page.')
        return redirect('/')


@app.route('/handle-new-admin', methods=["POST"])
@login_required
def handle_new_admin():
    """Creates new Admin from form input"""

    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    super_admin = request.form.get('super-admin')
    if super_admin == "True":
        super_admin = True
    elif super_admin == "False":
        super_admin = False

    if username in crud.view_all_usernames():
        flash('Username already taken')
        return redirect('/create-new-admin')
    elif username in crud.view_all_admin_usernames():
        flash('Username already taken')
        return redirect('/create-new-admin')      
    else:
        crud.create_admin(fname, lname, email, username, password, super_admin)

        flash(f'{fname} {lname} now has admin access.')
        return redirect('/')


@app.route('/create-user-appt')
@login_required
def render_admin_create_appt():
    """Allows admins to manually create a user appointment"""

    if session['admin'] == True:
        return render_template('admin_user_appt_create.html')
    else:
        flash('You do not have access to this page.')
        return redirect('/')


@app.route('/handle-admin-create-user-household', methods=["POST"])
def handle_admin_create_user_household():
    """Creates user and household based on admin input"""

    # User information
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    phone_number = request.form.get('phone-number')
    user = crud.create_user(fname, lname, phone_number=phone_number)

    #Household info
    num_people = request.form.get('num-people')
    wants_peanut_butter = request.form.get('wants-peanut-butter')
    picking_up_for_another = request.form.get('picking-up-for-another')
    another_pickup_name = request.form.get('pickup-for')
    allergies = request.form.get('allergies')
    special_requests = request.form.get('special-requests')
    # Changing strings to appropriate data type to create instance
    if allergies == "":
        allergies = None
    if special_requests == "":
        special_requests = None
    
    if wants_peanut_butter == "True":
        wants_peanut_butter = True
    else:
        wants_peanut_butter = False
    
    if picking_up_for_another == "true":
        picking_up_for_another = True
    else:
        picking_up_for_another = False
    
    household = crud.create_household(user, num_people, wants_peanut_butter,
                                    picking_up_for_another, another_pickup_name,
                                    allergies, special_requests)

    available_appts = {}
    all_appt_slots = crud.view_all_appt_slots()
    for appt_slot in all_appt_slots:
        if appt_slot.appointment == []:
            available_appts[appt_slot] = appt_slot.start_time.strftime("%B %d, %Y at %I:%M%p")
    
    return render_template('admin_schedule_appt.html',
                            available_appts=available_appts,
                            user_id=user.user_id,
                            household_id=household.household_id,
                            fname=fname, lname=lname)


@app.route('/handle-admin-create-appt', methods=["POST"])
def admin_create_appt():
    """Admin creates appointment for user"""

    user_id = request.form.get('user-id')
    household_id = request.form.get('household-id')
    user = User.query.get(user_id)
    household = Household.query.get(household_id)
    selected_appt_slot_str = request.form.get('appt_slot')
    selected_appt_slot = crud.string_to_ApptSlot(selected_appt_slot_str)

    crud.create_appointment(user, selected_appt_slot, household)

    flash(f'Appointment for {user.fname} {user.lname} successfully scheduled.')

    return redirect('/')


@app.route('/render-send-reminders')
@login_required
def render_send_reminders_page():
    """Renders page for admin to send reminders"""

    if session['admin'] == True:
        upcoming_appts = crud.view_all_upcoming_appts()

        return render_template('admin_reminders.html', upcoming_appts=upcoming_appts)
    else:
        flash('You do not have access to this page.')
        return redirect('/')


@app.route('/handle-send-reminders', methods=["POST"])
def handle_send_reminders():
    """Handles sending SMS reminders with Twilio"""

    appt_ids = request.form.getlist('remind')

    appt_phone_nums = crud.get_appt_phone_nums(appt_ids)

    for phone in appt_phone_nums:
        to_num = f'+1{appt_phone_nums[phone][0]}'
        msg_body = f'''Hello, {phone}! This is PanTrack reminding you of your appointment to pickup food at {appt_phone_nums[phone][1]}.'''
        crud.send_sms(to_num, msg_body)
    
    flash('Appointment SMS reminders sent.')
    
    return redirect('/')

@app.route('/delete-admin')
@login_required
def render_delete_admin_page():
    """Renders page for super admin to delete admin"""

    if session['admin'] == True:
        all_admin = crud.view_all_admin()

        return render_template('delete_admin.html', all_admin=all_admin)
    else:
        flash('You do not have access to this page.')
        return redirect('/')


@app.route('/handle-delete-admin', methods=["POST"])
@login_required
def handle_delete_admin():
    """Handles the deletion of selected Admin"""

    admin_ids = request.form.getlist('admin')

    for idx, admin_id in enumerate(admin_ids):
        admin_ids[idx] = int(admin_id)
    
    for admin in admin_ids:
        crud.delete_Admin(admin)

    flash('Admin deleted.')

    return redirect('/')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug=True, use_reloader=True, use_debugger=True)