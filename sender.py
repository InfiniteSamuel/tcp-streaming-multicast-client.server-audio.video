# import paho.mqtt.client as mqtt
# import pyaudio
# import struct
# import base64
# from time import sleep

# CHUNKSIZE = 1024 # fixed chunk size
# OUTPUT_SAMPLE_RATE = 44100

# # initialize portaudio
# pya = pyaudio.PyAudio()
# stream_in = pya.open(format=pyaudio.paInt16, channels=1, rate=OUTPUT_SAMPLE_RATE, input=True, frames_per_buffer=CHUNKSIZE)

# # The callback for when the client receives a CONNACK response from the server.
# def on_connect(client, userdata, flags, rc):
#     print("Connected with result code "+str(rc))


# client = mqtt.Client()
# client.on_connect = on_connect

# client.connect("broker.emqx.io", 1883, 60)
# client.loop_start()

# while True:
#     # do this as long as you want fresh samples
#     bytestream = stream_in.read(CHUNKSIZE)
#     client.publish("sample_sound", bytestream)


import socket
# import base64
import pyaudio
import numpy as np
from threading import Thread
import collections
import time

# Sockets channels configuration
IP_SERVER = "192.168.86.22"
AUDIO_SERVER_PORT = 11112
MAX_NUM_CONNECTIONS_LISTENER = 20

# PyAudio configuration
CHUNK = 1
CHANNELS = 1
RATE = 44100
FORMAT = pyaudio.paInt16

# d = collections.deque(maxlen=RATE*(CHUNK+1))


# class ConnectionPoolAudio(Thread):
#     def __init__(self, conn, device):
#         Thread.__init__(self)
#         # self.ip = ip
#         # self.port = port
#         self.conn = conn
#         self.device = device

#         # print("[+][.audio] New server socket thread started for " + ip + ":" + str(port))

#     def run(self):
#         while True:
#             data = self.device.read(CHUNK, exception_on_overflow=False)
#             self.conn.send(data)
#         self.conn.close()

conns = []


def callback(in_data, frame_count, time_info, status):
    # print(frame_count, time_info, status, in_data)
    for conn in conns:
        conn.send(in_data)

    return (in_data, pyaudio.paContinue)


def tcp_audio_thread():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    stream_callback=callback)
    stream.start_stream()

    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind((IP_SERVER, AUDIO_SERVER_PORT))
    connection.listen(MAX_NUM_CONNECTIONS_LISTENER)
    while True:
        (conn, (ip, port)) = connection.accept()
        conns.append(conn)
        # thread = ConnectionPoolAudio(conn, stream)
        # thread.start()


if __name__ == '__main__':
    print("Starting...")
    thread_audio = Thread(target=tcp_audio_thread)
    thread_audio.start()
