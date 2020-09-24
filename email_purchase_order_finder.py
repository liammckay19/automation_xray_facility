import glob
import imaplib
import string

import html2text as html2text

import get_credentials_util
import pprint
import email
from imap_tools import MailBox, Q, AND, OR
import datetime as dt
from tqdm import tqdm


def search_email(search_string):
    email_logins = [ "credentials_ucsc_email.json"]
    emails_found = ''
    for login in email_logins:
        username, password = get_credentials_util.get_credentials(login)
        emails_found += "; ".join(list(search_email_inbox(search_string, username, password))).replace(
            string.whitespace, "")
    return emails_found


def search_email_inbox(search_string, username, password):
    # get list of email subjects from INBOX folder
    with MailBox('imap.gmail.com').login(username, password) as mailbox:
        for message in mailbox.fetch(
                Q(
                    AND(subject=search_string,
                        date_gte=dt.date(2020, 8, 1)
                        )
                ), miss_defect=False, miss_no_uid=False):
            yield message.subject

    # mail = imaplib.IMAP4_SSL('imap.gmail.com')
    # mail.login(username, password)
    # mail.list()
    # # Out: list of "folders" aka labels in gmail.
    # mail.select("inbox") # connect to inbox.
    #
    # result, data = mail.search(None, search_string )
    #
    # ids = data[0] # data is a list.
    # id_list = ids.split() # ids is a space separated string
    # for id in id_list:
    #     result, data = mail.fetch(id, "(RFC822)") # fetch the email body (RFC822)             for the given ID
    #
    #     raw_email = str(data[0][1]) # here's the body, which is raw text of the whole email
    #     # including headers and alternate payloads
    #     msg = email.message_from_string(raw_email)
    #     for part in msg.walk():
    #         if part.get_content_type() == 'text/plain':
    #             txt = part.get_payload()
    #
    #         elif part.get_content_type() == "text/html":
    #             html = part.get_payload()
    #             try:
    #                 html2txt = html2text.html2text(part.get_payload())
    #             except NotImplementedError as e:
    #                 continue        # print (msg.get_payload(decode=True))
    #     print(txt)
    #     yield result
