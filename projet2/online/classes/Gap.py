from functools import reduce
from decimal import *


class Gap():
	def __init__(self, dimensions=2, pos=list(), dim=list()):
		if pos:
			self.pos = pos
		else:
			self.pos = [Decimal('0')]*dimensions
		if dim:
			self.dim = dim
		else:
			self.dim = [Decimal('0')]*dimensions

	def get_pos(self):
		return self.pos.copy()

	def get_dim(self):
		return self.dim.copy()

	def get_volume(self):
		return Decimal(reduce(lambda x, y: x*y, self.dim))

	def __repr__(self):
		return f"<Gap pos:{self.pos} dim:{self.dim}>"
