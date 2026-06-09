import os
from pathlib import Path
import shutil

from tqdm import tqdm
from unrpa import UnRPA
import unrpyc

from lib.extractor import Extractor
from lib.logger import Logger


class FileHelper:
	"""Helper class containing all functions related to file handling."""

	@staticmethod
	def makedirs() -> None:
		"""Create all necessary directories."""
		Path("./01_Input_RPA").mkdir(exist_ok=True)
		Path("./02_Output_RPA").mkdir(exist_ok=True)
		Path("./03_Input_RPYC").mkdir(exist_ok=True)
		Path("./04_Output_RPYC").mkdir(exist_ok=True)

	@staticmethod
	def nukedirs() -> None:
		"""Delete all directories created by `makedirs()`."""
		shutil.rmtree("./01_Input_RPA")
		shutil.rmtree("./02_Output_RPA")
		shutil.rmtree("./03_Input_RPYC")
		shutil.rmtree("./04_Output_RPYC")

	@staticmethod
	def rpa_list() -> list[str]:
		"""Get a list of RPA files in the input directory."""
		files = Path("./01_Input_RPA").glob("*.rpa")
		return [f.name for f in files]

	@staticmethod
	def get_game_directory(user_input: str) -> Path | None:
		"""Find the path to the `/game` subfolder of a Ren'Py game based on the user input.

		:param user_input: string with a path to one of:
			1. The root directory of a Ren'Py game
			2. The `/game` subfolder of a Ren'Py game
		:returns: a Path object to the `/game` subfolder or None if not found
		"""
		path = Path(user_input).resolve()

		if not path.is_dir():
			Logger.error(f"Path does not exist or is not a directory: {path}")
			return None

		# 1. Check for Root Indicators
		if (path / "renpy").is_dir() and (path / "lib").is_dir():
			game_dir = path / "game"
			if game_dir.is_dir():
				return game_dir
			Logger.warning(
				"Seems to be Ren'Py root, but '/game' subfolder is missing. Checking for game content indicators...")

		# 2. Check for Game Content Indicators
		has_game_files = (
				any(path.glob("*.rpa")) or
				any(path.glob("*.rpyc")) or
				any(path.glob("*.rpy"))
		)

		if has_game_files:
			return path

		Logger.error(
			"Invalid Ren'Py path.\n"
			"No Root Indicators (./renpy and ./lib subfolders)\n"
			"or Game Content Indicators (.rpa archives, .rpyc scripts, or .rpy source files)\n"
			"found."
		)
		return None

	@staticmethod
	def copy_with_pbar(src: Path, dst: Path, pbar: tqdm, block_size: int=1024) -> None:
		"""Copy a file from src to dst while updating a progress bar.

		:param src: source path
		:param dst: destination path
		:param pbar: progress bar
		:param block_size: how many bytes to copy between progress bar updates
		"""
		dst.parent.mkdir(parents=True, exist_ok=True)

		with open(src, 'rb') as fsrc:
			with open(dst, 'wb') as fdst:
				while True:
					chunk = fsrc.read(block_size)
					if not chunk:
						break
					fdst.write(chunk)
					# Update the global progress bar with the size of the chunk just written
					pbar.update(len(chunk))

		shutil.copystat(src, dst)


	@staticmethod
	def unrpa_generate_extractor(filename: str) -> Extractor:
		"""Get an extractor for an RPA archive.

		:param filename: RPA file to generate the extractor for
		:return: a dict with the extractor and supplementary data
		"""
		extractor = {"extractor": UnRPA(filename,0,"./02_Output_RPA",)}

		extractor["version"] = extractor["extractor"].detect_version()

		with open(extractor["extractor"].archive, "rb") as archive:
			extractor["index"] = extractor["extractor"].get_index(archive, extractor["version"])
			extractor["total_files"] = len(extractor["index"])
		return extractor

	@staticmethod
	def unrpa_extract(extractor: Extractor, pbar: tqdm) -> bool:
		"""Extract an RPA archive.

		:param extractor: dict with the extractor and supplementary data
		:param pbar: progress bar
		:return: True if extraction was successful, False otherwise
		"""
		if not Path(extractor["extractor"].path).is_dir():
			Logger.error("Output directory does not exist or is not a directory.")
			return False

		with open(extractor["extractor"].archive, "rb") as archive:
			for file_number, (path, data) in enumerate(extractor["index"].items()):
				try:
					display_name = path[-32:].ljust(32)
					pbar.set_postfix_str(display_name, refresh=False)

					extractor["extractor"].make_directory_structure(
						os.path.join(extractor["extractor"].path, os.path.split(path)[0])
					)

					file_view = extractor["extractor"].extract_file(
						path, data, file_number, extractor["total_files"], archive
					)

					with open(os.path.join(extractor["extractor"].path, path), "wb") as output_file:
						extractor["version"].postprocess(file_view, output_file)

					pbar.update(1)

				except:
					return False

		return True

	@staticmethod
	def remove_empty_dirs(root_path: Path) -> None:
		"""Remove empty subfolders of a directory.

		:param root_path: directory to remove empty subfolders from
		"""
		# glob('**') finds all subdirectories; sorted by length descending
		# ensures we process deepest directories first.
		for p in sorted(root_path.glob('**/*'), key=lambda x: len(str(x)), reverse=True):
			if p.is_dir():
				try:
					p.rmdir()  # Removes directory only if it is empty
				except OSError:
					pass  # Skip if directory is not empty

	@staticmethod
	def unrpyc_decompile(file: Path, pbar: tqdm) -> None:
		"""Decompile an RPYC file and update a progress bar.

		:param file: RPYC file to decompile
		:param pbar: progress bar
		"""
		display_name = file.name[-32:].ljust(32)
		pbar.set_postfix_str(display_name, refresh=False)
		unrpyc.decompile_rpyc(file, unrpyc.Context())
		pbar.update(1)

	@staticmethod
	def unrpyc_final_move(file_path: Path, root_dir: Path, pbar: tqdm) -> None:
		"""Move the decompiled files to the output directory.

		:param file_path: RPY file to move
		:param root_dir: root for constructing a relative path in the output directory
		:param pbar: progress bar
		"""
		relative_path = file_path.relative_to(root_dir)
		dest_dir = Path("./04_Output_RPYC")
		target_path = dest_dir / relative_path

		display_name = file_path.name[-32:].ljust(32)
		pbar.set_postfix_str(display_name, refresh=False)
		FileHelper.copy_with_pbar(file_path, target_path, pbar)

		file_path.unlink()
