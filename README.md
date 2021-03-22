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

### Download Images

To get all the images and links to images, simply:

1. Create a new email address, so it doesn't try to extract data from all your old emails.
1. Share the email address and tell people to send pictures to it.
1. Create a copy of the credentials file with `cp credentials_example.py credentials.py` and fill in with the appropriate credentials.
1. Run `email_extract.py`.

### Combine Images

Once the images have downloaded, you can run `combine.py`.
All images are copied to a `./comb_out/` directory.
If a file has the same name as a file already copied, the new file will have `_x` appended to the end of it, where `x` is `1, 2, 3, ...`.

If you run `combine.py -r`, the images will be renamed randomly to change their original order.
This walks through all the images and renames them in a random order and saves them to a `./comb_out/` directory.

### Remove Duplicates

All images should be combined before removing duplicates.
The following steps require ImageMagick and fdupes, which can be installed with `sudo apt-get install imagemagick` and `sudo apt-get install fdupes`.
To remove duplicates, simply:

1. Create a copy of all images and move them to a temporary directory `rm -rf ./comb_out_tmp/ && mkdir ./comb_out_tmp/ && cp -r ./comb_out/* ./comb_out_tmp/`
1. Resize the images with `cd ./comb_out_tmp/ && mogrify -resize .25% *`
1. Check for duplicates with `
1. Delete temp directory `rm -rf ./comb_out_tmp/`.