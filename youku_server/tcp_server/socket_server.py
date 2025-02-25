import socket
import struct
import json
from concurrent.futures import ThreadPoolExecutor
from interface import common_interface,admin_interface,user_interface

from threading import Lock
from lib import lock_file
from db import user_data

# 生成一把锁
lock = Lock()
lock_file.mutex = lock


func_dic = {
    'register': common_interface.register_interface,
    'login': common_interface.login_interface,
    'check_movie': admin_interface.check_movie_interface,
    'upload_movie': admin_interface.upload_movie_interface,
    'get_movie_list': common_interface.get_movie_list_interface,
    'delete_movie': admin_interface.delete_movie_interface,
    'put_notice': admin_interface.put_notice_interface,

    # 普通用户的功能
    'buy_vip': user_interface.by_vip_interface,
    'download_movie': user_interface.download_movie_interface
}


class SocketServer:
    def __init__(self):
        self.server = socket.socket()
        self.server.bind(('127.0.0.1', 8080))
        self.server.listen(5)
        self.pool = ThreadPoolExecutor(50)

    def run(self):
        print('服务端已经启动，监听127.0.0.1:8080 ......')
        while True:
            conn, addr = self.server.accept()
            self.pool.submit(self.working, conn, addr)
        # self.working(conn,addr)

    def dispatcher(self,client_back_dic, conn):
        _type = client_back_dic.get('type')

        if _type in func_dic:
            f = func_dic.get(_type)
            f(client_back_dic, conn)

    def working(self, conn, addr):
        while True:
            try:
                headers = conn.recv(4)
                data_len = struct.unpack('i', headers)[0]
                data_bytes = conn.recv(data_len)
                client_back_dic = json.loads(data_bytes.decode('utf-8'))  # type: dict
                client_back_dic['addr'] = str(addr)
                self.dispatcher(client_back_dic,conn)
            except Exception as e:
                print(e)
                lock.acquire()
                user_data.user_online.pop(str(addr))
                lock.release()
                conn.close()
                break
