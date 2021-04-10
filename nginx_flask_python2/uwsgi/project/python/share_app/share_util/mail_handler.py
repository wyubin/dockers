import smtplib
from os import path
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from validate_email import validate_email
from jinja2 import Environment, FileSystemLoader
class mail_handler():
	"""create a smtp server, a send function, and finally close()
	"""
	def __init__(self,from_addr, pw, smtp_str='smtp.gmail.com:587'):
		"get two object self.from and self.smtp"
		self.from_addr = from_addr
		self.smtp = smtplib.SMTP(smtp_str)
		self.smtp.ehlo()
		self.smtp.starttls()
		self.smtp.login(self.from_addr,pw)

	def send(self, type2addrs,subject,body,body_type='plain'):
		"send mail and return smtp error"
		msg = MIMEMultipart()
		msg['From'] = self.from_addr
		mails = []
		for i,j in type2addrs.items():
			if len(j):
				msg[i] = ','.join(j)
				mails.extend(j)

		msg['Subject'] = subject
		msg.attach(MIMEText(body, body_type))
		return self.smtp.sendmail(msg['From'],mails,msg.as_string())

def verify(mail_addr):
	"check mail address validation"
	return validate_email(mail_addr,verify=True)

def jinja2mail(mail_info):
	"based on {smpt_info,mail_list,path,args,title} to render into jinja and send out"
	t_dir,tmpl_name = path.split(mail_info['path'])
	jinja_tmpl = Environment(loader=FileSystemLoader(t_dir))
	tmpl = jinja_tmpl.get_template(tmpl_name)
	mail_han = mail_handler(*[mail_info['smpt_info'][x] for x in ['account','password','server']])
	mail_han.send(mail_info['mail_list'], mail_info['title'], tmpl.render(mail_info['args']),'html')
	return mail_han
