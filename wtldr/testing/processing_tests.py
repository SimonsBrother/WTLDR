from dotenv import dotenv_values

from wtldr.modules import emailing, processing
from wtldr.modules.logging_ import create_logger
from wtldr.modules.storage import WTLDRDatabase


def test_save_tldr_emails_to_db(email_manager: emailing.EmailManager, wtldr_db: WTLDRDatabase):
    print(processing.save_emails_to_db(email_manager, wtldr_db))


if __name__ == "__main__":
    secrets = dotenv_values()

    username = secrets["EMAIL"]
    password = secrets["PASSWORD"]

    logger = create_logger("logs")
    db = WTLDRDatabase("test.db", logger)
    email_manager = emailing.EmailManager(username, password, "imap-mail.outlook.com", logger)

    test_save_tldr_emails_to_db(email_manager, db)
