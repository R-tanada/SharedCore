# This Python file uses the following encoding: utf-8
from math import sin
from CorePython.CoreAPI import CoreAPI
from CorePython.Audio import AudioFormat
from CorePython.CoreAudio import CoreAudio
# import numpy
import threading
# import random
# import array

import time

core = CoreAPI()
audio = None
stopped = False

# Sampling rate
sampling_rate = 8000

# length of a buffer, make it half a second
length = int(sampling_rate/2)

# number channels
channel = 2

_time = 0


def generate_audio_data():
    if stopped is True:
        return

    global sampling_rate
    global channel
    global audio
    global length
    global _time

    # delta time is the opposite of sampling rate
    dt = 1.0 / sampling_rate
    # generate an empty audio data holder
    audio_data = [0 for i in range(length * channel)]

    for i in range(0, length):
        # Generate a sin wave at freq of 440Hz
        _time += dt * 440
        sample = sin(_time)
        # process the channels. The buffer layout for two channels should be
        # [Channel 0, Channel 1, Channel 0, Channel 1, ..., Channel 0, Channel]
        for j in range(0, channel):
            # convert the sample from floating point to UInt 16 by multiplying
            # with 65535 (0->65535)
            audio_data[i * channel + j] = int((sample * 0.5 + 0.5) * 65535)

    # write the frame to the resource
    audio.write_frame(channel,
                      sampling_rate,
                      length,
                      AudioFormat.U16,
                      audio_data)
    # recall the timer function to generate the next piece of audio
    threading.Timer(0.4, generate_audio_data).start()


def stop():
    global stopped
    stopped = True
    global audio
    audio.destroy()
    audio = None
    global core
    core.destroy_api()
    core = None
    print('Core destroyed')


if __name__ == "__main__":

    core.init_api(app_path='./')
    # create a resource named "local-audio"
    audio = CoreAudio('local-audio')
    generate_audio_data()

    try:
        while True:
            time.sleep(1)
            pass
    except KeyboardInterrupt:
        stop()
