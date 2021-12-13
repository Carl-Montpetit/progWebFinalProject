import sqlite3
import csv
import requests
import xml.etree.ElementTree as elementTree

###############################################################################
# CONSTANTS #
###############################################################################
URL_CSV_PISCINES = "https://data.montreal.ca/dataset/4604afb7-a7c4-4626" \
                   "-" + "a3ca-e136158133f2/resource/cbdca706-569e-4b4a-805d" \
                         "-" + "9af73af03b14/download/piscines.csv"
INSERT_PISCINES = """INSERT INTO piscines_installations_aquatiques (id_uev,
type,nom,arrondissement,adresse,propriete,gestion,point_x,point_y,
equipement,longitude,latitude) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
DROP_PISCINES = """DROP TABLE IF EXISTS piscines_installations_aquatiques;"""
# DESTROY_NBSP_PISCINES = """UPDATE piscines_installations_aquatiques SET
# adresse  = REPLACE(adresse, ' ', ' ');"""
DELETE_TITLES_PISCINES = """DELETE FROM piscines_installations_aquatiques
WHERE id=1"""
CREATE_PISCINES = """CREATE TABLE piscines_installations_aquatiques(
id INTEGER  PRIMARY KEY AUTOINCREMENT, id_uev INTEGER, type VARCHAR(100),
nom  VARCHAR(100), arrondissement VARCHAR(100), adresse
VARCHAR(100), propriete VARCHAR(100), gestion  VARCHAR(
100), point_x INTEGER, point_y INTEGER, equipement
VARCHAR(100), longitude INTEGER, latitude INTEGER);"""
URL_XML_PATINOIRES = "https://data.montreal.ca/dataset/225ac315-49fe-476f" \
                     "-95bd -a1ce1648a98c/resource/5d1859cc-2060-4def-903f" \
                     "-db 24408bacd0/download/l29-patinoire.xml"
INSERT_PATINOIRES = """INSERT INTO patinoires (nom_arr, nom_pat, date_heure,
ouvert, deblaye, arrose, resurface) VALUES (?, ?, ?, ?, ?, ?, ?);"""
DROP_PATINOIRES = """DROP TABLE IF EXISTS patinoires;"""
CREATE_PATINOIRES = """CREATE TABLE patinoires(id INTEGER PRIMARY KEY
AUTOINCREMENT, nom_arr VARCHAR(200), nom_pat VARCHAR(100), date_heure TEXT,
ouvert NUMERIC, deblaye NUMERIC, arrose NUMERIC, resurface NUMERIC);"""
URL_XML_GLISSADES = "http://www2.ville.montreal.qc.ca/services_citoyens" \
                    "" + "/pdf_transfert/L29_GLISSADE.xml"
INSERT_GLISSADES = """INSERT INTO glissades (nom, nom_arr, cle, date_maj,
ouvert, deblaye, condition) VALUES (?, ?, ?, ?, ?, ?, ?);"""
DROP_GLISSADES = """DROP TABLE IF EXISTS glissades;"""
CREATE_GLISSADES = """CREATE TABLE glissades(id INTEGER PRIMARY KEY
AUTOINCREMENT, nom VARCHAR(200), nom_arr VARCHAR(100), cle VARCHAR(100),
date_maj TEXT, ouvert NUMERIC, deblaye NUMERIC, condition VARCHAR(100));"""


# EMPTY_IS_NULL_OUVERT_GLISSADES = """UPDATE glissades SET ouvert = NULLIF(
# ouvert, 'None');"""
# EMPTY_IS_NULL_DEBLAYE_GLISSADES = """UPDATE glissades SET deblaye = NULLIF(
# deblaye, 'None');"""


###############################################################################
# STATIC FUNCTIONS FOR DATABASE OBJECT #
###############################################################################


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


def multiple_query_piscines(cursor, rows):
    cursor.executemany(INSERT_PISCINES, rows)
    cursor.execute(DELETE_TITLES_PISCINES)


def get_conditions_fields(conditions, j, k, noms_pats):
    """Return all conditions fiels data for patinoires"""
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
    return arrose, date_heure, deblaye, ouvert, resurface


def get_glissades_fields(glissade):
    """Return all fields data for glissades"""
    nom = glissade.find("nom")
    nom.text = 'None' if nom.text is None else glissade.find(
        "nom").text.strip()
    nom_arr = glissade.find("arrondissement").find("nom_arr")
    nom_arr.text = 'None' if nom_arr.text is None else \
        glissade.find("arrondissement").find("nom_arr").text.strip()
    cle = glissade.find("arrondissement").find("cle")
    cle.text = 'None' if cle.text is None else glissade.find(
        "arrondissement").find("cle").text.strip()
    date_maj = glissade.find("arrondissement").find("date_maj")
    date_maj.text = 'None' if date_maj.text is None else \
        glissade.find("arrondissement").find("date_maj").text.strip()
    ouvert = glissade.find("ouvert")
    ouvert.text = 'None' if ouvert.text is None else \
        glissade.find("ouvert").text.strip()
    deblaye = glissade.find("deblaye")
    deblaye.text = 'None' if deblaye.text is None else \
        glissade.find("deblaye").text.strip()
    condition = glissade.find("condition")
    condition.text = 'None' if condition.text is None else \
        glissade.find("condition").text.strip()
    return cle, condition, date_maj, deblaye, nom, nom_arr, ouvert


def cursor_records_to_dictionnary(cursor):
    """Return cursor content as dictionnary"""
    records = cursor.fetchall()
    record_list = []
    column_names = [column[0] for column in cursor.description]
    for record in records:
        record_list.append(dict(zip(column_names, record)))
    return record_list


