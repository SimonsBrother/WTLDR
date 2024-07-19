from datetime import datetime

from wtldr.modules import emailing, constants
from wtldr.modules.logging_ import create_logger
from wtldr.modules.storage import WTLDRDatabase, create_new_wtldr_db, Summary


def test_database_creation():
    wtldr_db = create_new_wtldr_db("test.db",
                                   create_logger("logs"))
    return wtldr_db


def test_email_interactions(wtldr_db: WTLDRDatabase):
    email = emailing.Email(email_id=1, sender='Caleb Hair <calebthair@outlook.com>', subject='Lab rat test subject',
                           body="Lab rat lab rat lab rat", time_sent=datetime.fromisoformat('2024-05-13 13:33:47'), processed=False)

    assert wtldr_db.insert_email(email)  # Test adding an email functions correctly
    added_email = wtldr_db.get_emails([1])[0]  # Test emails can be retrieved
    assert added_email == email  # Test retrieved email matches.


def test_summary_interactions(wtldr_db: WTLDRDatabase):
    # Create summaries
    summaries = [
        Summary(summary="1", summary_type=constants.SummaryType.TLDR, processed=True,
                source_email_id=1, url="example1.com"),
        Summary(summary="2", summary_type=constants.SummaryType.TLDR, processed=True,
                source_email_id=1, url="example2.com"),
        Summary(summary="3", summary_type=constants.SummaryType.TLDR, processed=False,
                source_email_id=1, url="example3.com"),
        Summary(summary="4", summary_type=constants.SummaryType.TLDR, processed=False,
                source_email_id=1, url="example4.com"),
    ]

    # Test adding them to database
    for summary in summaries:
        wtldr_db.add_summary(summary)

    # Test retrieving unprocessed summaries
    for summary in wtldr_db.get_all_unprocessed_summaries(constants.SummaryType.TLDR):
        # Make sure that only unprocessed summaries are returned, and that they are as expected.
        assert summary.processed is False and summary.summary in ("3", "4")


if __name__ == "__main__":
    db = test_database_creation()
    test_email_interactions(db)
    test_summary_interactions(db)
