from dotenv import dotenv_values

from imap_tools import MailBox, AND

from wtldr.modules import emailing, processing
from wtldr.modules.logging_ import create_logger
from wtldr.modules.storage import WTLDRDatabase


# TODO make a database and email specially for testing (need to wait for tldr emails to come through)
def test_save_tldr_emails_to_db(mailbox: MailBox, wtldr_db: WTLDRDatabase):
    print(processing.save_emails_to_db(mailbox, wtldr_db))


# TODO make proper tests
def test_extract_tldr_summaries(wtldr_db: WTLDRDatabase):
    print(processing.extract_tldr_summaries(wtldr_db.get_emails([3])[0]))


if __name__ == "__main__":
    secrets = dotenv_values()

    username = secrets["TEST_EMAIL"]
    password = secrets["TEST_PW"]
    host = "imap-mail.outlook.com"  # https://www.systoolsgroup.com/imap/ for other servers

    logger = create_logger("logs")
    db = WTLDRDatabase("test.db", logger)

    with MailBox(host).login(username, password) as mb:
        test_save_tldr_emails_to_db(mb, db)
        #test_extract_tldr_summaries(db)
