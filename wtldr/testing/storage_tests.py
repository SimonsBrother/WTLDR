from datetime import datetime

from wtldr.modules import emailing
from wtldr.modules.logging_ import create_logger
from wtldr.modules.storage import WTLDRDatabase, create_new_wtldr_db


def test_database_creation():
    wtldr_db = create_new_wtldr_db("test.db",
                                   create_logger("/Users/calebhair/Documents/Projects/WTLDR/wtldr/testing/logs"))
    return wtldr_db


def test_adding_email(wtldr_db: WTLDRDatabase):
    email = emailing.Email(email_id=1, sender='Caleb Hair <calebthair@outlook.com>', subject='Lab rat test subject',
                           body="Lab rat lab rat lab rat", time_sent=datetime.fromisoformat('2024-05-13 13:33:47'))

    wtldr_db.insert_email(email)
    added_email = wtldr_db.get_emails([1])[0]
    assert added_email == email


if __name__ == "__main__":
    db = test_database_creation()
    test_adding_email(db)
