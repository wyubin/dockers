from peewee import Model,CharField,TextField,DateTimeField,ForeignKeyField,Proxy
import datetime
db_proxy = Proxy()

class BaseModel(Model):
	class Meta:
		database = db_proxy

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

def db_init(db,m_conf):
	db.create_tables([Qtype,Ip,Mail,Question],safe=True)
	for i in m_conf['q_types']:
		Qtype.create(name=i)
