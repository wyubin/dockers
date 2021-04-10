from peewee import Model,Proxy,CharField,ForeignKeyField,IntegerField,DateField
db_proxy = Proxy()

class BaseModel(Model):
	class Meta:
		database = db_proxy

class Vdate(BaseModel):
	date = DateField(unique=True)

class Vtype(BaseModel):
	name = CharField(unique=True)

class Ip(BaseModel):
	addr = CharField(unique=True)
	country = CharField()

class Record(BaseModel):
	vdate = ForeignKeyField(Vdate, related_name='record')
	vtype = ForeignKeyField(Vtype, related_name='record')
	ip = ForeignKeyField(Ip, related_name='record')
	times = IntegerField(default=1)
