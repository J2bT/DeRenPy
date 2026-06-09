#!/usr/bin/env python3

# DeRenPy
#
# Copyright (C) 2026  J2bT
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import argparse
import os
from pathlib import Path
from sys import exit

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from InquirerPy.validator import PathValidator
from tqdm import tqdm

# noinspection PyUnusedImports
import lib.pathhack	# This MUST happen before importing lib.filehelper
from lib.filehelper import FileHelper
from lib.logger import Logger


def pause() -> None:
	"""Pause the application until Enter is pressed."""
	Logger.info("Press Enter to return to the main menu.")
	input()


def run_unrpa(args: argparse.Namespace) -> None:
	"""Unpack all RPA archives provided by the user.

	Expects:
		`args.files`: list of file paths (in strings)
	"""
	args.files = set(args.files)

	args.files = [f.strip() for f in args.files]

	for i in range(len(args.files)):
		if os.path.isabs(args.files[i]):
			if not os.path.isfile(args.files[i]):
				if not os.path.isfile(args.files[i] + ".rpa"):
					Logger.error(f"No such file: “{args.files[i]}”.")
					return
				else:
					args.files[i] = args.files[i] + ".rpa"
		else:   # Relative path
			if not os.path.isfile(args.files[i]):
				if not os.path.isfile(args.files[i] + ".rpa"):
					if not os.path.isfile("./01_Input_RPA/" + args.files[i]):
						if not os.path.isfile("./01_Input_RPA/" + args.files[i] + ".rpa"):
							display_name = args.files[i] if args.files[i].endswith(".rpa") else args.files[i] + ".rpa"
							Logger.error(f"No such file: “{display_name}”.")
							return
						else:   # Found the file in ./01_Input_RPA (.rpa was omitted)
							args.files[i] = "./01_Input_RPA/" + args.files[i] + ".rpa"
					else:   # Found the file in ./01_Input_RPA
						args.files[i] = "./01_Input_RPA/" + args.files[i]
				else:
					args.files[i] = args.files[i] + ".rpa"

	extractors = [FileHelper.unrpa_generate_extractor(filename) for filename in args.files]

	total_files = 0

	for extractor in extractors:
		total_files += extractor["total_files"]

	with tqdm(total=total_files, unit="files") as pbar:
		for extractor in extractors:
			pbar.write(f"Extracting: {extractor["extractor"].archive}")
			if not FileHelper.unrpa_extract(extractor, pbar):   # Note: Condition with a side effect
				Logger.error("Extraction failed.")
				return


def run_unrpyc(args: argparse.Namespace) -> None:
	"""Decompile all RPYC files provided by the user.

	Expects:
		`args.files`: one of:
			- A list of paths (in strings) to one of:
				- RPYC files to decompile
				- A directory with RPYC files to decompile
			- An empty list (will default to "['./03_Input_RPYC']")
	"""
	if len(args.files) == 0:
		args.files.append("./03_Input_RPYC")

	args.files = [f.strip() for f in args.files]

	files_to_process = {}
	for path in args.files:
		input_path = Path(path)

		# Case 1: Input is a Directory
		if input_path.is_dir():
			for f in input_path.rglob("*.rpyc"):
				if f.is_file():
					files_to_process[f.resolve()] = input_path.resolve()
			continue

		# Case 2: Input is a File
		candidates = [
			input_path,
			input_path.with_suffix(".rpyc"),
			Path("./03_Input_RPYC") / input_path,
			Path("./03_Input_RPYC") / input_path.with_suffix(".rpyc")
		]

		resolved_file = None
		for candidate in candidates:
			if candidate.is_file():
				resolved_file = candidate.resolve()
				break

		if resolved_file:
			files_to_process[resolved_file] = input_path.parent
		else:
			display_name = path if path.endswith(".rpyc") else path + ".rpyc"
			Logger.error(f"No such file: '{display_name}'.")
			return

	if len(files_to_process) == 0:
		Logger.error(f"No files to process.")
		return

	with tqdm(total=len(files_to_process), unit="files") as pbar:
		for file_path in files_to_process.keys():
			FileHelper.unrpyc_decompile(file_path, pbar)

	Logger.info("Decompilation finished, moving decompiled files to the output folder.")

	files_to_process = {file_path.with_suffix(".rpy"): source_dir for file_path, source_dir in files_to_process.items()}

	total_size = sum(f.stat().st_size for f in files_to_process.keys())
	with tqdm(total=total_size, unit="iB", unit_scale=True, desc="Moving", unit_divisor=1024) as pbar:
		for file_path, source_dir in files_to_process.items():
			if not file_path.exists():
				Logger.warning(f"File does not exist: {file_path}, skipping...")
				return

			FileHelper.unrpyc_final_move(file_path, source_dir, pbar)


