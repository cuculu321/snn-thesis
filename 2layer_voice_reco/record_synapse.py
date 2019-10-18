from datetime import datetime

def export_txt(target_list, output_name):
	save_path = "synapse_recoed/" + output_name + ".txt"
	
	with open(save_path, mode = 'w') as save_file:
		for layer_synapse in target_list:
			for synapse in layer_synapse:
				save_file.write(str(synapse) + ",")
			save_file.write("\n")
		save_file.close()


def create_timestamp():
	timestamp = datetime.now()
	return (timestamp.strftime('%Y') + 
			"-" + timestamp.strftime('%m') + 
			"-" + timestamp.strftime('%d') + 
			"-" + timestamp.strftime('%H') +
			"-" + timestamp.strftime('%M'))


def import_synapse(txt_path_str):
	synapse_str = read_txtfile(txt_path_str)
	return synapse_str2list(synapse_str)


def read_txtfile(txt_path_str):
	with open(txt_path_str, mode = 'r') as f:
		return f.read()


def synapse_str2list(synapse_str):
	synapse_list = []
	for splite_line in synapse_str.splitlines():
		synapse_list.append(splite_line.split(","))
		synapse_list[-1].pop(-1)

	return synapse_list


if __name__ == "__main__":
	synapse = import_synapse("synapse_recoed/sample_synapse.txt")
	export_txt(synapse, create_timestamp())
