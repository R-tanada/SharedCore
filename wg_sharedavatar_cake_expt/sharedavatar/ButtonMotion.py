import numpy as np
from loggle import logger

from . import RobotConfig as RC


class CrossButtonMotion:
    def __init__(self, button: str, distance: int, resolution: int):
        self.button = button
        self.distance = distance
        self.resolution = resolution

        self.s_flag = 0

        if self.button == "front":
            self.index = 0
            self.plus = True
        elif self.button == "back":
            self.index = 0
            self.plus = False
        elif self.button == "left":
            self.index = 1
            self.plus = True
        elif self.button == "right":
            self.index = 1
            self.plus = False
        elif self.button == "roll_plus":
            self.index = 5
            self.plus = False
        elif self.button == "roll_minus":
            self.index = 5
            self.plus = True
        elif self.button == "up":
            self.index = 2
            self.plus = True
        elif self.button == "down":
            self.index = 2
            self.plus = False

    def liner(self, data):
        if data:
            if data["data"]["Button"] == self.button:
                if self.s_flag == 0:
                    self.client_id = data["client_id"]
                    RC.robot_move_queue.put(
                        {
                            "type": "executed_command",
                            "message": data,
                            "resolution": self.resolution,
                            "distance": self.distance,
                            "robot_move": True,
                        }
                    )
                    self.s_flag = 1
                    linspace = np.linspace(-1, 1, int(self.resolution))
                    interval = [
                        i / 2 + np.sin(np.pi * i) / (2 * np.pi) for i in linspace
                    ]
                    interval = self.distance * np.abs(np.diff(interval))
                    self.move_iter = iter(interval)

        if self.s_flag == 1:
            try:
                if self.plus:
                    RC.pos[self.index] += next(self.move_iter)
                else:
                    RC.pos[self.index] -= next(self.move_iter)
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


class GripperMotion:
    gripper_active_flag = False
    alternative_flag = True
    get_cream_flag = False

    def __init__(
        self, button="button", distance=0, resolution=0, set_x=None, set_y=None
    ):
        self.button = button
        self.distance = distance
        self.resolution = resolution

        self.s_flag = 0

        self.force_threshold = 0.05
        self.cnt_over_force = 0

        self.start_x = set_x
        self.start_y = set_y

    def g_auto(self, data):
        if data:
            if not GripperMotion.get_cream_flag:
                if data["data"]["Button"] == self.button:
                    if self.s_flag == 0:
                        self.client_id = data["client_id"]
                        RC.robot_move_queue.put(
                            {
                                "type": "executed_command",
                                "message": data,
                                "alternative_flag": GripperMotion.alternative_flag,
                                "robot_move": True,
                            }
                        )
                        self.s_flag = 1

                        if GripperMotion.alternative_flag:
                            grip_state = {"Button": "grip", "state": 1}
                        else:
                            grip_state = {"Button": "grip", "state": 0}
                        RC.core.core_write_data("server-data", "grip-state", grip_state)

        if self.s_flag == 1:
            if GripperMotion.alternative_flag:
                RC.gripper_pos -= 0.5
                # print(RC.loadcell_val)
                if RC.loadcell_val > self.force_threshold:
                    self.cnt_over_force += 1

                if self.cnt_over_force == 10 or RC.gripper_pos <= RC.MIN_GRIPPER_POS:
                    self.s_flag = 0
                    self.cnt_over_force = 0
                    GripperMotion.alternative_flag = False
                    RC.robot_move_queue.put(
                        {
                            "type": "finished_command",
                            "message": self.button,
                            "client_id": self.client_id,
                            "alternative_flag": GripperMotion.alternative_flag,
                            "robot_move": False,
                        }
                    )

            else:
                RC.gripper_pos += 1

                if RC.gripper_pos >= 840:
                    self.s_flag = 0
                    GripperMotion.alternative_flag = True
                    RC.robot_move_queue.put(
                        {
                            "type": "finished_command",
                            "message": self.button,
                            "client_id": self.client_id,
                            "alternative_flag": GripperMotion.alternative_flag,
                            "robot_move": False,
                        }
                    )

    def g_cream(self, data):
        if data:
            if data["data"]["Button"] == self.button:
                if self.s_flag == 0:
                    self.s_flag = 1
                    grip_state = {"Button": "cream", "state": 1}
                elif self.s_flag == 1:
                    self.s_flag = 2
                    grip_state = {"Button": "cream", "state": 0}
                RC.core.core_write_data("server-data", "grip-state", grip_state)
                self.client_id = data["client_id"]
                if grip_state["state"] == 0:
                    RC.robot_move_queue.put(
                        {
                            "type": "executed_command",
                            "message": self.button,
                            "grip_state": grip_state,
                            "client_id": self.client_id,
                            "robot_move": True,
                        }
                    )
                elif grip_state["state"] == 1:
                    RC.robot_move_queue.put(
                        {
                            "type": "executed_command",
                            "message": data,
                            "grip_state": grip_state,
                            "robot_move": True,
                        }
                    )

        if self.s_flag == 1:
            if RC.gripper_pos >= RC.MIN_GRIPPER_POS:
                RC.gripper_pos -= 0.07

        elif self.s_flag == 2:
            RC.gripper_pos += 0.3
            if RC.loadcell_val <= self.force_threshold:
                self.s_flag = 0
                RC.robot_move_queue.put(
                    {
                        "type": "finished_command",
                        "message": self.button,
                        "client_id": self.client_id,
                        "grip_state": grip_state,
                        "robot_move": False,
                    }
                )

    def g_open(self, data):
        if data:
            if data["data"]["Button"] == self.button:
                if not GripperMotion.get_cream_flag:
                    if self.s_flag == 0:
                        self.s_flag = 1
                        grip_state = {"Button": "open", "state": 1}
                    elif self.s_flag == 1:
                        self.s_flag = 0
                        grip_state = {"Button": "open", "state": 0}
                    RC.core.core_write_data("server-data", "grip-state", grip_state)
                    self.client_id = data["client_id"]
                    if grip_state["state"] == 0:
                        RC.robot_move_queue.put(
                            {
                                "type": "executed_command",
                                "message": data,
                                "grip_state": grip_state,
                                "client_id": self.client_id,
                                "robot_move": False,
                            }
                        )
                    elif grip_state["state"] == 1:
                        RC.robot_move_queue.put(
                            {
                                "type": "executed_command",
                                "message": data,
                                "grip_state": grip_state,
                                "robot_move": True,
                            }
                        )

        if self.s_flag == 1:
            if RC.gripper_pos >= 840:
                self.s_flag = 0
                GripperMotion.alternative_flag = True
                grip_state = {"Button": "open", "state": 0}
                RC.core.core_write_data("server-data", "grip-state", grip_state)
                RC.robot_move_queue.put(
                    {
                        "type": "finished_command",
                        "message": self.button,
                        "client_id": self.client_id,
                        "grip_state": grip_state,
                        "robot_move": False,
                    }
                )
            else:
                RC.gripper_pos += 0.1
