"""Server for PanTrack app"""

from flask import (Flask, render_template, request, flash, session,
                    redirect)
from model import connect_to_db, User
from jinja2 import StrictUndefined
import crud
from flask_login import (LoginManager, login_user, login_required,
                        logout_user, current_user)

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def render_hompeage():
    """Displays the homepage is user in session"""

    # user = User.query.filter_by(username=session['username']).first()

    # if len(user.appointments) != 0:
    #     user_next_appt = user.appointments[-1]

    if current_user.is_authenticated:
        user = User.query.filter_by(username=session['username']).first()
        if len(user.appointments) != 0:
            has_appt = True
            user_next_appt = user.appointments[-1].appointment_slot.start_time
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


    if user is None:
        flash("Sorry try again.")
        return redirect("/")


    if user.password == password:
        # Call flask_login.login_user to login a user
        login_user(user)

        flash("Logged in successfully!")

        #Add user to session
        session['username'] = request.form['username']
        session['password'] = request.form['password']

        return redirect('/')
    
    flash("Sorry try again.")
    return redirect("/")
  

    # return render_template('homepage.html', session=session)


@app.route('/logout')
@login_required
def logout():
    # username = session['username']
    # user = User.query.filter_by(username=username).first()
    logout_user()
    return render_template('log_in_page.html')

@app.route('/create-account')
def render_create_account_form():
    """Renders form for user to create an account"""

    return render_template('create_account.html')


@app.route('/handle-create-account', methods=["POST"])
def create_user_account():
    """Creates user account based off info provided in form"""

    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    phone_number = request.form['phone-number']

    new_user = crud.create_user(fname, lname, email, username, password, phone_number)

    login_user(new_user)
    session['username'] = request.form['username']
    session['password'] = request.form['password']

    return redirect('/')

    # return render_template('homepage.html')

@app.route('/schedule-appointment')
def render_schedule_appointment_page():
    """Renders page to schedule an appointment"""

    available_appts = []
    all_appt_slots = crud.view_all_appt_slots()
    for appt_slot in all_appt_slots:
        if appt_slot.appointment == []:
            available_appts.append(appt_slot)
    return render_template('schedule_appointment.html', available_appts=available_appts)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug=True, use_reloader=True, use_debugger=True)