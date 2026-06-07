# DeRenPy [![License](https://img.shields.io/github/license/J2bT/DeRenPy.svg)](https://github.com/J2bT/DeRenPy/blob/main/LICENSE)

A wrapper around "UnRPA" and "UnRPYC" open source utilities with a few other functions meant to speed up and simplify decompiling Ren'Py games.

***

## Getting Started
**WARNING: Following instructions assume you have Python 3 and Git installed!**

Start by cloning the repository with `git clone --recursive https://github.com/J2bT/DeRenPy`.

If the repository was cloned non-recursively previously, use `git submodule update --init` to clone the necessary submodules.

```bash
# 1. Change into the directory you cloned this repository to
cd DeRenPy

# IMPORTANT: If you're on Windows, replace all mentions of `python3` with `py -3`!

# 2. Optional: Create and activate a virtualenv
python3 -m venv venv
# venv activation command differs depending on your OS/shell. DON'T run all of them.
# If there is no command for you below, a quick search should solve the issue.
source venv/bin/activate	# Bash
venv\Scripts\Activate.ps1	# Windows PowerShell
venv\Scripts\activate.bat	# Windows cmd.exe

# 3. Install the dependencies.
pip install -r requirements.txt
```

***

## Usage
DeRenPy has two modes of operation: interactive and pure CLI.

### Interactive mode
Just run `python3 main.py` (or `py -3 main.py` for Windows). If you have created venv during installation, make sure it is active!

### Pure CLI mode
Coming soon...


## License and credits
- GPL-3.0 for this repository (see `LICENSE` file for more details).
- Credits to [UnRPA](https://github.com/Lattyware/unrpa/): this project wouldn't be possible without this wonderful utility.
	- UnRPA is licensed under GPL-3.0 (see `LICENSE` file for more details).
- Credits to [UnRPYC](https://github.com/CensoredUsername/unrpyc): this project wouldn't be possible without this wonderful utility.
	- UnRPYC is licensed under MIT License (see `lib/unrpyc/LICENSE` file for more details).
- Credits to [xaxa9551/De_RenPy](https://github.com/xaxa9551/De_RenPy) for the idea and inspiration.
- Credits to [Waydroid Extras Script](https://github.com/casualsnek/waydroid_script) for the idea and inspiration on the technical side of things, as well as being a wonderful example. This project's general structure heavily resembles <ins>Waydroid Extras Script</ins>. Before I stumbled onto this repo by accident, I wasn't even aware of the existence of `InquirerPy` and `tqdm` libraries, so when I saw what this script did, I wanted to use them too. I learned a lot from this repository. Thank you!
	- Waydroid Extras Script is licensed under GPL-3.0 (see `LICENSE` file for more details)
