from os import path
from peewee import Model,CharField,TextField,DateTimeField,ForeignKeyField,SqliteDatabase
import datetime
from config import contact as app_conf
from config import system as sys_conf
db_path = path.abspath(path.join(sys_conf._basedir,app_conf.db_path))
db = SqliteDatabase(db_path,**sys_conf.DATABASE_CONNECT_OPTIONS)

class BaseModel(Model):
	class Meta:
		database = db

class Qtype(BaseModel):
	name = CharField(unique=True)

class Ip(BaseModel):
	addr = CharField(unique=True)
	country = CharField()

class Mail(BaseModel):
	addr = CharField(unique=True)

class Question(BaseModel):
	content = TextField()
	time_submit = DateTimeField(default=datetime.datetime.now)
	qtype = ForeignKeyField(Qtype, related_name='Question')
	ip = ForeignKeyField(Ip, related_name='Question')
	mail = ForeignKeyField(Mail, related_name='Question')

if not path.exists(db_path):
	db.create_tables([Qtype,Ip,Mail,Question],safe=True)
	for i in app_conf.q_type:
		Qtype.create(name=i)
