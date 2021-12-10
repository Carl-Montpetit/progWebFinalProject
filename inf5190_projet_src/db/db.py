import sqlite3
import csv
import requests
import xml.etree.ElementTree as elementTree

################################################################################
# CONSTANTS
################################################################################
URL_CSV_PISCINES_INSTALLATIONS_AQUATIQUES = "https://data.montreal.ca/dataset/4604afb7-a7c4-4626-a3ca-e136158133f2/resource/cbdca706-569e-4b4a-805d-9af73af03b14/download/piscines.csv"
INSERT_PISCINES_INSTALLATIONS_AQUATIQUES = "INSERT INTO piscines_installations_aquatiques (id_uev, type, nom, arrondissement, adresse, propriete, gestion, point_x, point_y, equipement, longitude, latitude) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
DROP_PISCINES_INSTALLATIONS_AQUATIQUES = "DROP TABLE IF EXISTS piscines_installations_aquatiques;"
DELETE_TITLES_ROW_PISCINES_INSTALLATIONS_AQUATIQUES = "DELETE FROM " \
                                                     "piscines_installations_aquatiques WHERE id=1"
CREATE_PISCINES_INSTALLATIONS_AQUATIQUES = "CREATE TABLE piscines_installations_aquatiques(id INTEGER PRIMARY KEY AUTOINCREMENT, id_uev INTEGER, type VARCHAR(100), nom VARCHAR(100), arrondissement VARCHAR(100), adresse VARCHAR(100), propriete VARCHAR(100), gestion VARCHAR(100), point_x INTEGER, point_y INTEGER, equipement VARCHAR(100), longitude INTEGER, latitude INTEGER);"
URL_XML_PATINOIRES = "https://data.montreal.ca/dataset/225ac315-49fe-476f-95bd-a1ce1648a98c/resource/5d1859cc-2060-4def-903f-db24408bacd0/download/l29-patinoire.xml"
INSERT_PATINOIRES = "INSERT INTO patinoires (nom_arr, nom_pat, date_heure, " \
                    "ouvert, deblaye, arrose, resurface) VALUES (?, ?, " \
                    "?, ?, ?, ?, ?);"
DROP_PATINOIRES = "DROP TABLE IF EXISTS patinoires;"
CREATE_PATINOIRES = "CREATE TABLE patinoires(id INTEGER PRIMARY KEY " \
                    "AUTOINCREMENT, nom_arr VARCHAR(200), nom_pat VARCHAR(" \
                    "100), date_heure TEXT," \
                    "ouvert NUMERIC, deblaye NUMERIC, arrose NUMERIC," \
                    "resurface NUMERIC);"
URL_XML_GLISSADES = "http://www2.ville.montreal.qc.ca/services_citoyens/pdf_transfert/L29_GLISSADE.xml"
INSERT_GLISSADES = "INSERT INTO glissades (nom, nom_arr, cle, " \
                   "date_maj, ouvert, deblaye, condition) VALUES (?, ?, " \
                   "?, ?, ?, ?, ?);"
DROP_GLISSADES = "DROP TABLE IF EXISTS glissades;"
CREATE_GLISSADES = "CREATE TABLE glissades(id INTEGER PRIMARY KEY " \
                   "AUTOINCREMENT, nom VARCHAR(200), nom_arr VARCHAR(" \
                   "100), cle VARCHAR(100), date_maj TEXT," \
                   "ouvert NUMERIC, deblaye NUMERIC, " \
                   "condition VARCHAR(100));"


################################################################################
# STATIC FUNCTIONS
################################################################################
def get_csv_data_from_url(url):
    """Get the piscines data"""
    with requests.Session() as s:
        response = s.get(url)
    decoded_content = response.content.decode('utf-8')
    root = csv.reader(decoded_content.splitlines(), delimiter=',')
    rows = list(root)
    return rows


def get_xml_data_from_url(url):
    """Get the glissade data"""
    with requests.Session() as s:
        response = s.get(url)
    decoded_content = response.content.decode('utf-8')
    tree = elementTree.fromstring(decoded_content)
    return tree


def download_xml_file_from_url(url):
    with requests.Session() as s:
        response = s.get(url)
    content = response.content
    with open('patinoires.xml', 'wb') as file:
        file.write(content)


def print_xml_tree(root):
    print(elementTree.tostring(root, encoding='utf8').decode('utf8'))
    return 1


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
        cursor.execute(DELETE_TITLES_ROW_PISCINES_INSTALLATIONS_AQUATIQUES)
        connection.commit()
        connection.close()
        self.disconnect()

    def add_patinoires_data_to_database(self):
        """add XML data from url to database : O(i*j*k) where i < j << k"""
        connection = self.get_connection()
        cursor = connection.cursor()
        root = get_xml_data_from_url(URL_XML_PATINOIRES)
        arrondissements = root.findall("arrondissement")
        for arrondissement in arrondissements:
            nom_arr = arrondissement.find("nom_arr").text.strip()
            patinoires = arrondissement.find("patinoire")
            noms_pats = patinoires.findall("nom_pat")
            conditions = patinoires.findall("condition")
            for j, nom in enumerate(noms_pats):
                nom_pat = nom.text.strip()
                for k in range(int(len(conditions) / len(noms_pats))):
                    date_heure = conditions[k + j * int(len(
                        conditions) / len(noms_pats))][0].text.strip()
                    ouvert = conditions[k + j * int(len(
                        conditions) / len(noms_pats))][1].text.strip()
                    deblaye = conditions[k + j * int(len(
                        conditions) / len(noms_pats))][2].text.strip()
                    arrose = conditions[k + j * int(len(
                        conditions) / len(noms_pats))][3].text.strip()
                    resurface = conditions[k + j * int(len(
                        conditions) / len(noms_pats))][4].text.strip()
                    cursor.execute(INSERT_PATINOIRES, (
                        nom_arr, nom_pat, date_heure, ouvert, deblaye, arrose,
                        resurface))
        connection.commit()
        connection.close()
        self.disconnect()

    def add_glissades_data_to_database(self):
        """add XML data from url to database"""
        connection = self.get_connection()
        cursor = connection.cursor()
        glissades = get_xml_data_from_url(URL_XML_GLISSADES)
        glissades_data = []
        for glissade in glissades:
            nom = glissade.find("nom").text.strip()
            nom_arr = glissade.find("arrondissement").find(
                "nom_arr").text.strip()
            cle = glissade.find("arrondissement").find("cle").text.strip()
            date_maj = glissade.find("arrondissement").find(
                "date_maj").text.strip()
            ouvert = glissade.find("ouvert").text
            deblaye = glissade.find("deblaye").text.strip()
            condition = glissade.find("condition").text.strip()
            total = (nom, nom_arr, cle, date_maj, ouvert, deblaye, condition)
            glissades_data.append(total)
        cursor.executemany(INSERT_GLISSADES, glissades_data)
        connection.commit()
        connection.close()
        self.disconnect()

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

    def create_patinoires_table(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(DROP_PATINOIRES)
        cursor.execute(CREATE_PATINOIRES)
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
