"""Server for PanTrack app"""

from flask import (Flask, render_template, request, flash, session,
                    redirect)
from model import connect_to_db, User
from jinja2 import StrictUndefined
import crud
from flask_login import LoginManager, login_user, login_required

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

    if 'username' in session:
        return render_template('homepage.html')
    else:
        return render_template('log_in_page.html')


# @app.route('/log-in')
# def render_user_log_in():
#     """Renders page for user to log in"""

#     return render_template('log_in_page.html')


@app.route('/log-in', methods=["POST"])
def handle_log_in():
    """Save session and return to homepage and process log in"""

    # session['username'] = request.form['username']
    # session['password'] = request.form['password']

    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()
    # print(user)

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

    return render_template('homepage.html', user=new_user)




if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug=True, use_reloader=True, use_debugger=True)