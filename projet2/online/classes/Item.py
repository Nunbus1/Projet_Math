from functools import reduce
from decimal import *
import settings


class Item:
	def __init__(self, numero, nom, x, y, z):
		self.numero = numero
		self.nom = nom
		self.dims = [x, y, z]
		self.position = [None, None, None]
		self.rotation = [0, 0, 0]

	def set_position(self, res):
		if (not settings.contains_liquid) and settings.dimension > 1:
			self.position = res[1]

	def set_rotation(self, res): # Si dimension == 2, seulement la rotation en z est possible
		if (not settings.contains_liquid) and settings.dimension > 1:
			self.rotation = res[1]

	def get_volume(self, dim_cut):
		return Decimal(reduce(lambda x, y: x*y, self.dims[:dim_cut]))

	def get_position(self):
		return self.position

	def get_rotation(self):
		return self.rotation

	def overlaps(self, item, pos, dimension_):
		res = False
#		print(pos)
#		print(item.dims)
#		print(self.position)
#		print(self.dims)
		for i in range(dimension_):
			res = res or (pos[i] + item.dims[i] <= self.position[i] or self.position[i] + self.dims[i] <= pos[i])
		return not res

	def test_gap(self, bin_dims, ds, dimension_):
		res = False
		for i in range(1, dimension_):
			res = res or (bin_dims[i] - self.position[i] - self.dims[i] >= ds[i])
		return res

	def get_collisions(self, items, pos, dimension_):
		coll_list = list()
		for it in items:
			if it.overlaps(self, pos, dimension_):
				coll_list.append(it)
		return coll_list

	def __repr__(self):
		return f"<Item[{self.numero}] '{self.nom}' {self.dims}>"
