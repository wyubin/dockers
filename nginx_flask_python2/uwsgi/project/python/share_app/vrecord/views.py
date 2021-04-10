"check visit type and "
import os,sys,GeoIP
from peewee import SqliteDatabase
from datetime import date
from models import db_proxy,Vdate,Vtype,Ip,Record
from app import sys_conf

# init views db
db_path = os.path.join(sys_conf.db_dir,'vrecord.sqlite')
db = SqliteDatabase(db_path, **sys_conf.DATABASE_CONNECT_OPTIONS)
db_proxy.initialize(db)
if not os.path.exists(db_path):
	db.create_tables([Vdate,Vtype,Ip,Record],safe=True)
# initiate vtype
for i in sys_conf.mconfig['vrecord']['vtype']:
	t_sql = Vtype.select().where(Vtype.name == i)
	if not t_sql.count():
		Vtype.create(name = i)

class record_han():
	def __init__(self):
		self.gi = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)

	def visit(self,ip_addr,v_string):
		if v_string in sys_conf.mconfig['vrecord']['vtype']:
			vtype = Vtype.select().where(Vtype.name == v_string)[0]
			tdate = self._today_check()
			ip = self._ip_check(ip_addr)
			# check Record
			t_sql = Record.select().where(Record.vtype == vtype,Record.vdate == tdate,Record.ip == ip)
			if t_sql.count():
				ret = t_sql[0]
				ret.times += 1
				ret.save()
			else:
				ret = Record.create(vtype = vtype, vdate = tdate, ip = ip, times=1)
			return ret
		else:
			return []

	def _today_check(self):
		"check if today in db, then return or create one"
		t_day = date.today()
		t_sql = Vdate.select().where(Vdate.date == t_day)
		if t_sql.count():
			return t_sql[0]
		else:
			return Vdate.create(date = t_day)

	def _ip_check(self,ip_addr):
		"check ip exist or not and return ip object"
		t_sql = Ip.select().where(Ip.addr == ip_addr)
		if t_sql.count():
			return t_sql[0]
		else:
			return Ip.create(addr=ip_addr,country=self.gi.country_code_by_name(ip_addr))

	def info(self,v_string,date_f='month'):
		dates,visits = [],[]
		fd = {'day':'%m-%d-%Y','month':'%m-%Y','year':'%Y'}
		t_sql = """SELECT strftime('%s', vdate.date) as d_str, sum(record.times)
				FROM record,vtype,vdate
				Where record.vtype_id = vtype.id
				AND record.vdate_id=vdate.id
				AND vtype.name IN (%s)
				group by d_str
				order by vdate.date ASC """ % (fd[date_f],','.join(['"%s"' % x for x in v_string.split(',')]))
		t_sql = db.execute_sql(t_sql)
		for i in t_sql:
			dates.append(i[0])
			visits.append(i[1])
		return {'dates':dates,'visits':visits} if dates else []
