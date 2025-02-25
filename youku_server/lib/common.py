import hashlib
import time
import json
import struct
import uuid
from functools import wraps
from db import user_data


def get_md5_pwd(password: str):
    md = hashlib.md5()
    md.update(password.encode('utf-8'))
    md.update('solt-123456'.encode('utf-8'))
    return md.hexdigest()

def get_time():
    now_time = time.strftime('%Y-%m-%d %X')
    return now_time

def send_data(send_dic, conn):
    data_bytes = json.dumps(send_dic).encode('utf-8')
    headers = struct.pack('i', len(data_bytes))
    conn.send(headers)
    conn.send(data_bytes)

def get_random_code():
    md5 = hashlib.md5()
    md5.update(str(uuid.uuid4()).encode('utf-8'))
    return md5.hexdigest()

def login_auth(func):
    @wraps(func)
    # 接口层包含两个位置参数，client_back_dic,conn
    # 获取客户端传过来的session，和服务端的做对比，如果一致就认为用户登陆状态合法
    def inner(*args, **kwargs):
        print('args 0 :',args[0])

        # args 0 : {'type': 'buy_vip', 'session': '46024c342f229814c218e7044af8d953', 'addr': "('127.0.0.1', 56468)"}
        addr = args[0].get('addr')
        # user_online = > {"('127.0.0.1', 56468)": ['46024c342f229814c218e7044af8d953', 2]}
        user_session = user_data.user_online.get(addr)

        client_cookie_session = args[0].get('session')
        print('用户侧的 - cookies ',client_cookie_session)
        # 服务端存放的session
        print('服务端的- session ', user_data.user_online.values())
        for server_save_session in user_data.user_online.values():
            print('判断session - %s : %s'%(client_cookie_session,server_save_session[0]))
            if client_cookie_session == server_save_session[0]:
                args[0]['user_id'] = user_session[1]
                func(*args, **kwargs)
                return
            # user_session = user_data.user_online.get(addr) 使用客户端的方式因为可能换连接导致客户断地址不一致
            # print('serser user_session: ',user_session)
            # if user_session:
            #     if args[0].get('session') == user_session[0]:
            #         args[0]['user_id'] = user_session[1]
            #     if args[0].get('user_id'):
            #         func(*args, ** kwargs)
        send_dic = {'flag': False, 'msg': '未登录，请去登录!'}
        # send_data(send_dic, conn)
        send_data(send_dic, args[1])
    return inner


if __name__ == '__main__':
    res = get_random_code()
    print(res)