################################################################################
# LIBRARY #
################################################################################
from db.db import Database
from datetime import datetime
from flask_bootstrap import Bootstrap
from flask import render_template, redirect, request, url_for, flash, Flask, \
    jsonify, make_response, abort, session, get_flashed_messages
from apscheduler.schedulers.background import BackgroundScheduler
import time
import pytz

################################################################################
# CONSTANTS #
################################################################################
ERROR_TEMPLATE = 'error.html'

################################################################################
# INITIALIZE FLASK APPLICATION #
################################################################################
local_time_quebec_canada = datetime.now(pytz.timezone('America/Toronto'))
# Create and initialize a Flask application called app
app = Flask(
    __name__, static_folder="static", template_folder="templates",
    static_url_path=""
)

app.config['SECRET_KEY'] = 'hard_to_guess_string'

# link flask-bootstrap with the application
bootstrap = Bootstrap(app)

# create a database object called db
db = Database()

# link scheduler with the application
scheduler = BackgroundScheduler(daemon=True)


################################################################################
# SCHEDULER #
################################################################################

def scheduled_database_update():
    db.create_piscines_installations_aquatiques_table()
    db.add_piscines_installations_aquatiques_data_to_database()
    # db.create_glissades_table()
    # db.add_glissades_data_to_database()
    # db.create_patinoires_table()
    # db.add_patinoires_data_to_database()
    print('The database was updated at {}'.format(local_time_quebec_canada))


# Update database every day at midnight
scheduler.add_job(scheduled_database_update, 'cron', hour='0', day='*')
scheduler.start()


################################################################################
# ERROR HANDLERS #
################################################################################


@app.errorhandler(400)
def bad_request(error):
    return render_template(ERROR_TEMPLATE, error=error), 400


@app.errorhandler(401)
def unauthorized(error):
    return render_template(ERROR_TEMPLATE, error=error), 401


@app.errorhandler(403)
def forbidden(error):
    return render_template(ERROR_TEMPLATE, error=error), 403


@app.errorhandler(404)
def not_found(error):
    return render_template(ERROR_TEMPLATE, error=error), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template(ERROR_TEMPLATE, error=error), 500


@app.errorhandler(501)
def not_implemented_yet(error):
    return render_template(ERROR_TEMPLATE, error=error), 501


@app.errorhandler(503)
def service_unavailable(error):
    return render_template(ERROR_TEMPLATE, error=error), 503


################################################################################
# REST SERVICES #
################################################################################


@app.route("/")
def index():
    """main route of application"""
    print(local_time_quebec_canada)
    return render_template("home.html")


################################################################################
# This is always true if app.py is used as entry point of the interpreter #
################################################################################
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
################################################################################
# END OF FILE #
################################################################################
