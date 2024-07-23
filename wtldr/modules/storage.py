import sqlite3
from logging import Logger
from pathlib import Path

from pydantic import validate_call, BaseModel, Field

from wtldr.modules import emailing, constants


class Summary(BaseModel):
    """ Represents a summary, of an online article, in the database.
    :var summary_id (None by default): int | None, the ID of the summary in the database.
    :var source_email_id: int, the ID of the email containing this summary in the database.
    :var summary: str, the summary content.
    :var url: str, the URL to the article being summarised.
    :var summary_type: SummaryType, the type of the summary.
    :var processed: bool (False by default), True if the summary was processed for some purpose.
    """
    summary_id: int | None = Field(default=None)
    source_email_id: int
    summary: str
    url: str
    summary_type: constants.SummaryType
    processed: bool = Field(default=False)


class WTLDRDatabase:
    """ Stores a connection to the database and any related attributes and methods that make it easier to interact
    with the database.

    :var conn: Connection to the database
    :var cursor: a cursor created from the database connection.
    :var logger: the logger instance used for logging, passed in on instantiation.
    """
    def __init__(self, db_path: Path | str, logger: Logger):
        """ Connects to the database.

        :raises sqlite3.OperationalError: issues may arise when trying to connect to the database (if it does not exist).
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
        """ Creates each table needed for the system to work.
        :raises sqlite3.ProgrammingError: Raised for programming errors, such as using a closed database connection.
        :raises sqlite3.DataError: Raised for errors related to the processing of data, such as data type mismatches or values out of range.
        """
        self.logger.info("Creating tables...")
        self._create_emails_table()
        self._create_summaries_table()
        self._create_super_summaries_table()
        self._create_summaries_used_table()
        self.logger.info("Tables created.")

    def _create_table(self, table_name: str, create_table_stmt: str):
        """ Drops the table if it already exists, creates it, and commits.

        :raises sqlite3.ProgrammingError: Raised for programming errors, such as using a closed database connection.
        :raises sqlite3.DataError: Raised for errors related to the processing of data, such as data type mismatches or values out of range.

        :param table_name: the name of the table to create. Risk of SQL injection if data from user is passed.
        :param create_table_stmt: the SQL statement to create the table.
        """
        self.logger.info(f"Dropping {table_name} if possible...")
        self.cursor.execute(f"DROP TABLE IF EXISTS {table_name};")

        self.logger.info(f"Creating {table_name}...")
        self.cursor.execute(create_table_stmt)

        self.logger.info(f"Committing...")
        self.conn.commit()
        self.logger.info(f"Table {table_name} created and committed.")

    def _create_emails_table(self):
        """ Creates a table for storing emails in current database connection.
        :raises sqlite3.ProgrammingError: Raised for programming errors, such as using a closed database connection.
        :raises sqlite3.DataError: Raised for errors related to the processing of data, such as data type mismatches or values out of range.
        """
        table_name = "emails"
        stmt = f"""
        CREATE TABLE {table_name} (
            email_id INTEGER AUTO_INCREMENT,
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
        """ Creates a table for storing TLDR summaries in current database connection.
        :raises sqlite3.ProgrammingError: Raised for programming errors, such as using a closed database connection.
        :raises sqlite3.DataError: Raised for errors related to the processing of data, such as data type mismatches or values out of range.
        """
        table_name = "summaries"
        stmt = f"""
        CREATE TABLE {table_name} (
            summary_id INTEGER AUTO_INCREMENT,
            source_email_id INTEGER NOT NULL,
            summary LONGTEXT NOT NULL,
            url TEXT NOT NULL,
            summary_type TEXT NOT NULL,
            processed BOOL NOT NULL DEFAULT 0,
            PRIMARY KEY(summary_id),
            FOREIGN KEY (source_email_id) REFERENCES emails(email_id)
        );
        """
        self._create_table(table_name, stmt)

    def _create_super_summaries_table(self):
        """ Creates a table for storing super summaries.
        :raises sqlite3.ProgrammingError: Raised for programming errors, such as using a closed database connection.
        :raises sqlite3.DataError: Raised for errors related to the processing of data, such as data type mismatches or values out of range.
        """
        table_name = "super_summaries"
        stmt = f"""
        CREATE TABLE {table_name} (
            super_sum_id INTEGER AUTO_INCREMENT,
            summary LONGTEXT NOT NULL,
            prompt TEXT NOT NULL,
            PRIMARY KEY(super_sum_id)
        );
        """
        self._create_table(table_name, stmt)

    def _create_summaries_used_table(self):
        """ Creates a table for storing which summaries are used in super summaries.
        :raises sqlite3.ProgrammingError: Raised for programming errors, such as using a closed database connection.
        :raises sqlite3.DataError: Raised for errors related to the processing of data, such as data type mismatches or values out of range.
        """
        table_name = "summaries_used"
        stmt = f"""
        CREATE TABLE {table_name} (
            super_sum_id INTEGER,
            summary_id INTEGER,
            PRIMARY KEY (super_sum_id, summary_id),
            FOREIGN KEY (super_sum_id) REFERENCES custom_summaries(super_sum_id),
            FOREIGN KEY (summary_id) REFERENCES summaries(summary_id)
        );
        """
        self._create_table(table_name, stmt)

    @validate_call
    def insert_email(self, email: emailing.Email):
        """ Inserts a new email in the emails table. Does nothing if an email with the same ID already exists.
        :raises sqlite3.IntegrityError: Raised when the relational integrity of the database is affected, such as a foreign key check failure.
        """
        values = (email.sender, email.subject, email.body, email.time_sent, email.processed)
        self.cursor.execute("INSERT INTO emails(sender, subject, body, time_sent, processed) VALUES (?, ?, ?, ?, ?)", values)
        self.conn.commit()

    @validate_call
    def add_summary(self, summary: Summary):
        """ Adds a new summary to the database. Note that the ID of the summary object passed is ignored.
        :raises sqlite3.IntegrityError: Raised when the relational integrity of the database is affected, such as a foreign key check failure.
        """
        values = summary.source_email_id, summary.summary, summary.url, summary.summary_type.value, summary.processed
        self.cursor.execute("INSERT INTO summaries (source_email_id, summary, url, summary_type, processed) VALUES(?, ?, ?, ?, ?)", values)
        self.conn.commit()

    @validate_call
    def get_all_unprocessed_summaries(self, summary_type: constants.SummaryType) -> list[Summary]:
        """ Gets all the summaries of a certain type that have not yet been processed. """
        summaries = []
        rows = self.cursor.execute("SELECT * FROM summaries WHERE summary_type == ? AND NOT processed;",
                                   (summary_type.value,))
        for row in rows:
            summary = Summary(summary_id=row[0],
                              source_email_id=row[1],
                              summary=row[2],
                              url=row[3],
                              summary_type=row[4],
                              processed=row[5])
            summaries.append(summary)

        return summaries


def create_new_wtldr_db(db_path: Path | str, logger: Logger) -> WTLDRDatabase:
    """ Creates a database file with the path specified, and creates the tables needed for the database to function.

    :raises IsADirectoryError: the database file should be a file, not a directory
    :raises PermissionError: program must have permission to read from, write to, and create the database file.
    :raises OSError: general exception that should be handled.

    :param db_path: path to the database file.
    :param logger: a Logger instance.
    :return: a WTLDRDatabase instance.
    """
    # Create the new file - exceptions should be handled outside the function
    with open(db_path, "w"):
        pass

    db = WTLDRDatabase(db_path, logger)

    # Create database contents
    db.create_tables()

    return db