###############################################################################
# DATABASE OBJECT #
###############################################################################


class Database:
    """Definition of a Database object"""

    ###########################################################################
    # CONSTRUCTOR #
    ###########################################################################
    def __init__(self):
        self.connection = None

    ###########################################################################
    # FUNCTIONS #
    ###########################################################################

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
        rows = get_csv_data_from_url(URL_CSV_PISCINES)
        multiple_query_piscines(cursor, rows)
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
                    arrose, date_heure, deblaye, ouvert, resurface = \
                        get_conditions_fields(conditions, j, k, noms_pats)
                    cursor.execute(INSERT_PATINOIRES, (
                        nom_arr, nom_pat, date_heure, ouvert, deblaye, arrose,
                        resurface))
        # multiple_query_patinoires(cursor)
        connection.commit()
        connection.close()
        self.disconnect()

    def add_glissades_data_to_database(self):
        """add XML data from url to database"""
        connection = self.get_connection()
        cursor = connection.cursor()
        glissades = get_xml_data_from_url(URL_XML_GLISSADES)
        final = []
        for glissade in glissades:
            cle, condition, date_maj, deblaye, nom, nom_arr, ouvert = \
                get_glissades_fields(glissade)
            total = (nom.text.strip(), nom_arr.text.strip(), cle.text.strip(),
                     date_maj.text.strip(), ouvert.text.strip(),
                     deblaye.text.strip(), condition.text.strip())
            final.append(total)
        cursor.executemany(INSERT_GLISSADES, final)
        connection.commit()
        connection.close()
        self.disconnect()

    def create_piscines_installations_aquatiques_table(self):
        """create the piscines table in database object"""
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(DROP_PISCINES)
        cursor.execute(CREATE_PISCINES)
        connection.commit()
        connection.close()
        self.disconnect()

    def create_glissades_table(self):
        """create the glissades table in database object"""
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(DROP_GLISSADES)
        cursor.execute(CREATE_GLISSADES)
        connection.commit()
        connection.close()
        self.disconnect()

    def create_patinoires_table(self):
        """create patinoires table in database object"""
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(DROP_PATINOIRES)
        cursor.execute(CREATE_PATINOIRES)
        connection.commit()
        connection.close()
        self.disconnect()

    def get_piscines_installations_list_from_arrondissement(self,
                                                            arrondissement):
        """return a list of installations specific to an arrondissement"""
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("""SELECT DISTINCT nom FROM
        piscines_installations_aquatiques
        WHERE arrondissement LIKE ?;""", ('%' + arrondissement + '%',))
        record_list = cursor_records_to_dictionnary(cursor)
        connection.commit()
        connection.close()
        self.disconnect()
        return record_list

    def get_patinoires_installations_list_from_arrondissement(self,
                                                              arrondissement):
        """return a list of installations specific to an arrondissement"""
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("""SELECT DISTINCT nom_pat FROM patinoires WHERE nom_arr
        LIKE ?;""", ('%' + arrondissement + '%',))
        record_list = cursor_records_to_dictionnary(cursor)
        connection.commit()
        connection.close()
        self.disconnect()
        return record_list

    def get_glissades_installations_list_from_arrondissement(self,
                                                             arrondissement):
        """return a list of installations specific to an arrondissement"""
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("""SELECT DISTINCT nom FROM
           glissades WHERE nom_arr LIKE ?;""", ('%' + arrondissement + '%',))
        record_list = cursor_records_to_dictionnary(cursor)
        connection.commit()
        connection.close()
        self.disconnect()
        return record_list

    def get_piscines_installations_2021(self):
        """return a list of all iscines updated in 2021"""
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM
           piscines_installations_aquatiques ORDER BY nom ASC;""")
        record_list = cursor_records_to_dictionnary(cursor)
        connection.commit()
        connection.close()
        self.disconnect()
        return record_list

    def get_patinoires_installations_2021(self):
        """return a list of all patinoires updated in 2021"""
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM
           patinoires WHERE date_heure >= ? ORDER BY nom_pat
           ASC;""", ('2021-1-1',))
        record_list = cursor_records_to_dictionnary(cursor)
        connection.commit()
        connection.close()
        self.disconnect()
        return record_list

    def get_glissades_installations_2021(self):
        """return a list of all installations updated in 2021"""
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM
           glissades WHERE date_maj >= ? ORDER BY nom ASC;""", ('2021-1-1',))
        record_list = cursor_records_to_dictionnary(cursor)
        connection.commit()
        connection.close()
        self.disconnect()
        return record_list

    def get_all_piscines_names(self):
        """return a list of all piscines names"""
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("""SELECT DISTINCT nom FROM 
        piscines_installations_aquatiques;""")
        record_list = cursor_records_to_dictionnary(cursor)
        connection.commit()
        connection.close()
        self.disconnect()
        return record_list

    def get_all_patinoires_names(self):
        """return a list of all patinoires names"""
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("""SELECT DISTINCT nom_pat FROM 
        patinoires;""")
        record_list = cursor_records_to_dictionnary(cursor)
        connection.commit()
        connection.close()
        self.disconnect()
        return record_list

    def get_all_glissades_names(self):
        """return a list of all patinoires names"""
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("""SELECT DISTINCT nom FROM 
           glissades;""")
        record_list = cursor_records_to_dictionnary(cursor)
        connection.commit()
        connection.close()
        self.disconnect()
        return record_list
###############################################################################
# END OF FILE #
###############################################################################