def run_pull(args: argparse.Namespace) -> None:
	"""Copy game files of a specified type to the appropriate input/output folder.

	Expects:
		`args.game_path`: path (in a string) to one of:
			- The root directory of a Ren'Py game
			- `/game` subfolder of a Ren'Py game
		`args.file_type`: one of:
			- 'rpa'
			- 'rpyc'
			- 'rpy'
	"""
	# Get a Path object pointing to /game subfolder
	game_path = FileHelper.get_game_directory(args.game_path.strip())

	if game_path is None:
		return

	Logger.info(f"Game folder found: {game_path}")

	if args.file_type == "rpa":
		dest_dir = Path("./01_Input_RPA")
	elif args.file_type == "rpyc":
		dest_dir = Path("./03_Input_RPYC")
	else:   #if args.file_type == "rpy"
		dest_dir = Path("./04_Output_RPYC")

	file_pattern = "*." + args.file_type

	files_to_copy = [f for f in game_path.rglob(file_pattern) if f.is_file()]

	if len(files_to_copy) == 0:
		Logger.error(f"No {args.file_type} files found in the provided game path.")
		return

	total_size = sum(f.stat().st_size for f in files_to_copy)

	with tqdm(total=total_size, unit="iB", unit_scale=True, desc="Copying", unit_divisor=1024) as pbar:
		for file_path in files_to_copy:
			relative_path = file_path.relative_to(game_path)
			target_path = dest_dir / relative_path

			display_name = file_path.name[-32:].ljust(32)
			pbar.set_postfix_str(display_name, refresh=False)
			FileHelper.copy_with_pbar(file_path, target_path, pbar)


def run_move(args: argparse.Namespace) -> None:
	"""Move script files from the `02_Output_RPA` folder to their appropriate folder.

	Expects:
	 	`args.file_type`: one of:
			- 'rpy'
			- 'rpyc'
			- 'both'
	"""
	if args.file_type == "both":
		extensions = {".rpy", ".rpyc"}
	else:
		extensions = {"." + args.file_type}

	src_dir = Path("./02_Output_RPA")

	files_to_copy = [f for f in src_dir.rglob("*") if f.is_file() and f.suffix in extensions]

	if len(files_to_copy) == 0:
		Logger.error(
			f"No {args.file_type if args.file_type != "both" else "script"} files found in ./02_Output_RPA.")
		return

	total_size = sum(f.stat().st_size for f in files_to_copy)

	with tqdm(total=total_size, unit="iB", unit_scale=True, desc="Moving", unit_divisor=1024) as pbar:
		for file_path in files_to_copy:
			relative_path = file_path.relative_to(src_dir)
			dest_dir = Path("./03_Input_RPYC") if file_path.suffix == ".rpyc" else Path("./04_Output_RPYC")
			target_path = dest_dir / relative_path

			display_name = file_path.name[-32:].ljust(32)
			pbar.set_postfix_str(display_name, refresh=False)
			FileHelper.copy_with_pbar(file_path, target_path, pbar)

			file_path.unlink()

	FileHelper.remove_empty_dirs(src_dir)


def run_clean(args: argparse.Namespace) -> None:
	"""Delete all files from the application's input/output directories.

	Expects:
		`args.assume_yes`: boolean value determining whether to prompt the user for confirmation
	"""
	if not args.assume_yes:
		Logger.warning(
			"You are about to delete all files in the following folders:\n"
			"./01_Input_RPA\n"
			"./02_Output_RPA\n"
			"./03_Input_RPYC\n"
			"./04_Output_RPYC\n")

		if not inquirer.confirm(message="Are you sure you want to proceed?").execute():
			Logger.info("Clean cancelled. Aborting...")
			return

	FileHelper.nukedirs()
	FileHelper.makedirs()

	Logger.info("Clean finished.")


