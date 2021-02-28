import re
import os
import base64
import imaplib
import binascii
import pprint
from textfx import *
from credentials import *
from email.parser import BytesParser as Parser

"""
Code heavily inspired by:
https://www.tutorialspoint.com/python_network_programming/python_imap.htm
"""

regex = re.compile("((?:(https?|s?ftp):\/\/)?(?:www\.)?((?:(?:[A-Z0-9][A-Z0-9-]{0,61}[A-Z0-9]\.)+)([A-Z]{2,6})|(?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))(?::(\d{1,5}))?(?:(\/\S+)*))", re.IGNORECASE)

def parse_msg(parsedbytes) -> dict:
    msg_full = (
        parsedbytes.get_payload()[0].get_payload()
        if parsedbytes.is_multipart()
        else parsedbytes.get_payload()
    )
    print("1")
    print(msg_full)
    print("2")
    # msg_full = msg_full.split("\r\n", 1)
    return {
        "from": parsedbytes.get("From"),
        "to": parsedbytes.get("To"),
        "subject": parsedbytes.get("Subject"),
        "header": msg_full[0],
        "body": msg_full[1],
    }

def decode_image():
    pass

def save_img(a,b):
    pass

def check_base(bytestr)->int:
    # convert to bytes
    if isinstance(bytestr, str):
        bytestr = bytestr.encode()
    if not isinstance(bytestr, bytes):
        raise ValueError("Trying to check base of a non-string or -bytes object")
    #
    # remove \n
    bytestr = bytestr.replace(b'\n', b'')
    print(bytestr)
    #
    try:
        if base64.b64encode(base64.b64decode(bytestr)) == bytestr:
            return 64
        elif base64.b32encode(base64.b32decode(bytestr)) == bytestr:
            return 32
        else:
            return 0
    except binascii.Error:
        return 0

def replace(string, replacements):
    rep = dict((re.escape(k), v) for k, v in replacements.items())
    pattern = re.compile("|".join(replacements.keys()))
    return pattern.sub(lambda m: replacements[re.escape(m.group())], string)

def get_urls(string) -> list:
    return [t[0] for t in regex.findall(string)]

def mkchdir(dir_):
    # create dir
    try:
        os.mkdir(dir_)
    except FileExistsError:
        pass
    # move to dir
    os.chdir(dir_)

# connect with SSL
mail = imaplib.IMAP4_SSL(imap_host)

# log in
mail.login(imap_user, imap_pass)

mail.select('inbox')

result, data = mail.search(None, 'ALL')

email_id = data[0].split()

if not email_id:
    print_error("No mail found")
    exit(1)
else:
    print_info("You've got mail!")

print(email_id)

parser = Parser()

# create image dir
mkchdir("out")

for d in email_id:
    result, data = mail.fetch(d, "(RFC822)")
    parsedbytes = parser.parsebytes(data[0][1])

    # create directory using date and user email
    from_ = parsedbytes.get("From")
    mkchdir(replace(from_,{"\\<":"","\\>":"","\\\"":""}))

    for part in parsedbytes.walk():
        if part.get_content_type().startswith("image"):
            img = decode_image() # TODO image saving
            save_img(img, "filename")
        if part.get_content_type() == "text/plain":
            # convert to regular text if encoded
            if part.get('Content-Transfer-Encoding') == "base64":
                part = base64.b64decode(str(part.get_payload()))
            # get URLs
            urls = get_urls(str(part))
            with open("urls.txt", 'a') as url_file:
                for url in urls:
                    url_file.write("{}\n".format(url))

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