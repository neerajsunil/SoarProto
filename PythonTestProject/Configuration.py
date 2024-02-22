"""""""""""""""""""""""""""""""""""""""""""""
Configuration.py

This file contains configuration constants for the TVCLabJack.py and LoadCell.py files.

Authors: Christopher Chan
"""""""""""""""""""""""""""""""""""""""""""""

# Defines
CALIBRATION_FILE = "calibration.json"
STAND_CONFIG_FILE = "config_stand.json"
DATA_CAPTURE_DIRECTORY = "captures"
DATA_CAPTURE_RATE = 2000 # Hz
DATA_CAPTURE_REFRESH_DELAY = 0.333 # Screen refresh delay in seconds
CALIBRATION_MENU_REFRESH_DELAY = 0.5 # Screen refresh delay in seconds
STREAM_RESOLUTION = 2   # 2 for 16-bit resolution
SCANS_PER_READ_DIVISOR = 2 # 2 for RATE/2 (1000) scans per read e.g. 500ms, 10 for 100ms
COM_PORT = "COM3"
DEFAULT_Z1 = 1.0
DEFAULT_Z2 = 1.0
DEFAULT_X1 = 1.0

# Vane Configuration
REPLAY_VANE_PROFILE = 0
VANE_PROFILE_DIFFERENTIAL_Z_FORCE = 20 # 20N Z force above first step

# Auto-generated Defines
DATA_CAPTURE_DELAY = 1/DATA_CAPTURE_RATE

# Configuration Maps
ANALOG_CHANNELS = {
    "LOAD_CELL_X" : "AIN0",
    "LOAD_CELL_Y" : "AIN1",
    "LOAD_CELL_Z" : "AIN2",
    "LOAD_CELL_T" : "AIN3",
}
RESOLUTION = { # Ignored in Stream Mode (STREAM_RESOLUTION) used above
    # Note: Use the ResolutionSelector10V class from T7Constants.py to select the resolution index
    "AIN0" : 2,
    "AIN1" : 2,
    "AIN2" : 2,
    "AIN3" : 2,
}

# Auto-generated Configuration
ANALOG_TO_NAME = {v: k for k, v in ANALOG_CHANNELS.items()}

# Constant Unit Mappings
FORCE_UNITS = {
    "Fx" : "N",
    "Fy" : "N",
    "Fz" : "N",
    "Mx" : "Nm",
    "My" : "Nm",
    "Mz" : "Nm"
}