import numpy as np
from loggle import logger

from . import RobotConfig as RC


class PositionMotion:
    def __init__(self, s, p, q, resolution):
        self.s = s
        self.p = p
        self.q = q

        self.resolution = resolution
        self.s_flag = 0

    def calc_pos(self, data):
        if data:
            if data["data"]["Button"] == "micro":
                self.per_x = data["data"]["bool"][0]
                self.per_y = data["data"]["bool"][1]

                if self.s_flag == 0:
                    self.s_flag = 1
                    self.client_id = data["client_id"]
                    RC.robot_move_queue.put(
                        {
                            "type": "executed_command",
                            "message": data,
                            "robot_move": True,
                        }
                    )

                    height_correction = 0.8 * RC.pos[2] / (RC.INIT_Z - RC.MIN_Z)

                    _s = self.s * height_correction
                    _p = self.p * height_correction
                    _q = self.q * height_correction

                    a = _s * self.per_x

                    if self.per_y >= 0:
                        b = _p * self.per_y
                    else:
                        b = _q * self.per_y

                    r = np.sqrt(a**2 + b**2)
                    delta = np.arctan2(b, a)

                    A = r * np.cos(delta + np.radians(RC.pos[5]))
                    B = r * np.sin(delta + np.radians(RC.pos[5]))

                    linspace = np.linspace(-1, 1, int(self.resolution))
                    interval = [
                        i / 2 + np.sin(np.pi * i) / (2 * np.pi) for i in linspace
                    ]

                    interval_list_x = B * np.abs(np.diff(interval))
                    interval_list_y = A * np.abs(np.diff(interval))

                    interval_xy = list(zip(interval_list_x, interval_list_y))

                    self.move_iter = iter(interval_xy)

        if self.s_flag == 1:
            try:
                diff = next(self.move_iter)
                RC.pos[0] += diff[0]
                RC.pos[1] -= diff[1]
            except StopIteration:
                self.s_flag = 0
                RC.robot_move_queue.put(
                    {
                        "type": "finished_command",
                        "message": {"x": self.per_x, "y": self.per_y},
                        "client_id": self.client_id,
                        "robot_move": False,
                    }
                )
