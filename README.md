# DeRenPy [![License](https://img.shields.io/github/license/J2bT/DeRenPy.svg)](https://github.com/J2bT/DeRenPy/blob/main/LICENSE)

A wrapper around "UnRPA" and "UnRPYC" open source utilities with a few other functions meant to speed up and simplify decompiling Ren'Py games.

Windows users can now download a compiled executable from the [releases page](https://github.com/J2bT/DeRenPy/releases/latest)! If you do, skip the "Getting Started" section. You will need to run this executable instead of `main.py`.

***

## Getting Started
**WARNING: Following instructions assume you have Python 3.9+ and Git installed!**

Start by cloning the repository with `git clone --recursive https://github.com/J2bT/DeRenPy`.

If the repository was cloned non-recursively previously, use `git submodule update --init` to clone the necessary submodules.

```bash
# 1. Change into the directory you cloned this repository to
cd DeRenPy

# IMPORTANT: If you're on Windows, replace `python3` with `py -3`!

# 2. Optional: Create and activate a virtualenv
python3 -m venv venv
# venv activation command differs depending on your OS/shell. DON'T run all of them.
# If there is no command for you below, a quick search should solve the issue.
source venv/bin/activate	# Bash
venv\Scripts\Activate.ps1	# Windows PowerShell
venv\Scripts\activate.bat	# Windows cmd.exe

# 3. Install the dependencies.
pip install -r requirements.txt

# 4. Linux-ONLY: make the `main.py` file executable
chmod a+x main.py
```

***

## Usage
DeRenPy has two modes of operation: interactive and pure CLI.

If you have created a venv during installation, make sure it is active before trying to run the project!

## Interactive mode
Just run the `main.py` file. (If this fails, run `python3 main.py` (Linux) or `py -3 main.py` (Windows) in your terminal of choice.)

If you did NOT create a venv during installation, just double-clicking on the file in your file explorer will likely work.

Note that interactive mode can't do some stuff pure CLI mode can. You can do everything, but with more steps involved. For example, you won't be able to decompress any RPA files that are not in the `01_Input_RPA` folder, so you'll have to pull them first.

![main-menu](assets/main-menu.png)

### Run RPA decompressor
![unrpa-1](assets/unrpa-1.png)

![unrpa-2](assets/unrpa-2.png)

### Run RPYC decompiler
![unrpyc-1](assets/unrpyc-1.png)

### Pull files from game folder
![pull-1](assets/pull-1.png)

![pull-2](assets/pull-2.png)

![pull-3](assets/pull-3.png)

### Move scripts from ./02_Output_RPA to their respective folders
![move-1](assets/move-1.png)

![move-2](assets/move-2.png)

### Clean all subfolders
![clean-1](assets/clean-1.png)

## Pure CLI mode
DeRenPy has a usage guide built-in. Just run it with the `-h` flag. The examples below do NOT showcase all the features.

```bash
# Decompress an RPA archive. Output will be in the `02_Output_RPA` folder.
main.py unrpa archive.rpa

# Decompress an RPYC compiled script. Output will be in the `04_Output_RPYC` folder.
main.py unrpyc script.rpyc

# Copy all RPA files from the game to `01_Input_RPA`. Can also copy RPYC (to `03_Input_RPYC`) or RPY (to `04_Output_RPYC`) files
main.py pull ~/Games/SomeVisualNovel rpa

# Move all RPYC files from `02_Output_RPA` to `03_Input_RPYC`. Can also move RPY files (to `04_Output_RPYC`) or both (to their respective folders).
main.py move rpyc

# Delete all files from `01_Input_RPA`, `02_Output_RPA`, `03_Input_RPYC` and `04_Output_RPYC` folders.
main.py clean
```

### `unrpa` subcommand
Usage: `main.py unrpa [-h] rpa_file [rpa_file ...]`.

If the RPA file is in the `01_Input_RPA` folder, path can be omitted. `.rpa` file extension can always be omitted.

Tip: running `main.py unrpa -h` will also show you the list of all RPA files in the `01_Input_RPA` folder.

### `unrpyc` subcommand
Usage: `main.py unrpyc [-h] [rpyc_file ...]`.

Running with no arguments will decompile all RPYC files in the `03_Input_RPYC` folder.

You can pass a directory instead of a specific file. Doing so will decompile all RPYC files in that directory.

If the RPYC file is in the `03_Input_RPYC` folder, path can be omitted. `.rpyc` file extension can always be omitted.

### `pull` subcommand
Usage: `main.py pull [-h] game_path [{rpa,rpyc,rpy}]`.

Running without specifying a file type will default to pulling RPA files.

### `move` subcommand
Usage: `main.py move [-h] [{both,rpyc,rpy}]`.

Running with no arguments will move both RPY and RPYC files to their respective folders.

### `clean` subcommand
Usage: `main.py clean [-h] [-y]`.

Running with the `-y` flag will skip the confirmation prompt.


## License and credits
- GPL-3.0 for this repository (see `LICENSE` file for more details).
- Credits to [UnRPA](https://github.com/Lattyware/unrpa/): this project wouldn't be possible without this wonderful utility.
	- UnRPA is licensed under GPL-3.0 (see `LICENSE` file for more details).
- Credits to [UnRPYC](https://github.com/CensoredUsername/unrpyc): this project wouldn't be possible without this wonderful utility.
	- UnRPYC is licensed under MIT License (see `lib/unrpyc/LICENSE` file for more details).
- Credits to [xaxa9551/De_RenPy](https://github.com/xaxa9551/De_RenPy) for the idea and inspiration.
- Credits to [Waydroid Extras Script](https://github.com/casualsnek/waydroid_script) for the idea and inspiration on the technical side of things, as well as being a wonderful example. This project's general structure heavily resembles <ins>Waydroid Extras Script</ins>. Before I stumbled onto this repo by accident, I wasn't even aware of the existence of `InquirerPy` and `tqdm` libraries, so when I saw what this script did, I wanted to use them too. I learned a lot from this repository. Thank you!
	- Waydroid Extras Script is licensed under GPL-3.0 (see `LICENSE` file for more details)
