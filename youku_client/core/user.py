import os.path
import time

from tcp_client import socket_client
from lib import common
from conf import settings

user_info = {
    'cookies': None,
    'is_vip': None
}

def register(client):
    while True:
        username = input('请输入用户名: ').strip()
        password = input('请输入用户名密码: ').strip()
        re_password = input('请再次输入密码: ').strip()

        if password == re_password:
            # 在用户表插入数据的字段
            send_dict = {
                'username': username,
                'password': password,
                'type': 'register',
                'user_type': 'user'
            }

            # {'flag': False, 'msg': '用户已存在!'}
            # {'flag': True, 'msg': '注册成功'}
            # 发送给服务端的过程,封装在公共组件里面，因为每个过程都会和服务器交互
            back_dic = common.send_msg_back_dic(send_dict, client)

            if back_dic.get('flag'):
                print(back_dic.get('msg'))
                break
            else:
                print(back_dic.get('msg'))

def login(client):
    while True:
        username = input('请输入用户名: ').strip()
        password = input('请输入密码: ').strip()

        send_dic = {
            'type': 'login',
            'username': username,
            'password': password,
            'user_type': 'user'
        }

        # 把认证的信息发送到服务端
        back_dic = common.send_msg_back_dic(send_dic, client) # type: dict

        if back_dic.get('flag'):
            session = back_dic.get('session')
            user_info['cookies'] = session
            user_info['is_vip'] = back_dic.get('is_vip')
            print(user_info['cookies'])
            print(back_dic.get('msg'))

            if back_dic.get('new_notice'):
                print(back_dic.get('new_notice'))
            break
        else:
            print(back_dic.get('msg'))

def by_vip(client):
    # 从本地就先进行判断了
    if user_info.get('is_vip'):
        print('你已经是会员了!')
        return

    is_vip = input('是否购买会员y/n ?: ').strip()
    if is_vip == 'y':
        send_dic = {
            'type': 'buy_vip',
            'session': user_info.get('cookies')
        }

        back_dic = common.send_msg_back_dic(send_dic, client)

        if back_dic.get('flag'):
            print(back_dic.get('msg'))
    else:
        ('快去充值100w!')

def check_all_movie(client):
    send_dic = {
        'type': 'get_movie_list',
        'session': user_info.get('cookies')
    }

    back_dic = common.send_msg_back_dic(send_dic,client)
    if back_dic.get('flag'):
        print(back_dic.get('back_movie_list'))
    else:
        print(back_dic.get('msg'))

def download_free_movie(client):
    while True:
        # 获取所有的免费电影
        send_dic = {
            'type': 'get_movie_list',
            'session': user_info.get('cookies'),
            'movie_type': 'free'
        }

        back_dic = common.send_msg_back_dic(send_dic, client)

        if back_dic.get('flag'):
            # 2.选择下载的免费电影，并提交给服务端
            movie_list = back_dic.get('back_movie_list')
            for index, movie in enumerate(movie_list):
                print("%s -- %s"%(index, movie))

            choice = input('请输入下载的电影编号: ').strip()

            if not choice.isdigit():
                continue

            choice = int(choice)

            if choice not in range(len(movie_list)):
                continue
            # 0 -- ['06d3ae46ec08a2929ebf236cf75045a7打牌.mp4', '免费', 3]
            movie_name, movie_type, movie_id = movie_list[choice]

            send_dic = {
                'type': 'download_movie',
                'session': user_info.get('cookies'),
                'movie_id': movie_id,
                'movie_name': movie_name,
                'movie_type': movie_type
            }

            back_dic = common.send_msg_back_dic(send_dic,client)

            if back_dic.get('flag'):
                # 3.开始下载电影
                movie_path = os.path.join(settings.DOWNLOAD_FILES, movie_name)
                movie_size = back_dic.get('movie_size')

                wait_time = back_dic.get('wait_time')

                if wait_time:
                    print('广告时间。。。。。')
                    time.sleep(wait_time)

                recv_data = 0

                with open(movie_path, 'wb') as f:
                    while recv_data < movie_size:
                        data = client.recv(1024)
                        f.write(data)
                        recv_data += len(data)
                    f.flush()
                print('电影下载成功!')
                break
        else:
            print(back_dic.get('msg'))
            break

def download_pay_movie(client):
    pass

def check_download_record(client):
    pass

def check_all_notice(client):
    pass


func_dic = {
    '1': register,
    '2': login,
    '3': by_vip,
    '4': check_all_movie,
    '5': download_free_movie,
    '6': download_pay_movie,
    '7': check_download_record,
    '8': check_all_notice
}


def user_view():
    sk_client = socket_client.SocketClient()
    client = sk_client.get_client()

    while True:
        print(
        """
        1.注册
        2.登录
        3.充会员
        4.查看视频
        5.下载免费视频
        6.下载会员视频
        7.查看观影记录
        8.查看所有公告
        """
        )

        choice = input('请选择功能编号: ').strip()

        if choice == 'q':
            break

        if choice not in func_dic:
            break

        func_dic.get(choice)(client)

