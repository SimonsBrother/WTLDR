import re

from wtldr.modules.constants import SummaryType
from wtldr.modules.emailing import Email, EmailManager
from wtldr.modules.storage import WTLDRDatabase, Summary


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


# TODO break into smaller functions
def extract_tldr_summaries(tldr_email: Email):
    body = tldr_email.body

    # Get links
    links = {}
    links_start_cue = "Links:\r\n------\r\n"
    links_start_index = body.find(links_start_cue) + len(links_start_cue)
    # Get the area of text for links, split it by line
    for link_body in body[links_start_index:].splitlines():
        id_to_link = link_body.split(" ")  # Returns ['[x]', 'url']

        # Splice ID of link, and get URL
        link_id = int(id_to_link[0][1:-1])
        link_url = id_to_link[1]
        # Add to links dict
        links[link_id] = link_url

    summary_objects = []
    # Split by double carriage return (CR)
    sections = body.split("\r\n\r\n")
    # If a summary title is detected by regex, the next section will be a paragraph, and can be skipped, which is probably more optimal
    skip_next = False
    for i in range(len(sections)):
        if skip_next:
            skip_next = False
            continue

        section = sections[i]

        # Newlines and CRs make the regex matching miss some titles, so it is formatted remove them
        section = clean(section)

        # Summary titles will have the form: TITLE (METADATA) [LINK]
        # ...which roughly translates to *characters* *whitespace* (*characters*) *whitespace* [number]
        match = re.match(r"(?s)(.+)\s\((.+)\)\s\[(\d+)]", section)

        # If title detected
        if match:
            summary_title, title_metadata, link_id = match.groups()
            link_id = int(link_id)

            summary = sections[i + 1]
            full_summary = f"{summary_title} ({title_metadata})\n{clean(summary)}"

            summary_obj = Summary(source_email_id=tldr_email.email_id, summary=full_summary,
                                  url=links[link_id], summary_type=SummaryType.TLDR)
            summary_objects.append(summary_obj)

            skip_next = True

    return summary_objects


def clean(text: str) -> str:
    """ Removes CRs (carriage returns), newlines, and strips whitespace off ends. """
    return text.replace("\r\n", " ").replace("\n", " ").strip()


# TODO generating custom summaries using LLM
