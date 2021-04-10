from os import path
class table_io():
	"""
	next(): iter the data as list out
	load([index list]): load table file (with a assigned index list) and return a dict with header, data and notes
	dump(data,header,notes): dump the data to the file
	"""
	def __init__(self,file,sep='\t',end_str='#'):
		"initate args"
		self.file = file
		self.sep=sep
		self.end_str=end_str
		self.colnames = []
		self.notes = []

	def get_colnames(self):
		"parse header and save colnames"
		# set init colnames
		colnames = []
		while 1:
			temp = self.file.readline()
			if not temp: # at the end of file
				raise StopIteration
			else: # if have data
				if temp.strip() == '': # only space data
					continue
				elif temp[0] == '#': # header and save it in notes for temp
					self.notes.append(temp[1:].strip('\n\r'))
				else: # have real data, return colnames and shift up the file pointer
					if self.notes: # if notes, pop the last as colnames
						temp_coln = self.notes[-1]
						if temp_coln.count(self.sep) == temp.count(self.sep):
							colnames = self.notes.pop().split(self.sep)

					# shift up and break
					self.file.seek(-(len(temp)),1)
					break

		self.ncol = len(colnames) if colnames else (temp.count(self.sep)+1)
		return colnames or ['%s_col' % path.basename(self.file.name)]+['col%s' % x for x in range(1,self.ncol)]

	def next(self):
		"iteration method, start with no # prefix and stop at # prefix line"
		# if no colnames, get it then parse real data
		if not self.colnames:
			self.colnames = self.get_colnames()
		# in real data only raise end or skip space, other return list
		while 1:
			temp = self.file.readline()
			if not temp:
				raise StopIteration
			elif temp.strip() == '':
				continue
			elif temp[0] == self.end_str: # if meeting note description
				self.notes.append(temp[1:].strip('\n\r'))
			else:
				break
		rs = temp.strip('\n\r').split(self.sep)
		return rs if len(rs)==self.ncol else rs+['' for x in range(self.ncol-len(rs))]

	def __iter__(self):
		return self

	def load(self,index=[]):
		# get colname first
		colnames = self.get_colnames()

		if index == []:
			index = range(len(colnames))
		else:
			colnames = [colnames[x] for x in index]

		#save the data
		data = []
		while 1:
			try:
				temp_col = self.next()
				data.append([temp_col[x] for x in index])
			except StopIteration:
				break

		return {'colnames':colnames,'data':data,'notes':self.notes}

	def dump(self,data,colnames=[],notes=[]):
		"write into table with data [colnames,notes]"
		# decide ncol with max list length
		ncol = 0 if not data else max(map(len,data))

		if colnames: # check colnames and write
			# add colnames if shorter
			colnames.extend(['undefine_%s' % x for x in range(ncol-len(colnames))])
			self.file.write('#%s\n' % self.sep.join(colnames))

		temp = [self.file.write('%s\n' % self.sep.join(map(str,x+((('',) if type(x)==tuple else [''])*(ncol-len(x)))))) for x in data]
		temp = [self.file.write('#%s\n' % x) for x in notes]
		self.file.close()

	def write(self,data):
		"if data is str, write as '#[str]', if list or two layer list, write like real data"
		if type(data) == str:
			self.file.write('#%s\n' % data)
		elif type(data) == list:
			if type(data[0]) != list:
				self.file.write('%s\n' % '\t'.join(map(str,data)))
			else:
				temp = [self.file.write('%s\n' % '\t'.join(map(str,x))) for x in data]
		else:
			raise Exception('write format must be list or str')
