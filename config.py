import pickle
import os

def create_empty_config():
	return {'movement' : {'left': '', 'up':'', 'right':'', 'down':'', 'end_of_line': ''}, 
			'directory' : {'default' : ''},
			'file buffer' : {'colors' : ''}}

def load_config():
	if os.path.exists("config.pickle"):
		pickle_in = open("config.pickle", "rb")
		filesize = os.path.getsize("config.pickle")
		if filesize == 0:
			pickle_out = open("config.pickle", "wb")
			pickle.dump(create_empty_config(), pickle_out)
			pickle_out.close()
			pickle_in = open("config.pickle", "rb")
			return dict(pickle.load(pickle_in))
		return dict(pickle.load(pickle_in))
	else:
		pickle_out = open("config.pickle", "wb")
		pickle.dump(create_empty_config(), pickle_out)
		pickle_out.close()
		pickle_in = open("config.pickle", "rb")
		return dict(pickle.load(pickle_in))

# def write_config():
	# pickle_out = open("config.pickle", "wb")
	# pickle.dump(config, pickle_out)
	# pickle_out.close()

def change_config(config, key, value):
	config[key] = value
	pickle_out = open("config.pickle", "wb")
	pickle.dump(config, pickle_out)
	pickle_out.close()

config = load_config()



