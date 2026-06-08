class Logger:
	"""Class containing all the application's printing functions."""

	@staticmethod
	def error(string: str) -> None:
		"""Print an error message."""
		print("\033[31mERROR: " + string + "\033[0m")

	@staticmethod
	def info(string: str) -> None:
		"""Print an info message."""
		print("\033[32mINFO: " + "\033[0m" + string)

	@staticmethod
	def warning(string: str) -> None:
		"""Print a warning message."""
		print("\033[33mWARN: " + string + "\033[0m")
