# -*- coding: utf-8 -*-
import bluetooth

import threading,thread
import logging
import time


lock = threading.Lock()
con = threading.Condition()
buf = ""


class Server:
    def __init__(self):
        self.server_socket = None
        self.client_socket = None
        self.port = 1
        self.uuid = "e8587008-297a-4676-9fc6-cc8ee6fa097c"
        self.address = None

    def setup_socket(self):
        self.server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

        self.port = 1

        self.server_socket.bind(("", self.port))
        self.server_socket.listen(1)

        print "listening on port %d " % self.port

        bluetooth.advertise_service(self.server_socket, "FooBar Service", self.uuid)
        self.client_socket, self.address = self.server_socket.accept()
        print "Accepted connection from ", self.address
        try:
            self.client_socket.send("Connect Setup")
        except AttributeError as e:
            print e

    def start_server(self):
        if self.client_socket is None:
            logging.error("socket is none")
            return

        while True:
            if con.acquire():
                print "server thread get con , and started "
                if lock.acquire():
                    con.notify()
                    lock.release()
                    print "server thread release thread and wait"
                    con.wait()

                    # 这里会阻塞
                    data = self.client_socket.recv(1024)

                    if data.length != 0:
                        print "received [%s] " % data

    def send_msg(self):

        if self.client_socket is None:
            logging.error("socket is none")
            return

        while True:
            if con.acquire():
                print "sending thread get con ,and started"
                global buf
                self.client_socket.send(buf)
                buf = ""
                lock.acquire()
                con.notify()
                print "sending thread send message over"
                con.wait()


def send_msg(st):
    print "normal send_msg  function"
    global buf
    buf = st
    try:
        print "lock release"
        lock.release()
    except thread.error as e:
        print "normal" + e
        pass


if __name__ == "__main__":
    ser = Server()
    lock.acquire()
    ser.setup_socket()
    if ser.client_socket is not None:

        server = threading.Thread(target=ser.start_server)
        server.start()
        client = threading.Thread(target=ser.send_msg)
        client.start()
        #time.sleep(100)

        while True:
            s = raw_input()
            send_msg(s)




