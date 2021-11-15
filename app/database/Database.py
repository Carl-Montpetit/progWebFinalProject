import sqlite3


class Database:
    def __init__(self):
        self.connection = None

    # Return cursor as a dict

    def to_dict(self, dict_name, cursor):
        return [dict(dict_name) for dict_name in cursor.fetchall()]

    def get_connection(self):
        """Open database connection. Should be closed after use"""
        if self.connection is None:
            self.connection = sqlite3.\
                connect("app/database/database.db")
            self.connection.row_factory = sqlite3.Row
        return self.connection

    def disconnect(self):
        """Closes the database connection"""
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def get_five_last_articles(self, today_date):
        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM article WHERE date_publication <= \
                ? ORDER BY date_publication DESC LIMIT 5", (today_date,)
        )
        return self.to_dict("article", cursor)

    def get_all_articles(self):
        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM article ORDER BY date_publication DESC")
        return self.to_dict("article", cursor)

    def insert_article(self, article):
        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO article (titre, identifiant, auteur,\
                date_publication, paragraphe) VALUES (?, ?, ?, ?, ?)",
            [article[0], article[1], article[2], article[3], article[4]],
        )
        connection.commit()
        return 1

    def modify_article(self, titre, identifiant, paragraphe):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE article SET titre = ?, \
                paragraphe = ? WHERE identifiant = ?",
            (titre, paragraphe, identifiant)
        )
        connection.commit()
        return 1

    def get_article_by_identifiant(self, identifiant):
        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM article WHERE identifiant = ?", (identifiant,))
        return self.to_dict("article", cursor)

    def get_search_articles(self, search):
        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM article WHERE titre LIKE ? OR\
            paragraphe LIKE ? ORDER BY date_publication DESC",
                       ('%'+search+'%', '%'+search+'%'))
        return self.to_dict("article", cursor)
