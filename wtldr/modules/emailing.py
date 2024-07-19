""" Contains functionality and classes related to getting emails from an email account.
Highlights:
The Email dataclass, for representing key information about emails. This dataclass also has static methods
    for decoding information from email messages.
The EmailManager class, for handling interactions with an email account.
"""

import email
import imaplib
import ssl
from datetime import datetime
from email.header import decode_header
from email.message import Message
from logging import Logger

from pydantic import BaseModel, validate_call

# For converting timestamp of emails into a number, for converting the timestamp to datetime object.
month_name_to_number = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12
}


class Email(BaseModel):
    """ Dataclass for storing details about emails """
    email_id: int
    sender: str
    subject: str
    body: str
    time_sent: datetime
    processed: bool

    def __repr__(self):
        return (f"Email(email_id={self.email_id}, sender='{self.sender}', subject='{self.subject}', "
                f"time_sent='{self.time_sent}', processed='{self.processed}')")

    # Much of the code below was derived from
    # https://thepythoncode.com/article/reading-emails-in-python?utm_content=cmp-true
    @staticmethod
    def try_decode(data: bytes, encoding: str) -> str:
        """ Attempts to call decode on the item provided, and decode it according to the encoding provided.

        :param data: the data to decode.
        :param encoding: the encoding to decode with.
        :return: the encoded data if decoding was successful; if there was a problem, the provided data is returned.
        """
        try:
            # The encoding is sometimes None when it should be a string
            if isinstance(data, bytes) and isinstance(encoding, str):
                # if it's a bytes, decode to str
                data = data.decode(encoding)
        except:
            data = str(data)

        return data

    @staticmethod
    def get_subject(msg: Message) -> str:
        """ Gets the subject of an email Message """
        # decode the email subject
        subject, encoding = decode_header(msg["Subject"])[0]

        subject = Email.try_decode(subject, encoding)

        return subject

    @staticmethod
    def get_sender(msg: Message) -> str:
        """ Gets the sender name and email address of an email Message """
        # decode email sender
        sender, encoding = decode_header(msg["From"])[0]
        sender = Email.try_decode(sender, encoding)

        return sender

    @staticmethod
    def get_body(msg: Message) -> str:
        """ Gets the body of an email Message """

        body = ""
        # If the message is multipart, go through all the parts until something can be decoded.
        if msg.is_multipart():
            for part in msg.walk():
                try:
                    body = part.get_payload(decode=True).decode()
                    break
                except:
                    pass
        else:
            body = msg.get_payload(decode=True).decode()

        return body

    @staticmethod
    def get_sent_datetime(msg: Message) -> datetime:
        """ Gets the date and time an email Message was sent """
        # Date is in this format: Mon, 13 May 2024 13:33:47 +0000
        raw_date = str(msg["Date"])
        split_raw_date = raw_date.split(" ")[1:-1]  # ['13', 'May', '2024', '13:33:47']

        split_date = split_raw_date[:-1]  # Ignore time to just get date
        split_time = split_raw_date[-1].split(":")  # Split time

        sent_datetime = datetime(day=int(split_date[0]), month=month_name_to_number[split_date[1]],
                                 year=int(split_date[2]),
                                 hour=int(split_time[0]), minute=int(split_time[1]), second=int(split_time[2]))

        return sent_datetime

    @staticmethod
    def get_email_details(msg: Message, email_id: int):
        """ Gets the sender, subject, content type, body, and datetime sent. Requires the email ID as a parameter,
        because any time this function is used, the ID will probably already have been retrieved. """
        return Email(email_id=email_id,
                     sender=Email.get_sender(msg),
                     subject=Email.get_subject(msg),
                     body=Email.get_body(msg),
                     time_sent=Email.get_sent_datetime(msg),
                     processed=False)


class EmailManager:
    """ Handles accessing the email account. Most methods of this class do not handle exceptions. """

    def __init__(self, username: str, password: str, imap_server: str, logger: Logger):
        """ Creates an IMAP4_SSL object and logs into the email account. Exceptions may be raised. """
        self.logger = logger

        self.imap = imaplib.IMAP4_SSL(imap_server)

        # TLS may not be supported
        try:
            self.imap.starttls(ssl_context=ssl.create_default_context())
        except imaplib.IMAP4.abort:
            logger.warning("TLS not supported by server.")

        self.imap.login(username, password)

    @validate_call
    def get_email_from_mailbox(self, email_id: int, mailbox: str = "INBOX") -> Email:
        """ Opens the mailbox given (INBOX by default), creates an Email object from an email ID, and closes the mailbox.
        May raise exceptions.
        Use this for retrieving some emails - if you need to retrieve many emails, use get_email.

        :param email_id: the email ID to open.
        :param mailbox: the mailbox to open and retrieve the email from.
        :return: an Email object or None if there was a problem getting the email..
        """
        self.imap.select(mailbox)

        email_obj = self.get_email(email_id)

        self.close_mailbox()
        return email_obj

    @validate_call
    def get_email(self, email_id: int) -> Email:
        """ Creates an Email object from an email ID.
        NOTE: A mailbox should be opened before this is called.
        Use this for retrieving many emails from the same mailbox - otherwise stick to get_email_from_mailbox.
        May raise exceptions.

        :param email_id: the email ID to open.
        :return: None on failure, otherwise an Email object.
        """
        res, msg = self.imap.fetch(str(email_id), "(RFC822)")  # I don't really know what this means
        email_obj = None

        for response in msg:
            if isinstance(response, tuple):
                # Parse a bytes email into a Message object
                msg = email.message_from_bytes(response[1])

                # Parse details about Message object into Email object
                email_obj = Email.get_email_details(msg, email_id)

        return email_obj

    @validate_call
    def open_mailbox(self, mailbox_: str = "INBOX") -> None:
        """ Opens a mailbox. """
        self.imap.select(mailbox_)
        self.logger.info(f"Opened mailbox {mailbox_}.")

    def close_mailbox(self):
        """ Try to close any open mailbox. Logs the exception on failure. """
        try:
            self.imap.close()
            self.logger.info("Closed mailbox.")
        except Exception as e:
            self.logger.error(f"Failed to close mailbox: {e}")

    def __del__(self):
        """ Try to log out. Often displays an error if not deleted before the program ends; if this occurs, delete this instance at the end of the program. """
        try:
            self.imap.logout()
        except Exception as e:
            self.logger.error(f"Logout failed: {e}")

    def get_tldr_email_ids(self) -> list[int]:
        """ Gets all the email IDs that were sent from TLDR. """
        self.imap.select("INBOX")

        # Get all IDs of emails from TLDR - imap.search returns a tuple containing a status and then the IDs
        email_ids_bytes_list = self.imap.search(None, '(FROM "dan@tldrnewsletter.com")')[1]
        # Email bytes list is of the form: [b'2 4 5 6 7'] - remove this from the list, and specify they are bytes to
        # help PyCharm.
        email_ids_bytes = bytes(email_ids_bytes_list[0])
        # Split the bytes by spaces, and use list comprehension to convert to list of integers.
        email_ids = [int(email_id) for email_id in email_ids_bytes.split(b" ")]

        self.close_mailbox()
        return email_ids
