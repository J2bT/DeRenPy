from lib.logger import Logger


class Misc:

	@staticmethod
	def can_unrpa(rpa_list) -> bool:  # TODO: Maybe move to a new module?
		if len(rpa_list) == 0:
			Logger.error("No RPA files in the input directory. Pull them before selecting this option.")
			return False
		return True

