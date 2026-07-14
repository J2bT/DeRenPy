import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UNRPYC_DIR = ROOT / "derenpy" / "unrpyc"


if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
    
if str(UNRPYC_DIR) not in sys.path:
    sys.path.insert(0, str(UNRPYC_DIR))
