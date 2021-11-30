import sqlite3
import csv
import urllib3
import requests
import traceback
import xml
import dicttoxml
import urllib3
################################################################################
# CONSTANTS
################################################################################
URL_CSV_PISCINES_INSTALLATIONS_AQUATIQUES = "https://data.montreal.ca/dataset/4604afb7-a7c4-4626-a3ca-e136158133f2/resource/cbdca706-569e-4b4a-805d-9af73af03b14/download/piscines.csv"
INSERT_PISCINES_INSTALLATIONS_AQUATIQUES = "INSERT INTO piscines (id_uev, type, nom, arrondissement, adresse, propriete, gestion, point_x, point_y, equipement, longitude, latitude) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
DROP_PISCINES_INSTALLATIONS_AQUATIQUES = "DROP TABLE IF EXISTS piscines_installations_aquatiques;"
CREATE_PISCINES_INSTALLATIONS_AQUATIQUES = "CREATE TABLE piscines_installations_aquatiques(id INTEGER PRIMARY KEY AUTOINCREMENT, id_uev INTEGER, type varchar(100), nom varchar(100), arrondissement varchar(100), adresse varchar(100), propriete varchar(100), gestion varchar(100), point_x INTEGER, point_y INTEGER, equipement varchar(100), longitude INTEGER, latitude INTEGER);"
URL_XML_PATINOIRES = "https://data.montreal.ca/dataset/225ac315-49fe-476f-95bd-a1ce1648a98c/resource/5d1859cc-2060- 4def-903f-db24408bacd0/download/l29-patinoire.xml"
INSERT_PATINOIRES = ""
DROP_PATINOIRES = ""
CREATE_PATINOIRES = ""
URL_XML_GLISSADES = "http://www2.ville.montreal.qc.ca/services_citoyens/pdf_transfert/L29_GLISSADE.xml"
INSERT_GLISSADES = ""
DROP_GLISSADES = "DROP TABLE IF EXISTS glissades;"
CREATE_GLISSADES = ""

################################################################################
# STATIC FUNCTIONS
################################################################################


def to_dict(dict_name, cursor):
    return [dict(dict_name) for dict_name in cursor.fetchall()]


def get_csv_data_from_url(url):
    """Get the piscines data"""
    with requests.Session() as s:
        download = s.get(url)
    decoded_content = download.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    rows = list(cr)
    for row in rows:
        print(row)
    return rows


def get_xml_data_from_url(url):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    try:
        data = xmltodict.parse(response.data)
    except ValueError:
        print("Failed to parse xml from response (%s)" %
              traceback.format_exc())
    return data
################################################################################
# DATABASE OBJECT
################################################################################


class Database:
    ############################################################################
    # CONSTRUCTOR
    ############################################################################
    def __init__(self):
        self.connection = None
    ############################################################################
    # FUNCTIONS
    ############################################################################

    def get_connection(self):
        """Open database connection. Should be closed after use"""
        if self.connection is None:
            self.connection = sqlite3.connect(
                "db/db.db", check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        return self.connection

    def disconnect(self):
        """Disconnect from database"""
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def add_piscines_installations_aquatiques_data_to_database(self):
        """add csv data from url to database"""
        connection = self.get_connection()
        cursor = connection.cursor()
        rows = get_csv_data_from_url(URL_CSV_PISCINES_INSTALLATIONS_AQUATIQUES)
        cursor.executemany(INSERT_PISCINES_INSTALLATIONS_AQUATIQUES, rows)
        connection.commit()
        connection.close()

    def add_patinoires_data_to_database(self):
        """add XML data from url to database"""
        connection = self.get_connection()
        cursor = connection.cursor()
        rows = get_csv_data_from_url(URL_XML_PATINOIRES)
        cursor.executemany(INSERT_PATINOIRES, rows)
        connection.commit()
        connection.close()
        self.disconnect()

    def add_glissades_data_to_database(self):
        """add XML data from url to database"""
        connection = self.get_connection()
        cursor = connection.cursor()
        rows = get_csv_data_from_url(URL_XML_GLISSADES)
        cursor.executemany(INSERT_GLISSADES, rows)
        connection.commit()
        connection.close()
        self.disconnect()

    # source: https://pretagteam.com/question/how-to-read-a-csv-file-from-a-url-with-python
    def create_piscines_installations_aquatiques_table(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(DROP_PISCINES_INSTALLATIONS_AQUATIQUES)
        cursor.execute(CREATE_PISCINES_INSTALLATIONS_AQUATIQUES)
        connection.commit()
        connection.close()
        self.disconnect()

    def create_glissades_table(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(DROP_GLISSADES)
        cursor.execute(CREATE_GLISSADES)
        connection.commit()
        connection.close()
        self.disconnect()
################################################################################
# END OF FILE
################################################################################
# def get_five_last_articles(self, today_date):
#     connection = self.get_connection()
#     cursor = connection.cursor()
#
#     cursor.execute(
#         "SELECT * FROM article WHERE date_publication <= \
#             ? ORDER BY date_publication DESC LIMIT 5", (today_date,)
#     )
#     return self.to_dict("article", cursor)

# def get_all_articles(self):
#     connection = self.get_connection()
#     cursor = connection.cursor()
#
#     cursor.execute("SELECT * FROM article ORDER BY date_publication DESC")
#     return self.to_dict("article", cursor)

# def insert_article(self, article):
#     connection = self.get_connection()
#     cursor = connection.cursor()
#
#     cursor.execute(
#         "INSERT INTO article (titre, identifiant, auteur,\
#             date_publication, paragraphe) VALUES (?, ?, ?, ?, ?)",
#         [article[0], article[1], article[2], article[3], article[4]],
#     )
#     connection.commit()
#     return 1

# def modify_article(self, titre, identifiant, paragraphe):
#     connection = self.get_connection()
#     cursor = connection.cursor()
#     cursor.execute(
#         "UPDATE article SET titre = ?, \
#             paragraphe = ? WHERE identifiant = ?",
#         (titre, paragraphe, identifiant)
#     )
#     connection.commit()
#     return 1

# def get_article_by_identifiant(self, identifiant):
#     connection = self.get_connection()
#     cursor = connection.cursor()
#
#     cursor.execute(
#         "SELECT * FROM article WHERE identifiant = ?", (identifiant,))
#     return self.to_dict("article", cursor)

# def get_search_articles(self, search):
#     connection = self.get_connection()
#     cursor = connection.cursor()
#
#     cursor.execute("SELECT * FROM article WHERE titre LIKE ? OR\
#         paragraphe LIKE ? ORDER BY date_publication DESC",
#                    ('%'+search+'%', '%'+search+'%'))
#     return self.to_dict("article", cursor)
