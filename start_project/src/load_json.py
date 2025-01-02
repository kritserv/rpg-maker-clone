from json import load, dump

def json_loader(path) -> dict:
	with open(path) as f:
		json_load = load(f)
		f.close()
	return json_load

def json_saver(path, data):
	with open(path, "w") as f:
		dump(data, f)
	f.close()
