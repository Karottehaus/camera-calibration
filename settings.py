from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

CAMERA_POSITION = DATA_DIR / "camera_position.csv"

# camera calibration parameters

# number of spatial pixels of the line scanner
SPATIAL_PIXEL = 1312
# time required [ms] for the scanner to transfer the captured frame to the PC
FTT = 3.4

ARROW_DISTANCE = 24.1
MAX_SCAN_LENGTH = 1500
