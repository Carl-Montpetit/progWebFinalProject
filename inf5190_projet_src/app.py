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
import os
import json
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
from tabulate import tabulate

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
local_time = pytz.timezone("America/Toronto")

app = Flask(
    __name__, static_url_path="", root_path='',
    static_folder='static', template_folder='templates'
)

# link flask-bootstrap with the application
bootstrap = Bootstrap(app)

# create a database object called db
db = Database()

###############################################################################
# SCHEDULER #
###############################################################################
# link scheduler with the application
scheduler = BackgroundScheduler(timezone=local_time, daemon=True)


def scheduled_database_update():
    """Update the database from HTTP request from URLs"""
    db.create_piscines_installations_aquatiques_table()
    db.add_piscines_installations_aquatiques_data_to_database()
    db.create_glissades_table()
    db.add_glissades_data_to_database()
    db.create_patinoires_table()
    db.add_patinoires_data_to_database()
    print('The database was updated at {}'.format(datetime.now(local_time)))


# FIXME
# Update database every day at midnight
scheduler.add_job(scheduled_database_update, 'cron', hour='0', minute='0',
                  day='*')
scheduler.start()


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
    return render_template('home.html'), 200


@app.route('/districts', methods=['GET'])
def get_installations_for_arrondissement():
    """
    Return all installations for a specific query string entered as an
    arrondissement in JSON format on the browser. If there's no query
    string, render a html template.
    """
    # Getting the query string parameter for arrondissement
    arrondissement = str(request.args.get('arrondissement', None))
    if len(arrondissement) < 4 or len(arrondissement) > 40 or not \
            isinstance(arrondissement, str) or arrondissement is None or \
            arrondissement == '' or arrondissement == 'None':
        return render_template('error.html',
                               error=ERR_MSG_ARR_QUERY_FORMAT), 404
    installations_dict = get_data_for_arrondissement_as_dictionnaries(
        arrondissement)
    # installations_list = get_data_for_arrondissement(arrondissement)
    if dict is None or len(installations_dict) == 0:
        return render_template('error.html',
                               error=ERR_MSG_NO_INSTALLATIONS_FOR_ARR), 404
    json_object = jsonify(installations_dict)
    return json_object, 200
    # return Response(tabulate({"Installations List": installations_list},
    #                          headers='keys',
    #                          tablefmt='html').encode('utf-8'),
    #                 content_type='charset=UTF-8'), 200


@app.route('/districts/2021', methods=['GET'])
def get_installations_list_2021():
    """Return all installations data updated in 2021 in JSON format."""
    installations_list = get_installations_data_2021()
    if installations_list is None or len(installations_list) == 0:
        return abort(404)
    formated_data = jsonify(installations_list)
    return formated_data, 200


@app.route('/districts/all-installations', methods=['GET'])
def get_all_installations_list():
    """Return all installationst data."""
    installations_list = get_all_installations_names()
    if installations_list is None or len(installations_list) == 0:
        return abort(404)
    return render_template('specific-installation.html',
                           installations=list(installations_list)), 200


@app.route('/districts/all-installations/<string:specific>', methods=[
    'GET'])
def get_all_specific_installation_data(specific):
    specific_data = get_all_specific_installation_data(specific)
    if specific_data is None or len(specific_data) == 0:
        abort(404)
    json_data = jsonify(specific_data)
    return json_data, 200


@app.route('/districts/2021/installations-2021.xml',
           methods=['GET'])
def get_XML_formated_installations_list_2021():
    """Return all installations data updated in 2021 in JSON format."""
    installations_list = get_installations_data_2021()
    if installations_list is None or len(installations_list) == 0:
        return abort(404)
    formated_data = parseString(dicttoxml(installations_list)).toprettyxml()
    return Response(formated_data, content_type='application/xhtml+xml'), 200


@app.route('/districts/2021/installations-2021.csv', methods=['GET'])
def get_CSV_formated_installations_list_2021():
    """Return all installations data updated in 2021 in CSV format."""
    installations_list = get_installations_data_2021()
    if installations_list is None or len(installations_list) == 0:
        return abort(404)
    formated_data = parseString(dicttoxml(installations_list)).toprettyxml()
    df = pd.DataFrame(installations_list[0] + installations_list[
        1] + installations_list[2])
    df.to_csv('data.csv', index=False, header=False, encoding='utf-8')
    csv_string = open('data.csv', mode='r', encoding='utf-8')
    return Response(csv_string, content_type='img/svg+xml'), 200


@app.route('/doc', methods=['GET'])
def doc():
    """Render a template containing all REST services documentation"""
    return render_template('services.html'), 200


###############################################################################
# FUNCTIONS #
###############################################################################
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
    installations_list = (installations_piscines + installations_patinoires
                          + installations_glissades)
    return installations_list


def get_data_for_arrondissement_as_dictionnaries(arrondissement):
    """Return all installations data for a specific arrondissement as dict"""
    installations_piscines = \
        db.get_piscines_installations_dict_from_arrondissement(arrondissement)
    installations_patinoires = \
        db.get_patinoires_installations_dict_from_arrondissement(
            arrondissement)
    installations_glissades = \
        db.get_glissades_installations_dict_from_arrondissement(arrondissement)
    installations_list = [installations_piscines, installations_patinoires,
                          installations_glissades]
    return installations_list


def get_installations_data_2021():
    """Return all installations updated in 2021 data from all tables"""
    installations_piscines = db.get_piscines_installations_2021()
    installations_patinoires = db.get_patinoires_installations_2021()
    installations_glissades = db.get_patinoires_installations_2021()
    installations_list = [installations_piscines, installations_patinoires,
                          installations_glissades]
    return installations_list


def get_all_installations_names():
    """Return all installations name updated in 2021 data from all tables"""
    installations_piscines = db.get_all_piscines_names()
    installations_patinoires = db.get_all_patinoires_names()
    installations_glissades = db.get_all_glissades_names()
    installations_list = [installations_piscines, installations_patinoires,
                          installations_glissades]
    return installations_list


def get_all_specific_installation_data(specific):
    """Return all installations name updated in 2021 data from all tables"""
    specific_piscines = db.get_specific_piscine_data(specific)
    specific_patinoires = db.get_specific_patinoire_data(specific)
    specific_glissades = db.get_specific_glissade_data(specific)
    specific_list = [specific_piscines + specific_patinoires +
                     specific_glissades]
    return specific_list


###############################################################################
# This is always true if app.py is used as entry point of the interpreter #
###############################################################################
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
###############################################################################
# END OF FILE #
###############################################################################
