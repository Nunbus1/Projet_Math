def init():
	global dimension, contains_liquid, mlt_proc, precision, is_offline, opti
	dimension = 1
	contains_liquid = True
	mlt_proc = True
	precision = 1
	is_offline = False
	opti = list()

def get_all():
	return dimension, contains_liquid, mlt_proc, precision, is_offline, opti
