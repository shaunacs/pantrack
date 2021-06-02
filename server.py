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


@app.route('/log-in', methods=["POST"])
def render_user_log_in():
    """Renders page for user to log in"""

    # session["username"] = request.args["username"]

    return render_template('log_in_page.html')



if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)