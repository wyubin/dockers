from peewee import Model,CharField,DateTimeField,ForeignKeyField,Proxy
import datetime
db_proxy = Proxy()

class BaseModel(Model):
	class Meta:
		database = db_proxy

class Job_type(BaseModel):
	name = CharField(unique=True)

class Ip(BaseModel):
	addr = CharField(unique=True)
	country = CharField()

class Mail(BaseModel):
	addr = CharField(unique=True)

class Job(BaseModel):
	guid = CharField(unique=True)
	time_submit = DateTimeField(default=datetime.datetime.now)
	time_process = DateTimeField(null=True)
	time_complete = DateTimeField(null=True)
	job_type = ForeignKeyField(Job_type, related_name='jobs')
	ip = ForeignKeyField(Ip, related_name='jobs')
	mail = ForeignKeyField(Mail, related_name='jobs', null=True)
