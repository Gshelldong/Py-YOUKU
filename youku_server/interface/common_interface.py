from db import models
from lib import common,lock_file
from db import user_data


def register_interface(client_back_dic,conn):
    username = client_back_dic.get('username')

    # 这里orm中的异常处理有问题，如果没有表，不会报错，导致无法直接向下执行代码。
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

def login_interface(client_back_dic: dict,conn):
    username = client_back_dic.get('username')
    user_list = models.User.select(name=username)
    if not user_list:
        send_dic = {'flag': False, 'msg': '用户不存在'}
    else:
        user_obj = user_list[0]
        password = client_back_dic.get('password')

        # 判断用户对象的密码和数据库的密码是否一致
        if user_obj.pwd == common.get_md5_pwd(password):
            # 产生一个随机的字符串作为session值
            session = common.get_random_code()

            addr = client_back_dic.get('addr')
            # 保存session值到服务端，session + user_id一同保存到服务端本地
            # 使用锁写入数据
            lock_file.mutex.acquire()
            user_data.user_online[addr] = [session, user_obj.id]
            lock_file.mutex.release()
            print(user_data.user_online)

            send_dic = {'flag': True,'msg': '登陆成功!','session': session}
        else:
            send_dic = {'flag': False, 'msg': '用户名或密码错误!'}
    common.send_data(send_dic,conn)

def get_movie_list_interface():
    pass