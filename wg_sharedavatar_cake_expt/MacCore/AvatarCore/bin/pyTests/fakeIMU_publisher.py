# This Python file uses the following encoding: utf-8
from CorePython.CoreAPI import CoreAPI
from CorePython.CoreData import CoreData

import time
import math
import json

core_api = CoreAPI()


def stop():
    global core_api
    core_api.destroy_api()
    print('Core Destroyed!')

t=0

if __name__ == "__main__":
    core_api.init_api(app_path='./', master=False)
    # Create a Data resource
    while(True):
        data={
            "Euler":"{x},{y},{z}".format(x=int(90*math.sin(t)),y=int(30*math.cos(t)),z=int(45*math.sin(t*0.2)))
        }
        core_api.publish_message("","core/sensors/IMU",json.dumps(data))
        t+=0.05
        time.sleep(0.05)
