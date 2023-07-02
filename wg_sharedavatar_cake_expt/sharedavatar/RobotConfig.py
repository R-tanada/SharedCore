import json
from queue import Queue

settings = json.load(open("config/settings.json"))

core = None

INIT_X = settings["RobotConfig"]["INIT_X"]
INIT_Y = settings["RobotConfig"]["INIT_Y"]
INIT_Z = settings["RobotConfig"]["INIT_Z"]
INIT_ROLL = settings["RobotConfig"]["INIT_ROLL"]
INIT_PITCH = settings["RobotConfig"]["INIT_PITCH"]
INIT_YAW = settings["RobotConfig"]["INIT_YAW"]
MAX_X = settings["RobotConfig"]["MAX_X"]
MAX_Y = settings["RobotConfig"]["MAX_Y"]
MAX_Z = settings["RobotConfig"]["MAX_Z"]
MIN_X = settings["RobotConfig"]["MIN_X"]
MIN_Y = settings["RobotConfig"]["MIN_Y"]
MIN_Z = settings["RobotConfig"]["MIN_Z"]
INIT_GRIPPER_POS = settings["RobotConfig"]["INIT_GRIPPER_POS"]
MIN_GRIPPER_POS = settings["RobotConfig"]["MIN_GRIPPER_POS"]

SET_Z = settings["RobotConfig"]["SET_Z"]
CREAM_Z_GRIP = settings["RobotConfig"]["CREAM_Z_GRIP"]
CREAM_Z_UP = settings["RobotConfig"]["CREAM_Z_UP"]

pos = [INIT_X, INIT_Y, INIT_Z, INIT_ROLL, INIT_PITCH, INIT_YAW]
gripper_pos = INIT_GRIPPER_POS
loadcell_val = 0

robot_move_queue = Queue()

table_serial = None
