class Logger:

	@staticmethod
	def error(string: str) -> None:
		print("\033[31mERROR: " + string + "\033[0m")

	@staticmethod
	def info(string: str) -> None:
		print("\033[32mINFO: " + "\033[0m" + string)

	@staticmethod
	def warning(string: str) -> None:
		print("\033[33mWARN: " + string + "\033[0m")
