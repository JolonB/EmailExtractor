import re
import os
import base64
import imaplib
import binascii
import utilities
from textfx import *
from credentials import *
from datetime import datetime
from email.parser import BytesParser as Parser

"""
Code heavily inspired by:
https://www.tutorialspoint.com/python_network_programming/python_imap.htm
"""

url_regex = re.compile(
    "((?:(https?|s?ftp):\/\/)?(?:www\.)?((?:(?:[A-Z0-9][A-Z0-9-]{0,61}[A-Z0-9]\.)+)([A-Z]{2,6})|(?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))(?::(\d{1,5}))?(?:(\/\S+)*))",
    re.IGNORECASE,
)
url_char_regex = re.compile("[A-Za-z0-9\-\._~:/\?#\[\]@!\$&'\(\)\*\+,;%=]*")
filename_regex = re.compile('name="?([A-Za-z0-9_\-,()\. &]*)"?')


def decode_save_image(msg_part):
    # get payload
    payload = msg_part.get_payload()
    # convert payload from b64 to normal
    payload = base64.b64decode(payload)
    # save as "name"
    try:
        matches = [filename_regex.search(content) for content in re.split("\;\s+", msg_part.get("Content-Type"))]
        filename = [m for m in matches if m][0][1]
    except IndexError:
        print("Could not find a filename in {}".format(msg_part.get("Content-Type")))
        return
    print("Saving: {}".format(filename))

    # write file
    with open(filename, "wb") as f:
        f.write(payload)


def replace(string, replacements):
    rep = dict((re.escape(k), v) for k, v in replacements.items())
    pattern = re.compile("|".join(replacements.keys()))
    return pattern.sub(lambda m: replacements[re.escape(m.group())], string)


def get_urls(string) -> list:
    return [url_char_regex.match(t[0])[0] for t in url_regex.findall(string)]

# connect with SSL
mail = imaplib.IMAP4_SSL(imap_host)

# log in
mail.login(imap_user, imap_pass)

mail.select("inbox")

date = datetime(2021, 3, 12)  # ? change the date here
datestr = datetime.strftime(date, "%d-%b-%Y")
result, data = mail.search(None, "(SINCE {})".format(datestr))

email_id = data[0].split()

if not email_id:
    print_error("No mail found")
    exit(1)
else:
    print_info("You've got mail!")

parser = Parser()

# create image dir
utilities.mkchdir("out")

for d in email_id:
    result, data = mail.fetch(d, "(RFC822)")
    parsedbytes = parser.parsebytes(data[0][1])

    # create directory using date and user email
    from_ = parsedbytes.get("From")
    utilities.mkchdir(replace(from_, {"\\<": "", "\\>": "", '\\"': ""}))

    # save images and extract urls
    for part in parsedbytes.walk():
        content_type = part.get("Content-Type")
        # save image
        if content_type.startswith("image"):
            decode_save_image(part)
        # save links
        elif content_type.startswith("text/plain"):
            # convert to regular text if encoded
            if part.get("Content-Transfer-Encoding") == "base64":
                part = base64.b64decode(str(part.get_payload()))
            # get URLs
            urls = get_urls(str(part))
            if urls:
                with open("urls.txt", "a") as url_file:
                    for url in urls:
                        url_file.write("{}\n".format(url))
        # keep a record of any other content in the email
        elif not content_type.startswith(("multipart/", "text/html")):
            with open("other.txt", "a") as other_file:
                other_file.write("\n{}".format(content_type))

    os.chdir("../")

    # print(part.get_content_type())
    # f = open('output.txt','w')
    # f.write(str(parsedbytes))
    # f.close()
    # break
    # msg = parse_msg(parsedbytes)
    # print(type(msg["header"]))
    # for part in msg["header"].walk():
    #     print(type(part))
    # print(msg["body"])
    # break

mail.close()
