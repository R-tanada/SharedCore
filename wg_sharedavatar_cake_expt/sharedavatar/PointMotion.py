import numpy as np
from loggle import logger

from . import RobotConfig as RC


class PointMotion:
    grip_state = "open"

    def __init__(self, button, set_x=None, set_y=None):
        self.button = button
        self.set_x = set_x
        self.set_y = set_y
        self.set_z = RC.SET_Z
        self.cream_pos_list = []
        self.move_count = 0
        self.cream_number = 4

        if "cream" in self.button:
            for i in range(self.cream_number):
                self.cream_pos_list.append(self.set_x - (i * 60))

        self.resolution = 1500

        self.s_flag = 0

    def set_point(self, data):
        if data:
            if data["data"]["Button"] == self.button:
                if self.s_flag == 0:
                    self.s_flag = 1
                    self.client_id = data["client_id"]
                    RC.robot_move_queue.put(
                        {
                            "type": "executed_command",
                            "message": data,
                            "resolution": self.resolution,
                            "robot_move": True,
                        }
                    )
                    distance_x = self.set_x - RC.pos[0]
                    distance_y = self.set_y - RC.pos[1]
                    distance_z = self.set_z - RC.pos[2]

                    linspace = np.linspace(-1, 1, int(self.resolution))
                    interval = [
                        i / 2 + np.sin(np.pi * i) / (2 * np.pi) for i in linspace
                    ]

                    interval_x = distance_x * np.abs(np.diff(interval))
                    interval_y = distance_y * np.abs(np.diff(interval))
                    interval_z = distance_z * np.abs(np.diff(interval))
                    self.move_iter_x = iter(interval_x)
                    self.move_iter_y = iter(interval_y)
                    self.move_iter_z = iter(interval_z)

        if self.s_flag == 1:
            try:
                diff_z = next(self.move_iter_z)
                RC.pos[2] += diff_z
            except StopIteration:
                pass
            try:
                diff_x = next(self.move_iter_x)
                diff_y = next(self.move_iter_y)
                RC.pos[0] += diff_x
                RC.pos[1] += diff_y
            except StopIteration:
                self.s_flag = 0
                RC.robot_move_queue.put(
                    {
                        "type": "finished_command",
                        "message": self.button,
                        "client_id": self.client_id,
                        "robot_move": False,
                    }
                )

    def set_height_point(self, data):
        if data:
            if data["data"]["Button"] == self.button:
                if self.s_flag == 0:
                    self.client_id = data["client_id"]
                    RC.robot_move_queue.put(
                        {
                            "type": "executed_command",
                            "message": data,
                            "resolution": self.resolution,
                            "robot_move": True,
                        }
                    )
                    height_data = data["data"]["bool"]
                    target_z = height_data * (RC.MAX_Z - RC.MIN_Z) / 100 + RC.MIN_Z
                    distance_z = target_z - RC.pos[2]

                    linspace = np.linspace(-1, 1, int(self.resolution))
                    interval = [
                        i / 2 + np.sin(np.pi * i) / (2 * np.pi) for i in linspace
                    ]

                    interval_z = distance_z * np.abs(np.diff(interval))
                    self.move_iter_z = iter(interval_z)
                    self.s_flag = 1
        if self.s_flag == 1:
            try:
                diff_z = next(self.move_iter_z)
                RC.pos[2] += diff_z
            except StopIteration:
                self.s_flag = 0
                RC.robot_move_queue.put(
                    {
                        "type": "finished_command",
                        "message": self.button,
                        "client_id": self.client_id,
                        "robot_move": False,
                    }
                )

    def set_point_cream(self, data):
        if data:
            if data["data"]["Button"] == self.button:
                if self.s_flag == 0:
                    self.s_flag = 1
                    self.client_id = data["client_id"]
                    RC.robot_move_queue.put(
                        {
                            "type": "executed_command",
                            "message": data,
                            "count": self.move_count,
                            "grip_state": PointMotion.grip_state,
                            "robot_move": True,
                        }
                    )
                    RC.core.core_write_data(
                        "server-data",
                        "pickup_cream",
                        {"Button": self.button, "state": PointMotion.grip_state},
                    )
                    self.set_x = self.cream_pos_list[self.move_count]
                    distance_x = self.set_x - RC.pos[0]
                    distance_y = self.set_y - RC.pos[1]
                    distance_z = RC.CREAM_Z_UP - RC.pos[2]
                    distance_z_grip = RC.CREAM_Z_GRIP - RC.CREAM_Z_UP
                    distance_z_up = RC.CREAM_Z_UP - RC.CREAM_Z_GRIP

                    linspace = np.linspace(-1, 1, int(self.resolution))
                    interval = [
                        i / 2 + np.sin(np.pi * i) / (2 * np.pi) for i in linspace
                    ]

                    interval_x = distance_x * np.abs(np.diff(interval))
                    interval_y = distance_y * np.abs(np.diff(interval))
                    interval_z = distance_z * np.abs(np.diff(interval))
                    interval_z_grip = distance_z_grip * np.abs(np.diff(interval))
                    interval_z_up = distance_z_up * np.abs(np.diff(interval))
                    self.move_iter_x = iter(interval_x)
                    self.move_iter_y = iter(interval_y)
                    self.move_iter_z = iter(interval_z)
                    self.move_iter_z_grip = iter(interval_z_grip)
                    self.move_iter_z_up = iter(interval_z_up)

                    if PointMotion.grip_state == "open":
                        RC.gripper_pos = 850

                    self.diff_grip = 0.5
                    self.cream_threshold = 0.03

        if self.s_flag == 1:
            try:
                diff_x = next(self.move_iter_x)
                diff_y = next(self.move_iter_y)
                diff_z = next(self.move_iter_z)
                RC.pos[0] += diff_x
                RC.pos[1] += diff_y
                RC.pos[2] += diff_z
            except StopIteration:
                self.s_flag = 2

        elif self.s_flag == 2:
            try:
                diff_z_grip = next(self.move_iter_z_grip)
                RC.pos[2] += diff_z_grip
            except StopIteration:
                self.s_flag = 3

        elif self.s_flag == 3:
            if PointMotion.grip_state == "open":
                RC.gripper_pos -= self.diff_grip
                if RC.loadcell_val > self.cream_threshold or RC.gripper_pos < 300:
                    self.s_flag = 4
                    PointMotion.grip_state = "grip"
            elif PointMotion.grip_state == "grip":
                RC.gripper_pos += self.diff_grip
                if RC.gripper_pos >= 840:
                    self.s_flag = 4
                    self.move_count += 1
                    if self.move_count == self.cream_number:
                        self.move_count = 0
                    PointMotion.grip_state = "open"

        if self.s_flag == 4:
            try:
                diff_z_up = next(self.move_iter_z_up)
                RC.pos[2] += diff_z_up
            except StopIteration:
                self.s_flag = 0
                if PointMotion.grip_state == "open":
                    RC.core.core_write_data(
                        "server-data",
                        "pickup_cream",
                        {"Button": self.button, "state": None},
                    )
                RC.robot_move_queue.put(
                    {
                        "type": "finished_command",
                        "message": self.button,
                        "client_id": self.client_id,
                        "count": self.move_count,
                        "grip_state": PointMotion.grip_state,
                        "robot_move": False,
                    }
                )
