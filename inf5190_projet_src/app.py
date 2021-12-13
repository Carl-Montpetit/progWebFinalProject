###############################################################################
# LIBRARY #
###############################################################################
import csv
import json

import pandas as pd
import pytz_deprecation_shim
import tzlocal
import time
import pytz
import yaml

from db.db import Database
from datetime import datetime
from flask_bootstrap import Bootstrap
from flask import render_template, redirect, request, url_for, flash, Flask, \
    jsonify, make_response, abort, session, get_flashed_messages, Response
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from yaml.loader import SafeLoader
from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField
from wtforms.validators import DataRequired, length
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString, parse

###############################################################################
# CONSTANTS #
###############################################################################
ERROR_TEMPLATE = 'error.html'
ERR_MSG_ARR_QUERY_FORMAT = 'Error, the arrondissement name format is invalid!'
ERR_MSG_NO_INSTALLATIONS_FOR_ARR = "Error, there's no installations found " \
                                   "for that district!"
###############################################################################
# INITIALIZE FLASK APPLICATION #
###############################################################################
# CA = pds.timezone("Canada/Eastern")
local_time = pytz.timezone("America/Toronto")
app = Flask(
    __name__, static_folder="static", template_folder="templates",
    static_url_path=""
)
app.config['SECRET_KEY'] = 'hard_to_guess_string'

# link flask-bootstrap with the application
bootstrap = Bootstrap(app)

# create a database object called db
db = Database()


###############################################################################
# SCHEDULER #
###############################################################################
# link scheduler with the application
# scheduler = BackgroundScheduler(timezone=local_time, daemon=True)


def scheduled_database_update():
    db.create_piscines_installations_aquatiques_table()
    db.add_piscines_installations_aquatiques_data_to_database()
    db.create_glissades_table()
    db.add_glissades_data_to_database()
    db.create_patinoires_table()
    db.add_patinoires_data_to_database()
    print('The database was updated at {}'.format(datetime.now(local_time)))


# Update database every day at midnight
# scheduler.add_job(scheduled_database_update, 'cron', hour='0', minute='0',
#                   day='*')
# scheduler.start()


###############################################################################
# ERROR HANDLERS #
# To see this well in action (ex: 50X code errors) debug mode must be
# turned off
###############################################################################


@app.errorhandler(400)
def bad_request(error):
    """If 404 error occurs, render a template to notice it"""
    return render_template(ERROR_TEMPLATE, error=error), 400


@app.errorhandler(401)
def unauthorized(error):
    """If 401 error occurs, render a template to notice it"""
    return render_template(ERROR_TEMPLATE, error=error), 401


@app.errorhandler(403)
def forbidden(error):
    """If 403 error occurs, render a template to notice it"""
    return render_template(ERROR_TEMPLATE, error=error), 403


@app.errorhandler(404)
def not_found(error):
    """If 404 error occurs, render a template to notice it"""
    return render_template(ERROR_TEMPLATE, error=error), 404


@app.errorhandler(500)
def internal_server_error(error):
    """If 500 error occurs, render a template to notice it"""
    return render_template(ERROR_TEMPLATE, error=error), 500


@app.errorhandler(501)
def not_implemented_yet(error):
    """If 501 error occurs, render a template to notice it"""
    return render_template(ERROR_TEMPLATE, error=error), 501


@app.errorhandler(503)
def service_unavailable(error):
    """If 503 error occurs, render a template to notice it"""
    return render_template(ERROR_TEMPLATE, error=error), 503


###############################################################################
# REST SERVICES #
###############################################################################


@app.route('/', methods=['GET'])
def main_page():
    """Render the main template of the application"""
    return render_template('home.html'), 200


@app.route('/installations', methods=['GET'])
def get_installations_for_arrondissement():
    """
    Return all installations for a specific query string entered as an
    arrondissement in JSON format on the browser. If there's no query
    string, render a html template.
    """
    # Getting the query string parameter for arrondissement
    arrondissement = str(request.args.get('arrondissement', None))
    if arrondissement is None or arrondissement == '' or arrondissement == \
            'None':
        return render_template('installations.html')
    elif len(arrondissement) < 4 or len(arrondissement) > 40 or not \
            isinstance(arrondissement, str):
        return render_template('error.html',
                               error=ERR_MSG_ARR_QUERY_FORMAT), 404
    installations_list = get_data_for_arrondissement(arrondissement)
    if installations_list is None or len(installations_list) == 0:
        return render_template('error.html',
                               error=ERR_MSG_NO_INSTALLATIONS_FOR_ARR), 404
    json_installations = jsonify(installations_list)
    return json_installations, 200


@app.route('/installations/2021', methods=['GET'])
def get_installations_list_2021():
    installations_list = get_installations_data_2021()
    if installations_list is None or len(installations_list) == 0:
        return abort(404)
    formated_data = jsonify(installations_list)
    return formated_data, 200


@app.route('/installations/2021/installations-2021.xml',
           methods=['GET'])
def get_XML_formated_installations_list_2021():
    """Return all installations data updated in 2021 in JSON format."""
    installations_list = get_installations_data_2021()
    if installations_list is None or len(installations_list) == 0:
        return abort(404)
    formated_data = parseString(dicttoxml(installations_list)).toprettyxml()
    return Response(formated_data, content_type='application/xhtml+xml')


@app.route('/installations/2021/installations-2021.csv', methods=['GET'])
def get_CSV_formated_installations_list_2021():
    """Return all installations data updated in 2021 in CSV format."""
    installations_list = get_installations_data_2021()
    if installations_list is None or len(installations_list) == 0:
        return abort(404)
    formated_data = parseString(dicttoxml(installations_list)).toprettyxml()
    df = pd.DataFrame(installations_list)
    df.to_csv('data.csv', index=False, header=False, encoding='utf-8')
    csv_string = open('data.csv', mode='r', encoding='utf-8')
    return Response(csv_string, content_type='img/svg+xml')


def get_data_for_arrondissement(arrondissement):
    """Return all installations from all tables for specific arrondissement"""
    installations_piscines = \
        db.get_piscines_installations_list_from_arrondissement(
            arrondissement)
    installations_patinoires = \
        db.get_patinoires_installations_list_from_arrondissement(
            arrondissement)
    installations_glissades = \
        db.get_glissades_installations_list_from_arrondissement(
            arrondissement)
    installations_list = (
            installations_piscines + installations_patinoires +
            installations_glissades)
    return installations_list


def get_installations_data_2021():
    """Return all installations updated in 2021 data from all tables"""
    installations_piscines = db.get_piscines_installations_2021()
    installations_patinoires = db.get_patinoires_installations_2021()
    installations_glissades = db.get_patinoires_installations_2021()
    installations_list = (installations_piscines + installations_patinoires
                          + installations_glissades)
    return installations_list


@app.route('/doc', methods=['GET'])
def doc():
    """Render a template containing all REST services documentation"""
    return render_template('services.html'), 200


###############################################################################
# This is always true if app.py is used as entry point of the interpreter #
###############################################################################
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
###############################################################################
# END OF FILE #
###############################################################################
