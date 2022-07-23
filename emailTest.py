
import smtplib

# list of email_id to send the mail
mail_list = ['shubhamprakash444@ug.cusat.ac.in', 'samer.smiley123@gmail.com', 'gautamanand30@gmail.com']

from cred import psk

for dest in mail_list:
	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.starttls()
	s.login("covisionteam@gmail.com", psk)
	message = "Hello Auth 2!!"
	s.sendmail("covisionteam@gmail.com", dest, message)
	s.quit()
