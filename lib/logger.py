from tqdm import tqdm


class Logger:
	"""Class containing all the application's printing functions."""

	@staticmethod
	def error(string: str, pbar: tqdm | None = None) -> None:
		"""Print an error message."""
		string = "\033[31mERROR: " + string + "\033[0m"

		if pbar:
			pbar.write(string)
		else:
			print(string)

	@staticmethod
	def info(string: str, pbar: tqdm | None = None) -> None:
		"""Print an info message."""
		string = "\033[32mINFO: " + "\033[0m" + string

		if pbar:
			pbar.write(string)
		else:
			print(string)

	@staticmethod
	def warning(string: str, pbar: tqdm | None = None) -> None:
		"""Print a warning message."""
		string = "\033[33mWARN: " + string + "\033[0m"

		if pbar:
			pbar.write(string)
		else:
			print(string)
