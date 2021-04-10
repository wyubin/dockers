from peewee import Model,CharField,TextField,ForeignKeyField,IntegerField,FloatField,Proxy
db_proxy = Proxy()

class Base(Model):
	class Meta:
		database = db_proxy

class Contig(Base):
	name = CharField(unique=True)
	seq = TextField()

class ORF(Base):
	contig = ForeignKeyField(Contig, related_name='orfs', primary_key=True)
	range_info = TextField(null=True)
	seq = TextField()

class Anno_db(Base):
	name = CharField(unique=True)
	method = CharField()
	version = CharField()
	url_pre = CharField(unique=True)

class Anno_hit(Base):
	anno_db = ForeignKeyField(Anno_db, related_name='anno_hits')
	ac = CharField(unique=True)
	des = TextField()

class Anno_info(Base):
	contig = ForeignKeyField(Contig, related_name='anno_infos')
	anno_hit = ForeignKeyField(Anno_hit, related_name='anno_infos')
	align_info = TextField(null=True)

class Taxa(Base):
	contig = ForeignKeyField(Contig, related_name='taxas', primary_key=True)
	taxa_id = IntegerField()

class FPKM(Base):
	contig = ForeignKeyField(Contig, related_name='fpkms', primary_key=True)
	data = TextField()
