import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np

def export_color_map(double_list):
	ax = plt.subplot(111)
	im = ax.imshow(double_list)

	# create an axes on the right side of ax. The width of cax will be 5%
	# of ax and the padding between cax and ax will be fixed at 0.05 inch.
	divider = make_axes_locatable(ax)
	cax = divider.append_axes("right", size="5%", pad=0.1)
	plt.colorbar(im, cax=cax)
	plt.savefig("cb_append_axes.png", bbox_inches = 'tight', pad_inches = 0)


if __name__ == "__main__":
	from record_synapse import *
	import sys

	args = sys.argv
	input_file = args[1]

	neuron_parsent = import_synapse("end/" + str(input_file) + ".txt")

	export_color_map(np.random.randn(100).reshape((10, 10)))
