from peewee import Model,CharField,TextField,ForeignKeyField,IntegerField,FloatField,Proxy
db_proxy = Proxy()

class Base(Model):
	class Meta:
		database = db_proxy

class Contig(Base):
	name = CharField(unique=True)
	seq = TextField()

class Taxa(Base):
	contig = ForeignKeyField(Contig, related_name='taxas', primary_key=True)
	taxa_id = IntegerField()

class Count(Base):
	contig = ForeignKeyField(Contig, related_name='counts', primary_key=True)
	data = TextField()
