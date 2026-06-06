from pathlib import Path
import sys


# Add submodule root to sys.path
submodule_root = Path(__file__).parent /  "unrpyc"
sys.path.insert(0, str(submodule_root.resolve()))
