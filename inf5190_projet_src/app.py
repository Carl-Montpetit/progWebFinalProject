################################################################################
# LIBRARY #
################################################################################
from flask import render_template, redirect, request, url_for, flash, Flask, jsonify, make_response, abort, session, get_flashed_messages
from flask_bootstrap import Bootstrap
# from datetime import time
from db.db import Database
import csv

################################################################################
# INITIALIZE FLASK APPLICATION
################################################################################
app = Flask(
    __name__, static_folder="static", template_folder="templates",
    static_url_path=""
)
app.config['SECRET_KEY'] = 'hard_to_guess_string'
bootstrap = Bootstrap(app)
db = Database()
################################################################################
# DATABASE FUNCTIONALITIES (with SQLite) #
################################################################################
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/<db_name>.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
#
#
# class Installations(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(128))
#     specialisation = db.Column(db.String(128))
#
#     def _init_(self, name, specialisation):
#         self.name = name
#         self.specialisation = specialisation
#
#     def __repr__(self):
#         return '<Product %d>' % self.id
#
#     def create(self):
#         db.session.add(self)
#         db.session.commit()
#         return self
#
#
# db.create_all()
#
#
# class InstallationSchema(SQLAlchemySchema):
#     class Meta:
#         model = Installations
#         load_instance = True  # Optional: deserialize to model instances
#
#     id = fields.Number(dumb_only=True)
#     name = fields.String(required=True)
#     specialisation = fields.String(required=True)


################################################################################
#  #
################################################################################


################################################################################
# CONSTANTS #
################################################################################
ERROR_TEMPLATE = 'error.html'


################################################################################
# ERROR HANDLERS #
################################################################################
# @app.errorhandler(301)
# def moved_permanently(error):
#     return render_template(ERROR_TEMPLATE, error=error), 301


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
# SERVICES #
################################################################################
@app.route("/")
def index():
    db.create_piscines_installations_aquatiques_table()
    db.add_piscines_installations_aquatiques_data_to_database()
    db.disconnect()
    return render_template("home.html")


# @app.route('/installations', methods=['GET'])
# def index():
#     get_installations = Installations.query.all()
#     installation_schema = InstallationSchema(many=True)
#     installations = installation_schema.dump(get_installations)
#     return make_response(jsonify({"installations": installations}))

# @app.route('/installations', methods=['POST'])
# def create_author():
#     data = request.get_json()
#     installation_schema = InstallationsSchema()
#     installation = installation_schema.load(data)
#     result = installation_schema.dump(installation.create()).data
#     return make_response(jsonify({"installation": installations}), 201)


################################################################################
# This is always true if app.py is used as entry point of the interpreter #
################################################################################
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
################################################################################
# END OF FILE #
################################################################################
