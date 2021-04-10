from uuid import uuid4
def id_get(ex_set=[]):
	id = uuid4().hex
	if id in set(ex_set):
		return id_get(ex_set)
	else:
		return id
