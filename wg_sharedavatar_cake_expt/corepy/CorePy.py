import json
import platform
from concurrent.futures import ThreadPoolExecutor

from loggle import logger
from sharedavatar import RobotConfig as RC
from sharedavatar.MotionControl import MotionControl
from visualFB.VisualFB import VisualStageFB

__system_name = platform.system()
if __system_name == "Windows":
    from WinCore.AvatarCore.bin.CorePython.CoreAPI import CoreAPI
    from WinCore.AvatarCore.bin.CorePython.CoreResourceManager import (
        CoreResourceManager,
    )
    from WinCore.AvatarCore.bin.CorePython.CoreSession import CoreSession
    from WinCore.AvatarCore.bin.CorePython.Timeout import set_timeout
elif __system_name == "Darwin":
    from MacCore.AvatarCore.bin.CorePython.CoreAPI import CoreAPI
    from MacCore.AvatarCore.bin.CorePython.CoreResourceManager import (
        CoreResourceManager,
    )
    from MacCore.AvatarCore.bin.CorePython.CoreSession import CoreSession
    from MacCore.AvatarCore.bin.CorePython.Timeout import set_timeout
elif __system_name == "Linux":
    from MacCore.AvatarCore.bin.CorePython.CoreAPI import CoreAPI
    from MacCore.AvatarCore.bin.CorePython.CoreResourceManager import (
        CoreResourceManager,
    )
    from MacCore.AvatarCore.bin.CorePython.CoreSession import CoreSession
    from MacCore.AvatarCore.bin.CorePython.Timeout import set_timeout


class CoreSet:
    def __init__(self, app_name):
        self.core_api = CoreAPI()
        self.core_session = CoreSession(self.core_api)

        self.core_api.init_api(
            master=True, app_path="./", port=0, log_path="./log", app_name=app_name
        )

    def create_resource(self):
        self.core_resource = CoreResourceManager(self.on_resource_frame_arrived)
        self.core_resource.start(1)

    def on_resource_frame_arrived(self, type, resource, channel, frame):
        if type == "data":
            self.receive_data = json.loads(frame)

    def core_write_data(self, resource, channel, message):
        try:
            self.core_resource.write_data(resource, channel, json.dumps(message))
        except:
            logger.exception("write data failed")

    def core_stop(self):
        self.core_session.clear_session_callbacks()

        self.core_finished = self.core_api.destroy_api()


class CoreServer(CoreSet):
    def __init__(self, server_ip: str, services: list, base_alias: str):
        super().__init__(app_name="coreServer")

        self.server_ip = server_ip
        self.base_alias = base_alias

        self.joined_dict = {}
        self.joined_pool = ThreadPoolExecutor()
        self.joined_future = None

        self.core_api.subscribe_to_message(
            "avatarin", "cloud/status", self.__cloud_status
        )
        self.core_api.subscribe_to_message(
            "avatarin", "cloud/peer/joined", self.__joined_client
        )
        self.core_api.subscribe_to_message(
            "avatarin", "cloud/peer/disconnected", self.__disconnected_client
        )

        for service in services:
            self.core_api.load_services(service)

        self.core_api.start_default_services()
        self.core_session.init_session(base_alias + "/cloud")
        self.core_session.set_peer_id(self.server_ip)

        self.create_resource()

    def __cloud_status(self, name, path, data):
        self.cloud_status = data

    def __joined_client(self, name, path, data):
        self.joined_future = self.joined_pool.submit(self.__id_mapping, data)
        client_id = self.joined_future.result()
        ###  if visualFB==True:
        # if client_id == 1:
        #     self.vis_stage_1 = VisualStageFB(
        #         port=RC.settings["RobotConfig"]["STAGE1_PORT"], ID=client_id
        #     )
        #     self.vis_stage_1.start()
        # elif client_id == 2:
        #     self.vis_stage_2 = VisualStageFB(
        #         port=RC.settings["RobotConfig"]["STAGE2_PORT"], ID=client_id
        #     )
        #     self.vis_stage_2.start()
        self.joined_dict[client_id] = {
            "client_ip": data,
            "motion": MotionControl(),
            "command": None,
        }
        logger.info("client joined : %s" % self.joined_dict)

        self.core_api.start_service(
            self.base_alias + "/receiver/data/client/" + str(client_id)
        )
        self.core_resource.subscribe_data("client-data-%s" % client_id, "command")
        self.core_resource.subscribe_data("client-data-%s" % client_id, "cursor")
        self.core_resource.subscribe_data(
            "client-data-%s" % client_id, "cursor-pressed"
        )
        self.core_resource.subscribe_data("client-data-%s" % client_id, "button-state")
        self.core_resource.subscribe_data("client-data-%s" % client_id, "test")

        self.core_write_data(
            "server-data", "id", {"client_id": client_id, "client_ip": data}
        )

    def __id_mapping(self, joined_ip):
        if joined_ip not in self.joined_dict.values():
            id_list = list(self.joined_dict.keys())
            id_list.sort()
            if id_list:
                if id_list[0] == 1:
                    if len(id_list) >= 2:
                        for i in range(len(id_list)):
                            try:
                                if id_list[i + 1] - id_list[i] == 1:
                                    c_id = i + 3
                                else:
                                    c_id = i + 2
                            except:
                                pass
                    else:
                        c_id = 2
                else:
                    c_id = 1
            else:
                c_id = 1
        else:
            logger.error("Already mapped id !!!")
        return c_id

    def __disconnected_client(self, name, path, data):
        data = json.loads(data)
        logger.error(data)
        for key, value in self.joined_dict.items():
            try:
                if value["client_ip"] == str(data["id"]):
                    del self.joined_dict[key]
                    break
            except:
                pass
            try:
                if value["client_ip"] == str(data["PeerID"]):
                    del self.joined_dict[key]
                    break
            except:
                pass

    def core_stop(self):
        self.core_resource.destroy()
        self.core_resource = None
        self.core_session.disconnect_from_peer(self.server_ip)
        return super().core_stop()


class CoreClient(CoreSet):
    def __init__(self, server_ip: str, client_ip: str, services: list, base_alias: str):
        super().__init__(app_name="coreClient")

        self.server_ip = server_ip
        self.client_ip = client_ip

        self.client_id = None

        self.base_alias = base_alias

        for service in services:
            self.core_api.load_services(service)

        self.core_api.start_default_services()
        self.core_session.init_session(self.base_alias + "/cloud")
        self.core_session.set_peer_id(self.client_ip)
        self.core_api.start_service(self.base_alias + "/receiver/data/server")

        self.create_resource()
        self.core_resource.subscribe_data("server-data", "id")
        set_timeout(self.__connect_to_session, 2000)

    def __connect_to_session(self):
        self.core_session.connect_to_peer(self.server_ip)

    def core_write_data(self, resource, channel, message):
        write_data = {"client_id": self.client_id, "data": message}
        return super().core_write_data(resource, channel, write_data)

    def on_resource_frame_arrived(self, type, resource, channel, frame):
        super().on_resource_frame_arrived(type, resource, channel, frame)
        if type == "data":
            if resource == "server-data":
                if channel == "id":
                    if self.client_id is None:
                        if self.client_ip == self.receive_data["client_ip"]:
                            self.client_id = self.receive_data["client_id"]
                            self.core_api.start_service(
                                self.base_alias
                                + "/sender/data/client/"
                                + str(self.client_id)
                            )

    def core_stop(self):
        self.core_resource.destroy()
        self.core_resource = None
        self.core_session.disconnect_from_peer(self.server_ip)
        return super().core_stop()
