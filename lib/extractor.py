from typing import TypedDict, Iterable
from unrpa import UnRPA, Version


class Extractor(TypedDict):
	"""Dict containing everything needed to extract data from an RPA archive."""
	extractor: UnRPA
	version: Version
	index:  dict[str, Iterable[tuple[int, int, bytes]]]
	total_files: int
