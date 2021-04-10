import os
import operator as op
from range_tool import non_over_long_i,non_overlap
from Bio.Blast import NCBIXML
class parser():
	"""load blast m0,m8 or m9 format file and return iter object including a list(single query) of blast info object
	
	:param l_r: file read object of blast output file.
	:type l_r: file
	:returns: list of hit object of blast info(q_id,t_id,ident,a_l,q_s,q_e,t_s,t_e,e,bits, and a_r only in m0).
	"""
	def __init__(self,f_r):
		"initate args including cutoff and detect format"
		self.f_r = NCBIXML.parse(f_r)
		self.cutoff_list = []
		self.max_hits = 99999
		self.sort_by = 'e'
		self.attr_list = ['q_id','t_id','a_l','q_s','q_e','t_s','t_e','strand','ident','e','bits']
		self.colnames = ['seq_id','hit_seq','alignment_length','query_start','query_end','hit_start','hit_end','strand','identity','evalue','bits']

	def check_cutoff(self, hit):
		"check single hit blast info pass the threshold or not and return bool"
		for x,y,z in self.cutoff_list: # x:attr, y:op, z:value
			if not getattr(op,y)(getattr(hit,x,0),z):
				return False
		
		return True
	
	def order_proc(self,hits):
		"sort hits based on self.sort_by"
		return sorted(hits, key = lambda x: getattr(x,self.sort_by), reverse = (self.sort_by != 'e'))
	
	class hit(): pass
	
	def next(self):
		"iteration method for m0 format and the self.f_r is a blast iter object"
		hits = []
		#find a blast that has one hit at least
		blast_o = self.f_r.next()
		while not getattr(blast_o,'alignments',1): # skip blast info if query has no hits
			blast_o = self.f_r.next()
		
		if not blast_o: # if the end
			raise StopIteration
		
		for j in blast_o.alignments:
			for k in j.hsps:
				hit = self.hit()
				hit.q_id,hit.t_id = blast_o.query.split()[0],j.title.split()[1]
				hit.ident,hit.a_l = round(k.identities*1.0/k.align_length,2),k.align_length
				hit.a_r = hit.a_l*1.0/blast_o.query_letters
				hit.q_s,hit.q_e,hit.t_s,hit.t_e = k.query_start,k.query_end,k.sbjct_start,k.sbjct_end
				hit.e,hit.bits = k.expect,k.bits
				hit.q_align,hit.t_align = k.query,k.sbjct
				if k.frame:
					hit.strand = '/'.join(['Plus' if x==1 else 'Minus' for x in k.frame])
				elif k.strand:
					if k.strand[0]:
						hit.strand = '/'.join(k.strand).replace('Plus','+').replace('Minus','-')
					else:
						hit.strand = '-'
				
				if self.check_cutoff(hit):
					hits.append(hit)
		
		return self.order_proc(hits)[:self.max_hits]
	
	def hits2table_l(self,hits):
		"transform hits list to table_like two layer list"
		return [[getattr(x,y,'-') for y in self.attr_list] for x in hits]

	def __iter__(self):
		return self

def no_overlap_filter(hits):
	"""
	just find no overlap and return back
	
	:param hits: list of hit object from a single query.
	:type hits: list
	:returns: a list of hits that non overlap in query seq.
	"""
	l_range = []
	for i in hits: # prepare range
		q_range = sorted([i.q_s,i.q_e])
		q_range[0] -= 1
		l_range.append(q_range)
	
	return [hits[x] for x in non_overlap(l_range)]

def q2t_no_over_long(hits):
	"""
	split different hit id and find the multiple no overlap region both in query and target and return the multiple hits and region infomation
	
	:param hits: list of hit object from a single query.
	:type hits: list
	:returns: a list of multiple region info list[h_id,bs,hits index].
	"""
	hit2range,hit2inds = {},{}
	for i,j in enumerate(hits): # collect hit2range
		q_range = sorted([j.q_s,j.q_e])
		q_range[0] -= 1
		t_range = sorted([j.t_s,j.t_e])
		t_range[0] -= 1
		hit2range.setdefault(j.t_id,[]).append([q_range,t_range])
		hit2inds.setdefault(j.t_id,[]).append(i)
	
	result = []
	for i,j in hit2range.items():
		q_ind = non_over_long_i([x[0] for x in j]) # query side no over
		m_ind = [q_ind[y] for y in non_over_long_i([j[x][1] for x in q_ind])] # target side no over on previous output
		r_ind = [hit2inds[i][x] for x in m_ind]
		bs = [j[x][0][1]-j[x][0][0] for x in m_ind]
		result.append([i,bs,r_ind])
	
	return result