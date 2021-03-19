# import paho.mqtt.client as mqtt
# import pyaudio
# import struct
# import base64

# CHUNKSIZE = 1024  # fixed chunk size
# OUTPUT_SAMPLE_RATE = 44100

# # initialize portaudio
# pya = pyaudio.PyAudio()
# stream_out = pya.open(format=pyaudio.paInt16, channels=1, rate=OUTPUT_SAMPLE_RATE, output=True)

# # The callback for when the client receives a CONNACK response from the server.
# def on_connect(client, userdata, flags, rc):
#     print("Connected with result code "+str(rc))

#     # Subscribing in on_connect() means that if we lose the connection and
#     # reconnect then subscriptions will be renewed.
#     client.subscribe("sample_sound")

# def on_message(client, userdata, msg):
#     stream_out.write(msg.payload)


# client = mqtt.Client()
# client.on_connect = on_connect
# client.on_message = on_message

# client.connect("broker.emqx.io", 1883, 60)
# client.loop_forever()

import socket
import base64
import pyaudio
import numpy as np
from threading import Thread


IP_SERVER = "192.168.86.22"
AUDIO_SERVER_PORT = 11112
TIMEOUT_SOCKET = 10

# PyAudio configuration
SIZE_PACKAGE = 1024
CHANNELS = 1
RATE = 44100
FORMAT = pyaudio.paInt16


def audio_thread(socket_connection):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    )
    
    while True:
        data = socket_connection.recv(SIZE_PACKAGE)
        if data:
            stream.write(data)

    socket_connection.close()
    stream.stop_stream()
    stream.close()
    p.terminate()


if __name__ == '__main__':
    # Socket audio initialization
    connection_audio = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection_audio.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection_audio.settimeout(TIMEOUT_SOCKET)

    # Connect channels
    connection_audio.connect((IP_SERVER, AUDIO_SERVER_PORT))
    
    audio_thread(connection_audio)
