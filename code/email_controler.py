# -*- coding: utf-8 -*-

import os
import re
import zipfile
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


"""
	Required Input:
		- Source folder (src)
		- Archive name (dst)
		- SMTP information
		- Recipient email
"""
DIRECTORY_OF_IMAGES = "/folder/code/static/results/files"
NAME_OF_DESTINATION_ARCHIVE = "results" # test.zip
SUBJECT = "Results APP New" #separated by comma

server = "smtp.gmail.com"
port = 587
username = "address@gmail.com" #change
password = "password" #change
sender = username
isGMAIL = True

# From http://stackoverflow.com/questions/14568647/create-zip-in-python
def zip(src, dst):
	zf = zipfile.ZipFile("%s.zip" % (dst), "w", allowZip64=True)
	src = os.path.abspath(src)
	for d, s, f in os.walk(src):
		for n in f:
			if re.match(r"^.*[.](pdf|png)$", n):
				abs_name = os.path.abspath(os.path.join(d,n))
				arc_name = abs_name[len(src) + 1:]
				zf.write(abs_name, arc_name)
	zf.close()


# From http://stackoverflow.com/questions/3362600/how-to-send-email-attachments-with-python

def send_results(recipients):
    print(DIRECTORY_OF_IMAGES)
    print(NAME_OF_DESTINATION_ARCHIVE)
    zip(DIRECTORY_OF_IMAGES, NAME_OF_DESTINATION_ARCHIVE)
    msg = MIMEMultipart()
    msg['Subject'] = SUBJECT
    msg['From'] = sender
    msg['To'] = recipients

    part = MIMEBase("application", "octet-stream")
    part.set_payload(open(NAME_OF_DESTINATION_ARCHIVE + ".zip", "rb").read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", "attachment; filename=\"%s.zip\"" % (NAME_OF_DESTINATION_ARCHIVE))
    msg.attach(part)

    smtp = smtplib.SMTP(server, port)
    if isGMAIL:
	    smtp.ehlo()
	    smtp.starttls()
	    smtp.ehlo()
    smtp.login(username,password)
    smtp.sendmail(sender, recipients, msg.as_string())
    smtp.close()
