import os.path
import socket

from conf import settings
from lib import common

from tcp_client import socket_client

"""
管理员具体要实现的功能:
	1.注册
	2.登录
	3.上传视频
	4.删除视频
	5.发布公告
"""

# 保存用户状态的字典
user_info = {
    'cookies': None
}

# 在这里说明之后，在方法里面去.这个参数的时候就会有相应类型的自动补全
def register(client: socket.socket):
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
                'user_type': 'admin'
            }
            # 发送给服务端的过程,封装在公共组件里面，因为每个过程都会和服务器交互
            back_dic = common.send_msg_back_dic(send_dict, client)

            if back_dic.get('flag'):
                print(back_dic.get('msg'))
                break
            else:
                print(back_dic.get('msg'))

def login(client: socket.socket):
    while True:
        username = input('请输入用户名: ').strip()
        password = input('请输入密码: ').strip()

        send_dic = {
            'type': 'login',
            'username': username,
            'password': password,
            'user_type': 'admin'
        }

        # 把认证的信息发送到服务端
        back_dic = common.send_msg_back_dic(send_dic, client) # type: dict

        if back_dic.get('flag'):
            session = back_dic.get('session')
            user_info['cookies'] = session
            print(user_info['cookies'])
            print(back_dic.get('msg'))
            break
        else:
            print(back_dic.get('msg'))

def upload_movie(client: socket.socket):
    while True:
        # 1.打印电影列表
        movie_list =  common.get_movie_list()
        for index, movie in enumerate(movie_list):
            print(index, movie)

        choice = input('请输入上传电影的编号: ').strip()

        if not choice.isdigit():
            print('请输入数字!')
            continue

        choice = int(choice)
        if choice not in range(len(movie_list)):
            print('请输入正确的编号!')
            continue

        movie_name = movie_list[choice]

        movie_path = os.path.join(
            settings.UPLOAD_FILES, movie_name
        )

        file_md5 = common.get_movie_md5(movie_path)

        send_dic = {
            'type': 'check_movie',
            'session': user_info.get('cookies'),
            'file_md5': file_md5
        }

        # 做电影文件的校验
        back_dic = common.send_msg_back_dic(send_dic,client)
        print(back_dic)
        break

def delete_move():
    pass

def put_notice():
    pass

func_dic = {
    '1': register,
    '2': login,
    '3': upload_movie,
    '4': delete_move,
    '5': put_notice
}

# 展示用户的功能菜单
def admin_view():
    while True:
        print(
        """
        1.注册
        2.登录
        3.上传视频
        4.删除视频
        5.发布公告
        按q退出
        """
        )
        choice = input('请选择功能: ').strip()
        if choice == 'q':
            break
        if choice not in func_dic:
            print('请选择正确的功能选项!')
            continue

        sk_client = socket_client.SocketClient()
        client = sk_client.get_client()
        func_dic.get(choice)(client)