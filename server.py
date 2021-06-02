"""Server for PanTrack app"""

from flask import (Flask, render_template, request, flash, session,
                    redirect)
from model import connect_to_db
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def render_hompeage():
    """Displays the homepage"""

    if 'username' in session:
        return render_template('homepage.html')
    else:
        return redirect('/log-in')


@app.route('/log-in')
def render_user_log_in():
    """Renders page for user to log in"""

    return render_template('log_in_page.html')


@app.route('/handle-form-session')
def handle_session_form():
    """Save session and return to homepage"""

    session['username'] = request.args['username']
    session['password'] = request.args['password']

    return render_template('homepage.html', session=session)


@app.route('/create-account')
def render_create_account_form():
    """Renders form for user to create an account"""

    return render_template('create_account.html')


@app.route('/handle-create-account')
def create_user_account():
    """Creates user account based off info provided in form"""

    


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)