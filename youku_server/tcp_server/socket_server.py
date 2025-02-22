import socket
import struct
import json
from db import models
from lib import common

class SocketServer:
    def __init__(self):
        self.server = socket.socket()
        self.server.bind(('127.0.0.1',8080))
        self.server.listen(5)

    def run(self):
        print('服务端已经启动，监听127.0.0.1:8080 ......')
        while True:
            conn, addr = self.server.accept()

            headers = conn.recv(4)
            data_len = struct.unpack('i',headers)[0]
            date_bytes = conn.recv(data_len)
            client_back_dic = json.loads(date_bytes.decode('utf-8')) # type: dict

            # 判断功能的类型
            if client_back_dic.get('type') == 'register':
                # 写业务逻辑
                # 判断用户是否存在
                username = client_back_dic.get('username')
                user_obj_list = models.User.select(name = username)

                # 如果用户已经存在就返回msg
                if user_obj_list:
                    send_dic = {'flag': False,'msg': '用户已经存在!'}

                # 若不存在，保存数据到MySQL数据库中， 返回注册成功给客户端
                else:
                    password = client_back_dic.get('password')
                    user_obj = models.User(
                        name=username,
                        #  pwd, is_vip, is_locked, user_type, register_time
                        pwd=common.get_md5_pwd(password),
                        is_vip=0,
                        is_locked=0,
                        user_type=client_back_dic.get('user_type'),
                        register_time=common.get_time())

                    user_obj.save()

                    send_dic = {'flag': True, 'msg': '注册成功'}

                data_bytes = json.dumps(send_dic).encode('utf-8')
                headers = struct.pack('i', len(data_bytes))
                conn.send(headers)
                conn.send(data_bytes)


