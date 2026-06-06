class Logger:

	@staticmethod
	def error(string):
		#print("\033[31m"+"ERROR: "+string+"\033[0m")
		print("[ERROR]: " + string)

	@staticmethod
	def info(string):
		#print("\033[32m"+"INFO: "+"\033[0m"+string)
		print("[INFO]: " + string)

	@staticmethod
	def warning(string):
		#print("\033[33m"+"WARN: "+string+"\033[0m")
		print("[WARN]: " + string)
