import socket
import pickle
from constants import *


def receive_msg(s: socket.socket, buffer_size=server_opt['BUFFER_SIZE'], header_size=server_opt['HEADER_SIZE']):
    """
    :param s: socket to .recv() message from
    :param buffer_size: buffer size
    :param header_size: header size
    :return: returns bytestring message w/o header
    """
    while True:
        full_msg = b''
        new_msg = True
        while True:
            msg = s.recv(buffer_size)
            if new_msg:
                #print("new msg len:", msg[:header_size])
                msglen = int(msg[:header_size])
                new_msg = False

            #print(f"full message length: {msglen}")

            full_msg += msg

            if len(full_msg) - header_size == msglen:
                return pickle.loads(full_msg[header_size:])  #

            # if len(full_msg) - HEADERSIZE == msglen:
            #    print("full msg recvd")
            #    print(full_msg[HEADERSIZE:])
            #    print(pickle.loads(full_msg[HEADERSIZE:]))
            #    new_msg = True
            #    full_msg = b""


def send_msg(s: socket.socket, obj: object, header_size = server_opt['HEADER_SIZE']):
    msg = pickle.dumps(obj)
    msg = bytes(f"{len(msg):<{header_size}}", 'utf-8') + msg
    s.send(msg)
    return
