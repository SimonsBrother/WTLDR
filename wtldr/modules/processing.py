from wtldr.modules.emailing import Email, EmailManager
from wtldr.modules.storage import WTLDRDatabase


def save_emails_to_db(email_manager: EmailManager, wtldr_db: WTLDRDatabase) -> int:
    """ Save all emails in the email account to the database. May raise exceptions.
    :return: the number of emails saved.
    """
    # TODO archive emails after getting them
    ids = email_manager.get_tldr_email_ids()

    count = 0  # Count how many emails are added.
    email_manager.open_mailbox("INBOX")
    try:
        for id_ in ids:
            # Get email from account
            email = email_manager.get_email(id_)
            # Attempt to insert email
            if wtldr_db.insert_email(email):
                count += 1
    except Exception as e:
        raise e
    finally:
        # Make sure mailbox is closed
        email_manager.close_mailbox()

    return count


def extract_tldr_summaries(tldr_email: Email):
    # Get all unprocessed TLDR emails
    ...  # TODO


# TODO generating custom summaries using LLM
