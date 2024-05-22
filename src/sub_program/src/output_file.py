def write_line_to_file(line, filename) -> None:
	with open(filename, "w") as f:
		f.write(line)

def read_line_from_file(filename) -> str:
	with open(filename, "r") as f:
		return f.readline()