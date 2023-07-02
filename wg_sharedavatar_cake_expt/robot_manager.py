import datetime
import pickle
import socket
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

import loggle
from corepy import CoreServer
from loggle import logger
from sharedavatar import RobotConfig as RC
from sharedavatar import *
from udppy import UDP_Server
from visualFB.VisualFB import VisualSerailFB
from xarmWrapper import ArmWrapper


class CoreServer(CoreServer):
    def __init__(self, server_ip: str, services: list, base_alias: str):
        super().__init__(server_ip, services, base_alias)
        self.queue = Queue()

    def on_resource_frame_arrived(self, type, resource, channel, frame):
        super().on_resource_frame_arrived(type, resource, channel, frame)
        if type == "data":
            self.on_data_frame_arrived(resource, channel, self.receive_data)

    def on_data_frame_arrived(self, resource, channel, frame):
        logger.info(frame)
        if "client-data" in resource:
            if channel == "command":
                self.queue.put(frame)
                logger.info({"type": "received_command", "message": frame})
            elif channel == "cursor":
                self.core_write_data(
                    "server-data",
                    "cursor",
                    {
                        "user": frame["client_id"],
                        "x": frame["data"]["x"],
                        "y": frame["data"]["y"],
                    },
                )
                logger.info({"type": "cursor", "message": frame})
            elif channel == "cursor-pressed":
                self.core_write_data(
                    "server-data",
                    "cursor-pressed",
                    {"user": frame["client_id"], "pressed": frame["data"]["pressed"]},
                )
                logger.info({"type": "cursor_pressed", "message": frame})
            elif channel == "button-state":
                self.core_write_data(
                    "server-data",
                    "button-state",
                    {"user": frame["client_id"], "state": frame["data"]["state"]},
                )
                logger.info({"type": "button_state", "message": frame})


def __set_core_thr():
    RC.core = CoreServer(
        server_ip=RC.settings["CoreSDK"]["SERVER_IP"],
        services=[
            "config/core_server_services_camera.json",
            "config/core_server_services.json",
        ],
        base_alias="Server",
    )


def motion_thr(func, message):
    while True:
        try:
            with ThreadPoolExecutor() as pool:
                print("a")
                pool.submit(
                    func,
                    message,
                )
                print("b")
                if message:
                    message = None
        except:
            pass


if __name__ == "__main__":
    loggle.set_file_handler(
        "log/serverLog%s.log" % datetime.datetime.now().strftime("%Y%m%d"),
        loggle.INFO,
        "a",
    )

    mode = "core"
    visualize = False
    enableRobot = True
    visualFB = False

    xarm = ArmWrapper(enable=enableRobot, armIP=RC.settings["RobotConfig"]["XARM_IP"])
    before_pos = [0] * 6
    before_gpos = None

    RC.table_serial = TableSender(port=RC.settings["RobotConfig"]["TABLE_PORT"])

    if mode == "core":
        RC.core = None
        core_thr = threading.Thread(target=__set_core_thr, daemon=True)
        core_thr.start()
        while RC.core is None:
            pass
    elif mode == "key":
        key_server_thr = UDP_Server(port=8890)
        key_server_thr.start()
        test_dict = {
            "0": {"motion": MotionControl(), "command": None},
            "1": {"motion": MotionControl(), "command": None},
        }

    if visualFB:
        visFB = VisualSerailFB(port=RC.settings["RobotConfig"]["VISUAL_PORT"])

    if visualize:
        vis_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        vis_server_addr = ("127.0.0.1", 8585)

    with ThreadPoolExecutor() as pool:
        while True:
            try:
                if mode == "core":
                    try:
                        frame = RC.core.queue.get(block=False)
                        RC.core.joined_dict[frame["client_id"]]["command"] = frame

                    except:
                        pass
                    try:
                        for join in RC.core.joined_dict:
                            pool.submit(
                                RC.core.joined_dict[join]["motion"].create_motion,
                                RC.core.joined_dict[frame["client_id"]]["command"],
                            )
                            RC.core.joined_dict[frame["client_id"]]["command"] = None
                    except:
                        pass

                xarm.limitation_pos()
                if enableRobot:
                    xarm.send_data_to_robot()

                try:
                    robot_move = RC.robot_move_queue.get(block=False)
                    logger.info({"mes":robot_move})
                except:
                    pass

                if RC.pos != before_pos:
                    logger.info({"type": "robot_pos", "message": RC.pos})
                    if RC.pos[2] != before_pos[2]:
                        RC.core.core_write_data(
                            "server-data",
                            "robot-height",
                            {
                                "per-z": 100
                                * (RC.pos[2] - RC.MIN_Z)
                                / (RC.MAX_Z - RC.MIN_Z)
                            },
                        )
                # if visualFB:
                #     try:
                #         if robot_move["message"]["client_id"] == 1:
                #             visFB.OP1_Flag = 1
                #         elif robot_move["message"]["client_id"] == 2:
                #             visFB.OP2_Flag = 1
                #         visFB.send()
                #     except:
                #         pass
                #     try:
                #         if robot_move["client_id"] == 1:
                #             visFB.OP1_Flag = 0
                #         elif robot_move["client_id"] == 2:
                #             visFB.OP2_Flag = 0
                #         visFB.send()
                #     except:
                #         pass

                robot_move = None

                before_pos = RC.pos.copy()
                before_gpos = RC.gripper_pos

                if visualize:
                    vis_sock.sendto(pickle.dumps(RC.pos[0:3]), vis_server_addr)

            except KeyboardInterrupt:
                if mode == "core":
                    RC.core.core_stop()
                sys.exit()
