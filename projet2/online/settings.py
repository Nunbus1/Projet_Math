#!/usr/bin/python3

def init():
	global dimension, contains_liquid, mlt_proc
	dimension = 1
	contains_liquid = True
	mlt_proc = True

def get_all():
	return dimension, contains_liquid, mlt_proc
