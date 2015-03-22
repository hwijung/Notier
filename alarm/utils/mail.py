import os, smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders

import time
import datetime
import smtplib

gmail_user="hwijung.ryu@gmail.com"
gmail_pwd="jafw,tie1" 

def send_gmail(to, subject, text, html, attach):
    msg=MIMEMultipart('alternative')
    msg['From']=gmail_user  
    msg['To']=to
    msg['Subject']=subject
    msg.attach(MIMEText(text, 'plain'))
    msg.attach(MIMEText(html, 'html'))

    #managing attachment 
    #part=MIMEBase('application','octet-stream')
    #part.set_payload(open(attach, 'rb').read())
    #Encoders.encode_base64(part)
    #part.add_header('Content-Disposition','attachment; filename="%s"' % os.path.basename(attach))
    #msg.attach(part)

    mailServer=smtplib.SMTP("smtp.gmail.com",587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user,gmail_pwd)
    mailServer.sendmail(gmail_user, to, msg.as_string())
    mailServer.close()

def send_mail_with_local_server(to, subject, text):

    # 이메일 메세지 컨테이너를 만든다
    msg = MIMEMultipart()
    msg['Subject'] = subject
     
    # me == 보내는 사람의 주소
    # family = 받는 사람들의 모든 주소
    me = "root@ryuniverse.com"
    msg['From'] = me
    msg['To'] = to
      
    # 로컬 서버를 통해 메일을 보낸다.
    s = smtplib.SMTP('localhost')
    s.sendmail(me, to, msg.as_string())
    s.quit()
    
def mainLoop(): 
    title="title"
    #attach_file="send_mail.py"  .

    f = open("text.txt", "r")   #<------ content in text
    message = f.read()
    f.close()

    f = open("html.html", "r")   #<------ content in HTML
    html = f.read()
    f.close()

    print "Program Ready"
    print "----------------------"
    f = open("list.txt", "r")   # <---- mailing lists
    emails = f.readlines()
    for email in emails:
        email = email.strip('\r')
        email = email.strip('\n')
        email = email.strip(' ')
        email = email.strip('\t')
        if email == "" :
            continue
        print "[" + str(datetime.datetime.now()) + "] Sending email to " + email + "..."
        send_gmail(email,title,message,html,"")
        print "[" + str(datetime.datetime.now()) + "] Complete... Waiting for 5 seconds."  # send every 5 minutes
        time.sleep(5)
    print "Mails have just sent. The program is going to end." 

'''
if __name__ == "__main__":
    mainLoop()
'''