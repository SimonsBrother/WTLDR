import sqlite3
from pathlib import Path

from wtldr.modules import emailing


class WTLDRDatabase:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def create_tables(self):
        self._create_emails_table()
        self._create_tldr_summaries_table()

    def _create_emails_table(self):
        stmt = """
        CREATE TABLE emails (
            email_id INT NOT NULL,
            sender VARCHAR(50) NOT NULL,
            subject VARCHAR(200),
            body LONGTEXT NOT NULL,
            time_sent VARCHAR(30) NOT NULL,
            processed BOOL NOT NULL DEFAULT 0,
            PRIMARY KEY(email_id)
        );
        """
        self.cursor.execute("DROP TABLE IF EXISTS emails;")
        self.cursor.execute(stmt)
        self.conn.commit()

    def _create_tldr_summaries_table(self):
        stmt = """
        CREATE TABLE tldr_summaries (
            summary_id INT AUTO_INCREMENT,
            source_email_id INT NOT NULL,
            summary LONGTEXT NOT NULL,
            url TEXT NOT NULL,
            processed BOOL NOT NULL DEFAULT 0,
            PRIMARY KEY(summary_id),
            FOREIGN KEY (source_email_id) REFERENCES emails(email_id)
        );
        """
        self.cursor.execute("DROP TABLE IF EXISTS tldr_summaries;")
        self.cursor.execute(stmt)
        self.conn.commit()

    def insert_email(self, email: emailing.Email):
        values = (email.email_id, email.sender, email.subject, email.body, email.time_sent)
        self.cursor.execute("INSERT INTO emails VALUES (?, ?, ?, ?, ?)", values)
        self.conn.commit()


def create_new_wtldr_db(db_path: Path | str) -> WTLDRDatabase:
    """ Creates a database file with the path specified, and creates the tables needed for the database to function.

    :param db_path: path to the database file.
    :return: a WTLDRDatabase instance.
    """
    # Create the new file - exceptions should be handled outside the function
    file = open(db_path, "w")
    file.close()

    db = WTLDRDatabase(db_path)

    # Create database contents
    db.create_tables()

    return db