def interact(args: argparse.Namespace) -> None:
	"""Launch the interactive mode of the application."""

	os.system("cls" if os.name == "nt" else "clear")

	args.command = inquirer.select(
		message="Select an action",
		instruction="([\u2191\u2193]: Select Item)",
		choices=[
			Choice(name="Run RPA decompressor", value="unrpa"),
			Choice(name="Run RPYC decompiler", value="unrpyc"),
			Separator(),
			Choice(name="Pull files from game folder", value="pull"),
			Choice(name="Move scripts from ./02_Output_RPA to their respective folders", value="move"),
			Choice(name="Clean all subfolders", value="clean"),
			Separator(),
			Choice(name="Exit", value=None)
		],
		default="unrpa",
	).execute()
	if args.command is None:
		exit()

	if args.command == "unrpa":
		rpa_list = FileHelper.rpa_list()

		if len(rpa_list) == 0:
			Logger.error("No RPA files in the input directory. Pull them before selecting this option.")
			return

		args.files = inquirer.checkbox(
			message="Select files to decompress",
			instruction="([\u2191\u2193]: Select Item. [Space]: Toggle Choice, [Enter]: Confirm)",
			validate=lambda result: len(result) >= 1,
			invalid_message="select at least one item to decompress",
			choices=rpa_list
		).execute() if len(rpa_list) > 1 else rpa_list

		run_unrpa(args)

	elif args.command == "unrpyc":
		args.files = ["./03_Input_RPYC"]
		run_unrpyc(args)

	elif args.command == "pull":
		args.file_type = inquirer.select(
			message="Select which files to pull",
			instruction="([\u2191\u2193]: Select Item)",
			choices=["rpa", "rpyc", "rpy"],
		).execute()

		args.game_path = inquirer.filepath(
			message="Input the path to the game folder",
			validate=PathValidator(is_dir=True, message="input is not a directory"),
			only_directories=True,
		).execute()

		run_pull(args)

	elif args.command == "move":
		args.file_type = inquirer.select(
			message="Select which files to move",
			instruction="([\u2191\u2193]: Select Item)",
			choices=["both", "rpyc", "rpy"],
		).execute()

		run_move(args)

	elif args.command == "clean":
		args.assume_yes = False
		run_clean(args)


def main() -> None:
	"""Entry point of the application."""

	parser = argparse.ArgumentParser(description='''
	DeRenPy, a Ren'Py decompiler wrapper.
	Use -h flag for help!''')

	subparsers = parser.add_subparsers(title="command", dest='command')

	unrpa_help = "File to decompress. If the file is in ./01_Input_RPA, path can be omitted. '.rpa' can be omitted.\n\n"
	unrpa_help += "List of .rpa files in ./01_Input_RPA:\n"
	unrpa_help += "\n".join(FileHelper.rpa_list())

	rpa_deco = subparsers.add_parser(
		"unrpa", formatter_class=argparse.RawTextHelpFormatter, help="Run RPA decompiler")
	rpa_deco.add_argument(
		dest="files",
		nargs="+",
		metavar="rpa_file",
		help=unrpa_help
	)
	rpa_deco.set_defaults(func=run_unrpa)

	rpyc_deco = subparsers.add_parser(
		"unrpyc", help="Run RPYC decompiler")
	rpyc_deco.add_argument(
		dest="files",
		nargs="*",
		metavar="rpyc_file",
		help="File(s) to decompile. If the file is in ./03_Input_RPYC, path can be omitted. '.rpyc' can be omitted. "
			 "Can be a directory (equivalent to passing all its .rpyc files). "
			 "(default: './03_Input_RPYC')"
	)
	rpyc_deco.set_defaults(func=run_unrpyc)

	pull = subparsers.add_parser(
		"pull", help="Copy files from game folder")
	pull.add_argument(
		"game_path", help="Path to the game to pull from")
	pull.add_argument("file_type",
					  nargs="?",
					  help="Type of files to pull (default: rpa)",
					  default="rpa",
					  choices=["rpa", "rpyc", "rpy"])
	pull.set_defaults(func=run_pull)

	move = subparsers.add_parser(
		"move",
		help="Move scripts from ./02_Output_RPA to ./03_Input_RPYC (*.rpyc) and ./04_Output_RPYC (*.rpy)")
	move.add_argument("file_type",
					  nargs="?",
					  help="Type of files to move (default: both)",
					  default="both",
					  choices=["both", "rpyc", "rpy"])
	move.set_defaults(func=run_move)

	clean = subparsers.add_parser(
		"clean", help="Clean all subfolders")
	clean.add_argument("-y", "--assumeyes",
					   dest="assume_yes",
					   help="Don't prompt for confirmation",
					   action='store_true')
	clean.set_defaults(func=run_clean)

	args = parser.parse_args()
	FileHelper.makedirs()
	if hasattr(args, 'func'):
		args.func(args)
	else:
		while True:
			args = argparse.Namespace()
			interact(args)
			pause()


if __name__ == "__main__":
	main()
