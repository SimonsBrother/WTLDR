""" Contains functionality and classes related to getting emails from an email account.
Highlights:
The Email dataclass, for representing key information about emails.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class Email(BaseModel):
    """ Dataclass for storing details about emails.
    :var email_id: int, the ID of the email in the database.
    :var sender: str, the email address of who sent it.
    :var subject: str, the email subject.
    :var body: str, the email body.
    :var time_sent: datetime, the time the email was sent.
    :var processed: bool, flag indicating whether the email was processed.
    """
    email_id: int
    sender: str
    subject: str
    body: str
    time_sent: datetime
    processed: bool = Field(default=False)

    def __repr__(self):
        return (f"Email(email_id={self.email_id}, sender='{self.sender}', subject='{self.subject}', "
                f"time_sent='{self.time_sent}', processed='{self.processed}')")
