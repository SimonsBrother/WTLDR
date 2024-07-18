import sqlite3
from logging import Logger
from pathlib import Path

from pydantic import validate_call

from wtldr.modules import emailing


class WTLDRDatabase:
    def __init__(self, db_path: Path | str, logger: Logger):
        """ Connects to the database. May raise exceptions.

        :param db_path: the path to the database file.
        """
        self.logger = logger

        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.logger.info("Connected to database.")

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
        self._create_summaries_table()
        self._create_custom_summaries_table()
        self._create_summaries_used_table()
        self.logger.info("Tables created.")

    def _create_table(self, table_name: str, create_table_stmt: str):
        """ Drops the table if it already exists, creates it, and commits. """
        self.logger.info(f"Dropping {table_name} if possible...")
        self.cursor.execute(f"DROP TABLE IF EXISTS {table_name};")

        self.logger.info(f"Creating {table_name}...")
        self.cursor.execute(create_table_stmt)

        self.logger.info(f"Committing...")
        self.conn.commit()
        self.logger.info(f"Table {table_name} created and committed.")

    def _create_emails_table(self):
        """ Creates a table for storing emails in current database connection."""
        table_name = "emails"
        stmt = f"""
        CREATE TABLE {table_name} (
            email_id INTEGER NOT NULL,
            sender TEXT NOT NULL,
            subject TEXT NOT NULL,
            body LONGTEXT NOT NULL,
            time_sent DATETIME NOT NULL,
            processed BOOL NOT NULL DEFAULT 0,
            PRIMARY KEY(email_id)
        );
        """
        self._create_table(table_name, stmt)

    def _create_summaries_table(self):
        """ Creates a table for storing TLDR summaries in current database connection. """
        table_name = "summaries"
        stmt = f"""
        CREATE TABLE {table_name} (
            summary_id INTEGER AUTO_INCREMENT,
            source_email_id INTEGER NOT NULL,
            summary LONGTEXT NOT NULL,
            url TEXT NOT NULL,
            processed BOOL NOT NULL DEFAULT 0,
            PRIMARY KEY(summary_id),
            FOREIGN KEY (source_email_id) REFERENCES emails(email_id)
        );
        """
        self._create_table(table_name, stmt)

    def _create_custom_summaries_table(self):
        """ Creates a table for storing custom summaries. """
        table_name = "custom_summaries"
        stmt = f"""
        CREATE TABLE {table_name} (
            custom_sum_id INTEGER AUTO_INCREMENT,
            summary LONGTEXT NOT NULL,
            prompt TEXT NOT NULL,
            PRIMARY KEY(custom_sum_id)
        );
        """
        self._create_table(table_name, stmt)

    def _create_summaries_used_table(self):
        """ Creates a table for storing which summaries are used in custom summaries. """
        table_name = "summaries_used"
        stmt = f"""
        CREATE TABLE {table_name} (
            custom_sum_id INTEGER,
            summary_id INTEGER,
            PRIMARY KEY (custom_sum_id, summary_id),
            FOREIGN KEY (custom_sum_id) REFERENCES custom_summaries(custom_sum_id),
            FOREIGN KEY (summary_id) REFERENCES summaries(summary_id)
        );
        """
        self._create_table(table_name, stmt)

    @validate_call
    def insert_email(self, email: emailing.Email):
        """ Inserts a new email in the emails table. """
        values = (email.email_id, email.sender, email.subject, email.body, email.time_sent, False)
        self.cursor.execute("INSERT INTO emails VALUES (?, ?, ?, ?, ?, ?)", values)
        self.conn.commit()

    @validate_call
    def get_emails(self, email_ids: list[int]) -> list[emailing.Email]:
        emails = []
        rows = self.cursor.execute("SELECT * FROM emails WHERE email_id IN (?);", email_ids).fetchall()
        for row in rows:
            email = emailing.Email(email_id=row[0], sender=row[1], subject=row[2], body=row[3], time_sent=row[4])
            emails.append(email)

        return emails


def create_new_wtldr_db(db_path: Path | str, logger: Logger) -> WTLDRDatabase:
    """ Creates a database file with the path specified, and creates the tables needed for the database to function.

    :param db_path: path to the database file.
    :param logger: a Logger instance.
    :return: a WTLDRDatabase instance.
    """
    # Create the new file - exceptions should be handled outside the function
    file = open(db_path, "w")
    file.close()

    db = WTLDRDatabase(db_path, logger)

    # Create database contents
    db.create_tables()

    return db
