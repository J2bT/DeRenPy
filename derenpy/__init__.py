import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
UNRPYC_DIR = ROOT / "unrpyc"


if str(UNRPYC_DIR) not in sys.path:
    sys.path.insert(0, str(UNRPYC_DIR))

__version__ = "0.1.0"
