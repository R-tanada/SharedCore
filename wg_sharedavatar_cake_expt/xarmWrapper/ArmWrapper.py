import threading
import time

from sharedavatar import RobotConfig as RC
from xarm import XArmAPI


class ArmWrapper:
    def __init__(self, enable, armIP=None):
        if enable:
            self.arm = XArmAPI(armIP)

            self.__connect_arm()
            self.initialize_arm()
            self.__loadcell_setup()

    def __connect_arm(self):
        self.arm.connect()
        if self.arm.warn_code != 0:
            self.arm.clean_warn()
        if self.arm.error_code != 0:
            self.arm.clean_error()

    def initialize_arm(self):
        self.arm.motion_enable(enable=True)
        self.arm.set_mode(0)
        self.arm.set_state(state=0)
        self.arm.set_position(
            x=RC.INIT_X,
            y=RC.INIT_Y,
            z=RC.INIT_Z,
            roll=RC.INIT_ROLL,
            pitch=RC.INIT_PITCH,
            yaw=RC.INIT_YAW,
        )

        self.arm.set_tgpio_modbus_baudrate(2000000)
        self.arm.set_gripper_mode(0)
        self.arm.set_gripper_enable(enable=True)
        self.arm.set_gripper_position(RC.INIT_GRIPPER_POS, speed=5000)

        self.arm.motion_enable(enable=True)
        self.arm.set_mode(1)
        self.arm.set_state(state=0)

    def send_data_to_robot(self):
        self.arm.set_servo_cartesian(RC.pos)
        self.arm.getset_tgpio_modbus_data(self.convert_to_modbus_data(RC.gripper_pos))

    def limitation_pos(self):

        if RC.pos[0] > RC.MAX_X:
            RC.pos[0] = RC.MAX_X
        elif RC.pos[0] < RC.MIN_X:
            RC.pos[0] = RC.MIN_X

        if RC.pos[1] > RC.MAX_Y:
            RC.pos[1] = RC.MAX_Y
        elif RC.pos[1] < RC.MIN_Y:
            RC.pos[1] = RC.MIN_Y

        if RC.pos[2] > RC.MAX_Z:
            RC.pos[2] = RC.MAX_Z
        elif RC.pos[2] < RC.MIN_Z:
            RC.pos[2] = RC.MIN_Z

    def convert_to_modbus_data(self, value: int):
        if int(value) <= 255 and int(value) >= 0:
            dataHexThirdOrder = 0x00
            dataHexAdjustedValue = int(value)

        elif int(value) > 255 and int(value) <= 511:
            dataHexThirdOrder = 0x01
            dataHexAdjustedValue = int(value) - 256

        elif int(value) > 511 and int(value) <= 767:
            dataHexThirdOrder = 0x02
            dataHexAdjustedValue = int(value) - 512

        elif int(value) > 767 and int(value) <= 1123:
            dataHexThirdOrder = 0x03
            dataHexAdjustedValue = int(value) - 768

        modbus_data = [0x08, 0x10, 0x07, 0x00, 0x00, 0x02, 0x04, 0x00, 0x00]
        modbus_data.append(dataHexThirdOrder)
        modbus_data.append(dataHexAdjustedValue)

        return modbus_data

    def __loadcell_setup(self):
        self.init_loadcell_val = self.arm.get_cgpio_analog(0)[1]
        self.loadcell_thr = threading.Thread(
            target=self.__get_loadcell_val, daemon=True
        )
        self.loadcell_thr.start()

    def __get_loadcell_val(self):
        while True:
            try:
                RC.loadcell_val = (
                    self.arm.get_cgpio_analog(0)[1] - self.init_loadcell_val
                )
                time.sleep(0.01)
            except:
                RC.loadcell_val = 0
