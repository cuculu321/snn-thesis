import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np

def export_color_map(double_list, output_path):
	ax = plt.subplot(111)
	im = ax.imshow(double_list)

	# create an axes on the right side of ax. The width of cax will be 5%
	# of ax and the padding between cax and ax will be fixed at 0.05 inch.
	divider = make_axes_locatable(ax)
	plt.xlabel('predict label')
	plt.ylabel('test label')


	cax = divider.append_axes("right", size="5%", pad=0.1)
	plt.colorbar(im, cax=cax)
	plt.savefig(output_path + ".png", bbox_inches = 'tight', pad_inches = 0)


if __name__ == "__main__":
	from record_synapse import *
	from label_sort import label_sort
	import sys

	args = sys.argv
	input_file = args[1]

	neuron_parsent = import_synapse(input_file + "/answer" + input_file + ".txt")
	#synapse = import_synapse(input_synaps + "/end" + input_synaps +".txt")
	
	sorted_list = []
	
	for i in range(len(neuron_parsent)):
		sorted_list.append(label_sort(neuron_parsent[i]))

	export_color_map(neuron_parsent, input_file + "/color_map" + input_file)
