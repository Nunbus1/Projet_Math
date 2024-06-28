import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from classes.Item import Item
from classes.Bin import Bin


def plot_item(ax, position, dimensions, color):
	x, y, z = position
	x, y, z = float(x), float(y), float(z)
	dx, dy, dz = dimensions
	dx, dy, dz = float(dx), float(dy), float(dz)
	vertices = [
		[x, y, z],
		[x + dx, y, z],
		[x + dx, y + dy, z],
		[x, y + dy, z],
		[x, y, z + dz],
		[x + dx, y, z + dz],
		[x + dx, y + dy, z + dz],
		[x, y + dy, z + dz]
	]
	faces = [
		[vertices[0], vertices[1], vertices[2], vertices[3]],
		[vertices[4], vertices[5], vertices[6], vertices[7]],
		[vertices[0], vertices[1], vertices[5], vertices[4]],
		[vertices[2], vertices[3], vertices[7], vertices[6]],
		[vertices[1], vertices[2], vertices[6], vertices[5]],
		[vertices[4], vertices[7], vertices[3], vertices[0]]
	]
	poly3d = Poly3DCollection(faces, facecolors=color, linewidths=1, edgecolors='r', alpha=.25)
	ax.add_collection3d(poly3d)

def plot_dim2(bins):
	num_bins = len(bins)
	num_cols = 4
	num_rows = (num_bins + num_cols - 1) // num_cols
	fig, axs = plt.subplots(num_rows, num_cols, figsize=(num_cols * 5, num_rows * 5), constrained_layout=True)
	colors = plt.cm.tab20.colors
	axs = axs.flatten()
	for bin_index, bin_ in enumerate(bins):
		ax = axs[bin_index]
		for j, item in enumerate(bin_.items):
			#longueur, largeur, x, y = item
			longueur = item.dims[0]
			largeur = item.dims[1]
			x = item.position[0]
			y = item.position[1]
			color = colors[j % len(colors)]
			ax.fill([y, y, y + largeur, y + largeur], [x, x + longueur, x + longueur, x], color=color, alpha=0.5)
		ax.set_xlim(0, Bin.dims[0])
		ax.set_ylim(0, Bin.dims[1])
		#ax.invert_yaxis()
		ax.set_xlabel('Longueur')
		ax.set_ylabel('Largeur')
		ax.set_title(f'Conteneur {bin_index + 1}')
	for j in range(bin_index + 1, len(axs)):
		fig.delaxes(axs[j])
	plt.show()

def plot_dim3(bins):
	num_bins = len(bins)
	num_cols = 4
	num_rows = (num_bins + num_cols - 1) // num_cols
	fig = plt.figure(figsize=(num_cols * 5, num_rows * 5))

	for bin_index, bin_ in enumerate(bins):
		ax = fig.add_subplot(num_rows, num_cols, bin_index + 1, projection='3d')
		colors = plt.cm.tab20.colors
		color_idx = 0
		for item in bin_.items:
			color = colors[color_idx % len(colors)]
			plot_item(ax, item.position, item.dims, color)
			color_idx += 1
		ax.set_xlim(0, float(Bin.x))
		ax.set_ylim(0, float(Bin.y))
		ax.set_zlim(0, float(Bin.z))
		ax.set_xlabel('Longueur')
		ax.set_ylabel('Largeur')
		ax.set_zlabel('Hauteur')
		ax.set_title(f'Wagon {bin_index + 1} - Nombre d\'objets: {len(bin_.items)}')
	plt.tight_layout()
	plt.show()

def plot_bins_on_sheet(bins, dimensions=3):
	if dimensions == 2:
		plot_dim2(bins)
	elif dimensions == 3:
		plot_dim3(bins)
	else:
		print('ERROR')
