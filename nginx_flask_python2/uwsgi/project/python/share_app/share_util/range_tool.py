def range_merge(l_n):
	"""merge the 2 layer list about range, sort the range with start first and find overlap one loop
	
	:param l_n: list of range number(list or tuple).
	:type l_n: list
	:returns: list of merged range.
	"""
	l_n = sorted(map(sorted,l_n),key = lambda x: x[0])
	rg_mg = [l_n[0]]
	for i in l_n[1:]:
		map_ind = sum([x <= rg_mg[-1][1] for x in i])
		if map_ind == 1:# overlap with one end
			rg_mg[-1] = [rg_mg[-1][0],i[1]]
		elif map_ind == 0: # if no overlap totally
			rg_mg.append(i)
	
	return rg_mg

def collapse_i(l_n):
	"""collapse the smaller inclusive sequence, keep represent range
	
	:param l_n: list of range number(list or tuple).
	:type l_n: list
	:returns: indexs of represent range.
	"""
	l_n = map(sorted,l_n)
	l_n_i = [i[0] for i in sorted(enumerate(l_n), key=lambda x:x[1][0])]
	rg_mg = [l_n_i[0]]
	for i in l_n_i[1:]:
		if l_n[i][1] > l_n[rg_mg[-1]][1]: 
			if l_n[i][0] == l_n[rg_mg[-1]][0]: # anti-inclusive
				rg_mg[-1] = i
			else: # one end overlap or non-overlap
				rg_mg.append(i)
	
	return [l_n[x] for x in rg_mg]

def non_overlap(l_n):
	"""find the no overlap region flow the order
	
	:param l_n: list of range number(list or tuple).
	:type l_n: list
	:returns: indexs of non_overlap range.
	"""
	l_n = map(sorted,l_n)
	ret_ind = [] # init container for ind
	for i_ind,i_range in enumerate(l_n):
		loci_m = 0
		for p_ind in ret_ind: # scan checked no over list
			if not (i_range[0] >= l_n[p_ind][1] or i_range[1] <= l_n[p_ind][0]): # when overlap
				loci_m = 1
				break
		
		if not loci_m: # finish scan and no loci_m
			ret_ind.append(i_ind)
	
	return ret_ind

def non_over_long_i(l_n):
	"""find the longest non-overlap extended range
	
	:param l_n: list of range number(list or tuple).
	:type l_n: list
	:returns: indexs of non_over_long range.
	"""
	l_n = map(sorted,l_n)
	l_n_i = [i[0] for i in sorted(enumerate(l_n), key=lambda x:x[1][0])]
	t_l_n = [(x[0],x[1]-x[0]) for x in l_n]
	# Prepare (BackCount, BackLink) array with default (-1,-1)
	bb = [(-1,-1) for x in t_l_n] # (BackCount, BackLink)
	
	# set init longlen and longtail as -1,-1
	long_len, long_tail=-1,-1
	
	# Algorithm
	for i in l_n_i:
		if (bb[i][0] == -1): # visit first time, set backcount as 0
			bb[i] = (0, bb[i][1])
		
		i_to_len = t_l_n[i][1] + bb[i][0]
		if (i_to_len) > long_len: # bigget than known long len, reset the long info
			long_len = i_to_len
			long_tail = i
		
		for j in [l_n_i[x] for x in xrange(l_n_i.index(i)+1,len(l_n_i)) if l_n[l_n_i[x]][0] >= l_n[i][1]]: # find alter range tuple index
			if (bb[j][0] == -1) or (bb[j][0] < i_to_len): # if j is first visit or j backcount < i self and backcount
				# can be linked
				j_to_len = bb[j][0] + t_l_n[j][1]
				bb[j] = (bb[i][0] + t_l_n[i][1], i) # reset backcount and backlink
				if j_to_len > long_len: # if self and backcount of j > long len, record long info
					long_len = j_to_len
					long_tail = j
	
	# Done! now build up the solution
	ret=[]
	while (long_tail > -1):
		ret.insert(0,long_tail)
		long_tail = bb[long_tail][1]
	return ret