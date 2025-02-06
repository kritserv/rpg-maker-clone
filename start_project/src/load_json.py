from json import load, dump

def json_loader(path) -> dict:
	with open(path) as f:
		return load(f)

def json_saver(path, data):
	with open(path, "w") as f:
		dump(data, f, indent=4)
