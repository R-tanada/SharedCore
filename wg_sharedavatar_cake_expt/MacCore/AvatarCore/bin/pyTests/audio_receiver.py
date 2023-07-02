# This Python file uses the following encoding: utf-8
from CorePython.CoreAPI import CoreAPI
from CorePython.CoreAudio import CoreAudio
from CorePython.Audio import AudioFormat

import time

core = CoreAPI()


def audio_frame_callback(resource, frame):
    print('New frame arrived: ' +
          '{0} x {1} - '.format(frame.channels, frame.rate) +
          'Format: {0} - '.format(AudioFormat(frame.format)) +
          'Length {0}'.format(frame.length))
    # Now you can process the samples
    bytesList = frame.audio_data.tolist()
    print("Number of bytes: " + str(len(bytesList)))


def stop():
    global audio
    audio.destroy()
    audio = None
    global core
    core.destroy_api()
    core = None
    print("Core destroyed")


if __name__ == "__main__":
    core.init_api(app_path="./")
    audio = CoreAudio('local-audio', audio_frame_callback)
    audio.start()

    try:
        while True:
            time.sleep(1)
            pass
    except KeyboardInterrupt:
        stop()
