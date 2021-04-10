import os
class fasta_mini_han():
	"load fasta format file and iteration output a object with name and seq keys"
	def __init__(self,f_r,f_type='fasta'):
		"initate args. file object and type"
		self.f_r,self.type = f_r,f_type
		self.ids = set()

	class seq_o():
		"use seq_o() to create a new seq object"
		def __init__(self,name='',seq=''):
			"args are 'name','seq'"
			self.name,self.seq,self.qual_seq = name,seq,[]
			self.comp_dict = {'a':'t','c':'g','g':'c','t':'a','n':'n','A':'T','C':'G','G':'C','T':'A','N':'N'}

		def fasta(self,length=70):
			if self.name or self.seq:
				return '>%s\n%s\n' % (self.name,'\n'.join([self.seq[i:i+length] for i in range(0,len(self.seq),length)]))
			else:
				return ''

		def qual(self,length=20):
			if self.name or self.qual_seq:
				return '>%s\n%s\n' % (self.name,'\n'.join([' '.join(map(str,self.qual_seq[i:i+length])) for i in range(0,len(self.qual_seq),length)]))
			else:
				return ''

		def reverse_complement(self):
			return ''.join([self.comp_dict.get(x,x) for x in self.seq[::-1]])

	def next(self):
		"iteration method"
		#if EOF at beginning, stop iteration
		temp = self.f_r.readline()
		if not temp:
			raise StopIteration
		else:
			self.f_r.seek(-(len(temp)),os.SEEK_CUR)

		#set init_dict
		seq_d = self.seq_o()

		#get seq seqments when no '>' or ''
		while 1:
			temp = self.f_r.readline()
			if not temp:
				break
			elif not temp.rstrip():
				continue
			elif temp[0] == '>' and not seq_d.name:
				t_name = temp[1:].rstrip()
				if t_name in self.ids:
					print('%s already exist' % t_name)
					continue
				else:
					self.ids.add(t_name)
					seq_d.name = t_name
					temp_data = []
			elif temp[0] == '>' and seq_d.name:
				self.f_r.seek(-(len(temp)),os.SEEK_CUR)
				break
			else:
				temp = temp.rstrip()
				temp_data.append(temp)
		if self.type == 'fasta':
			seq_d.seq=''.join(temp_data)
		elif self.type == 'qual':
			temp = [seq_d.qual_seq.extend(map(int,x.split())) for x in temp_data]
		return seq_d

	def __iter__(self):
		return self
