import json
import struct
from db import models
from lib import common

def register_interface(client_back_dic,conn):
    print('hahahhaha ')
    username = client_back_dic.get('username')
    user_obj_list = models.User.select(name=username)

    # 如果用户已经存在就返回msg
    if user_obj_list:
        send_dic = {'flag': False, 'msg': '用户已经存在!'}

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

   # 在这一层直接返回到客户端
    common.send_data(send_dic, conn)

def login_interface():
    pass
