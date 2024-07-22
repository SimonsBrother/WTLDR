import re
from typing import Dict

from imap_tools import MailBox, AND

from wtldr.modules.constants import SummaryType
from wtldr.modules.emailing import Email
from wtldr.modules.storage import WTLDRDatabase, Summary


# TODO test
def save_emails_to_db(mailbox: MailBox, db: WTLDRDatabase) -> [int]:
    """ Save all emails in the email account to the database. May raise exceptions.
    :return: the number of emails saved.
    """
    # Archive emails so they are not re-fetched
    uids_of_saved_emails = []
    for email in mailbox.fetch(criteria=AND(from_="dan@tldrnewsletter.com")):
        # If UID is valid
        if email.uid is not None:
            # Save to database
            db.insert_email(Email(sender=email.from_, subject=email.subject, body=email.text, time_sent=email.date))
            uids_of_saved_emails.append(email.uid)

    # Move saved emails to archive
    mailbox.move(uids_of_saved_emails, "ARCHIVE")

    return uids_of_saved_emails


# TODO test
def extract_tldr_summaries(tldr_email: Email):
    links = parse_email_links(tldr_email.body)

    summary_objects = []
    # Split by double carriage return (CR)
    sections = tldr_email.body.split("\r\n\r\n")
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
            # Get info from regex groups
            summary_title, title_metadata, link_id = match.groups()
            link_id = int(link_id)

            # The summary will be the next section
            summary = sections[i + 1]
            full_summary = f"{summary_title} ({title_metadata})\n{clean(summary)}"

            summary_obj = Summary(source_email_id=tldr_email.email_id, summary=full_summary,
                                  url=links[link_id], summary_type=SummaryType.TLDR)
            summary_objects.append(summary_obj)

            skip_next = True

    return summary_objects


def parse_email_links(text: str) -> Dict[int, str]:
    """ Extracts the URLs and their IDs from the bottom of a TLDR email.

    :param text: the body of a TLDR email.
    :return: a dictionary correlating each ID to a URL.
    """
    links = {}

    # Find where the links start
    links_start_cue = "Links:\r\n------\r\n"
    links_start_index = text.find(links_start_cue) + len(links_start_cue)

    # Get the area of text for links, split it by newlines, where each line is a link with an ID
    for link_body in text[links_start_index:].splitlines():
        id_and_link = link_body.split(" ")  # Returns ['[x]', 'url'] where x is the ID

        # Splice ID of link, and get URL
        link_id = int(id_and_link[0][1:-1])  # the [1:-1] cuts off the square brackets
        link_url = id_and_link[1]
        # Add to links dict
        links[link_id] = link_url

    return links


def clean(text: str) -> str:
    """ Removes CRs (carriage returns), newlines, and strips whitespace off ends. """
    return text.replace("\r\n", " ").replace("\n", " ").strip()


# TODO generating custom summaries using LLM
