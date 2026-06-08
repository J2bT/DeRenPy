from pathlib import Path
import sys


# Add submodule root to sys.path
base_path = Path(sys._MEIPASS) if getattr(sys, 'frozen', False) else Path(__file__).resolve().parent
unrpyc_path = base_path / "unrpyc"
sys.path.insert(0, str(unrpyc_path))
