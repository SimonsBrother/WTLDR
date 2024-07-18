import sqlite3
from logging import Logger
from pathlib import Path

from wtldr.modules import emailing


# TODO: add more logging
class WTLDRDatabase:
    def __init__(self, db_path: Path | str, logger: Logger):
        """ Connects to the database. May raise exceptions.

        :param db_path: the path to the database file.
        """
        self.logger = logger

        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def __del__(self):
        # Attempt to close everything
        try:
            self.cursor.close()
        except Exception as e:
            self.logger.error(f"Could not close cursor: {e}")

        try:
            self.conn.close()
        except Exception as e:
            self.logger.error(f"Could not close database connection: {e}")

    def create_tables(self):
        """ Creates each table needed for the system to work. """
        self.logger.info("Creating tables...")
        self._create_emails_table()
        self._create_tldr_summaries_table()
        self.logger.info("Tables created.")

    def _create_emails_table(self):
        """ Creates a table for storing emails in current database connection."""
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
        """ Creates a table for storing TLDR summaries in current database connection. """
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
        """ Inserts a new email in the emails table. """
        values = (email.email_id, email.sender, email.subject, email.body, email.time_sent, False)
        self.cursor.execute("INSERT INTO emails VALUES (?, ?, ?, ?, ?, ?)", values)
        self.conn.commit()

    def get_emails(self, email_ids: list[int]) -> list[emailing.Email]:
        emails = []
        rows = self.cursor.execute("SELECT * FROM emails WHERE email_id IN (?);", email_ids).fetchall()
        for row in rows:
            email = emailing.Email(row[0], row[1], row[2], row[3], row[4])
            emails.append(email)

        return emails


def create_new_wtldr_db(db_path: Path | str, logger: Logger) -> WTLDRDatabase:
    """ Creates a database file with the path specified, and creates the tables needed for the database to function.

    :param db_path: path to the database file.
    :return: a WTLDRDatabase instance.
    """
    # Create the new file - exceptions should be handled outside the function
    file = open(db_path, "w")
    file.close()

    db = WTLDRDatabase(db_path, logger)

    # Create database contents
    db.create_tables()

    return db
