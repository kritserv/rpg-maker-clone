def write_line_to_file(line, path) -> None:
	with open(path, "w") as f:
		f.write(line)
		f.close()

def read_line_from_file(path) -> str:
	with open(path, "r") as f:
		line = f.readline()
		f.close()
		return line