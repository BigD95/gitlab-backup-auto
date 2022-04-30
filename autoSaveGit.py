import subprocess
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

date = str(datetime.datetime.now())
ldate = datetime.date.today()
d = ldate.strftime("%d %b %Y")
c = ["rm -rf /var/opt/gitlab/backups/*", "gitlab-rake gitlab:backup:create", "tar -czf /var/opt/gitlab/backups/save_html.tar.gz /var/www/html/", "mkdir /var/opt/gitlab/backups/crontabs", "cp /var/spool/cron/crontabs/* /var/opt/gitlab/backups/crontabs", "mkdir /var/opt/gitlab/backups/config", "cp -r /etc/gitlab/* /var/opt/gitlab/backups/config" ,"tar -czf /var/opt/gitlab/save_gitlab.tar.gz /var/opt/gitlab/backups", "mv /var/opt/gitlab/save_gitlab.tar.gz /mnt/path"] # /mnt/path is the path to the final remote folder
log = ""
noerreur = True
clerreur = True


def cl():
    global clerreur
    com = subprocess.run("ls /var/www/html", shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
    str_com = str(com.stdout)
    tab = str_com.split()
    for t in tab:
        if "." not in t:
            try:
                c1 ="rm -rf /var/www/html/"+t+"/var/cache/*"
                subprocess.run(c1, shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
            except:
                mail0("Erreur nettoyage\n"+c1)
                clerreur = False


def mail0(txt):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login('sender_email', 'password**')
    toaddr = ['receiver_email1', 'receiver_email2', 'receiver_email3']
    cc = ['receiver_email2', 'receiver_email3']
    msg = MIMEMultipart()
    msg['From'] = 'GitLab Local'
    msg['to'] = 'receiver_email1'
    msg['Cc'] = ','.join(cc)
    msg['Subject'] = 'GitLab Backup Report'
    message = "GitLab Backup Report \n "+txt+ "\n Cordially"
    msg.attach(MIMEText(message, 'plain'))
    text = msg.as_string()
    server.sendmail('sender_email', toaddr, text)
    server.quit()


cl()
if clerreur:
    mail0("Cleaning completed without error !!")
else:
    mail0("Cleaning completed with error !!")

for comma in c:
    if noerreur:
        try:
            com = subprocess.run(comma, shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
            str_com = str(com.stdout)
        except:
            mail0("Error \n"+comma)
            noerreur = False
            break

if noerreur:
    mail0("Backup completed successfully. !!!\n")
else:
    mail0("Backup ended incorrectly. Verification !!!\n")
