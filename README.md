# Email Extractor

A Python email parsing tool which for extracting and sorting images and links in emails.

This was created as a way to quickly download images sent to a new email address for a family reunion.
It also parses links in the messages in case there are links to shared pages.
A list of things that can be extracted are as follows:

- Attachments (any attachments will work, but it is specifically for images and .zip files)
- Images embedded in the email
- URLs in the email message
- Hyperlinks in the email
- Sharing links for Google Drive folders

If none of these are detected in an email, a message will be printed and the emails will be left unread.

## Usage

To get all the images and links to images, simply:

1. Create a new email address, so it doesn't try to extract data from all your old emails.
1. Share the email address and tell people to send pictures to it.
1. Create a copy of the credentials file with `cp credentials_example.py credentials.py` and fill in with the appropriate credentials.
1. Run this script
