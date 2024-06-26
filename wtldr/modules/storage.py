import sqlite3

from wtldr.modules import emailing


# TODO: Create tests
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
        self.cursor.execute("INSERT INTO emails VALUES (?, ?, ?, ?, ?)")
        self.conn.commit()


def create_new(db_path: str) -> WTLDRDatabase:
    # Create the new file
    try:
        file = open(db_path, "w")
        file.close()
    except FileNotFoundError:  # TODO use logging
        print("Error: The specified file path does not exist.")
    except IsADirectoryError:
        print("Error: The specified path is a directory, not a file.")
    except PermissionError:
        print("Error: You do not have permission to write to this file.")
    except OSError as e:
        print(f"OS error occurred: {e}")
    except ValueError as e:
        print(f"Invalid mode specified: {e}")

    db = WTLDRDatabase(db_path)

    # Create database contents
    try:
        db.create_tables()
    except:  # TODO add specific exceptions
        raise

    return db
