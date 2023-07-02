from loggle import logger

from .ButtonMotion import CrossButtonMotion, GripperMotion
from .PointMotion import PointMotion
from .PositionMotion import PositionMotion
from . import RobotConfig as RC


class MotionControl:
    def __init__(self) -> None:
        self.s_front = "front"
        self.s_back = "back"
        self.s_right = "right"
        self.s_left = "left"
        self.s_roll_plus = "roll_plus"
        self.s_roll_minus = "roll_minus"
        self.s_up = "up"
        self.s_down = "down"
        self.s_grip = "grip"
        self.s_cream = "squeeze"
        self.s_open = "g_open"

        self.speed = 1.4

        self.pancake_button_motion = PointMotion("cake", 260, -200)
        self.fruit_button_motion = PointMotion("fruit", 260, 100)
        self.height_slider_motion = PointMotion("height_slider")

        self.position_motion = PositionMotion(
            80, 150 * 0.55, 150 * 0.45, 1300 / self.speed
        )

        self.mode = "liner"
        self.base_length = 40
        self.base_resolution = 600 / self.speed
        self.mc_front = CrossButtonMotion(
            self.s_front, distance=self.base_length, resolution=self.base_resolution
        )
        self.mc_back = CrossButtonMotion(
            self.s_back, distance=self.base_length, resolution=self.base_resolution
        )
        self.mc_right = CrossButtonMotion(
            self.s_right, distance=self.base_length, resolution=self.base_resolution
        )
        self.mc_left = CrossButtonMotion(
            self.s_left, distance=self.base_length, resolution=self.base_resolution
        )
        self.mc_roll_plus = CrossButtonMotion(
            self.s_roll_plus, distance=15, resolution=self.base_resolution
        )
        self.mc_roll_minus = CrossButtonMotion(
            self.s_roll_minus, distance=15, resolution=self.base_resolution
        )
        self.mc_up = CrossButtonMotion(
            self.s_up, distance=self.base_length * 0.5, resolution=self.base_resolution
        )
        self.mc_down = CrossButtonMotion(
            self.s_down,
            distance=self.base_length * 0.5,
            resolution=self.base_resolution,
        )
        self.grip = GripperMotion(
            button=self.s_grip,
            distance=self.base_length * 0.5,
            resolution=self.base_resolution,
        )
        self.cream = GripperMotion(
            button=self.s_cream,
            distance=self.base_length * 0.5,
            resolution=self.base_resolution,
        )
        self.open = GripperMotion(
            button=self.s_open,
            distance=self.base_length * 0.5,
            resolution=self.base_resolution,
        )

        self.cream_button_motion_1 = PointMotion(button="cream_1", set_x=410, set_y=280)
        self.cream_button_motion_2 = PointMotion(button="cream_2", set_x=410, set_y=380)

    def create_motion(self, data):
        if data:
            print(data)
        self.pancake_button_motion.set_point(data)
        self.fruit_button_motion.set_point(data)
        self.height_slider_motion.set_height_point(data)

        self.position_motion.calc_pos(data)

        RC.table_serial.write_signal(data)

        if self.mode == "liner":
            self.mc_front.liner(data)
            self.mc_back.liner(data)
            self.mc_right.liner(data)
            self.mc_left.liner(data)
            self.mc_roll_plus.liner(data)
            self.mc_roll_minus.liner(data)
            self.mc_up.liner(data)
            self.mc_down.liner(data)

        self.grip.g_auto(data)
        self.cream.g_cream(data)
        self.open.g_open(data)
        self.cream_button_motion_1.set_point_cream(data)
        self.cream_button_motion_2.set_point_cream(data)
