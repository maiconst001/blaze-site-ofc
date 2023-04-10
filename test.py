import smtplib
from random import choice
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp-mail.outlook.com"
SMTP_PORT = 587
SMTP_USERNAME = "maisantosmix2018@hotmail.com"
SMTP_PASSWORD = "Negucio2018$"

EMAIL_FROM = "maisantosmix2018@hotmail.com"
EMAIL_TO = "videos2018pg@gmail.com"

def send_email():
    code = ''
    for c in range(6):
        code += str(choice(range(0, 10)))

    html = '<h1>seu codigo de confirmação botwinner <br><br> codigo: ' + code + '</h1>'
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Botwinner - bussines"
    msg['From'] = EMAIL_FROM 
    msg['To'] = EMAIL_TO

    part2 = MIMEText(html, 'html')
    msg.attach(part2)

    debuglevel = False
    mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    mail.set_debuglevel(debuglevel)
    mail.starttls()
    mail.login(SMTP_USERNAME, SMTP_PASSWORD)
    mail.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    mail.quit()
    return code


send_email()