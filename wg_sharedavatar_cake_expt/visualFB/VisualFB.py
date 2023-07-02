import threading

import serial
from loggle import logger


class VisualSerailFB:
    def __init__(self, port=""):
        self.OP1_Flag = 0
        self.OP2_Flag = 0
        try:
            self.LEDserial = serial.Serial(port, 115200, timeout=0.01)
            logger.info("Successfully connected to the VisFB")
        except:
            logger.error("Failed to connecting VisFB")

    def send(self):
        try:
            condition = self.OP1_Flag + self.OP2_Flag * 2 + 1
            mes = bytes(str(condition), "utf-8")
            self.LEDserial.write(mes)
        except:
            logger.error("Failed to send")


class VisualStageFB(threading.Thread):
    def __init__(self, port, ID):
        threading.Thread.__init__(self, daemon=True)
        self.id = ID
        try:
            self.LEDserial = serial.Serial(port, 115200, timeout=0.1)
            logger.info("Successfully connected to the VisFB_Stag, port:%s" % port)
        except:
            logger.error("Failed to connecting VisFB_Stage")

    def run(self):
        while True:
            try:
                mes = bytes(str(self.id), "utf-8")
                self.LEDserial.write(mes)
            except:
                # logger.error("Failed to send")
                pass
