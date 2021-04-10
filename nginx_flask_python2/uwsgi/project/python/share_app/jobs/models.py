from os import path
from peewee import Model,CharField,DateTimeField,ForeignKeyField,SqliteDatabase
import datetime
from config import jobs as app_conf
from config import system as sys_conf
db_path = path.abspath(path.join(sys_conf._basedir,app_conf.db_path))
db = SqliteDatabase(db_path,**sys_conf.DATABASE_CONNECT_OPTIONS)

class BaseModel(Model):
	class Meta:
		database = db

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

if not path.exists(db_path):
	db.create_tables([Job_type,Ip,Mail,Job],safe=True)
	for i in app_conf.type2info:
		Job_type.create(name=i)
