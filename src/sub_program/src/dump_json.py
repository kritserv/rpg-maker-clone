from json import dump

def json_dumper(path, content) -> None:
	with open(path, "w") as f:
		dump(content, f)
		f.close()