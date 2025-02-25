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

        if back_dic.get('flag'):
            print(back_dic.get('msg'))

            send_dic = {
                'type': 'upload_movie',
                'file_md5': file_md5,
                'file_size': os.path.getsize(movie_path),
                'movie_name': movie_name,
                'session': user_info.get('cookies')
            }

            is_free = input('上传的电影是否免费: y/n: (Default "n")').strip()

            if is_free == 'y':
                send_dic['is_free'] = 1
            else:
                send_dic['is_free'] = 0

            back_dic = common.send_msg_back_dic(send_dic, client, file = movie_path)
            if back_dic.get('flag'):
                print(back_dic.get('msg'))
                break
        else:
            print(back_dic.get('msg'))


# 删除电影
def delete_move(client):
    while True:
        # 先从服务端获取电影的列表
        send_dic = {
            'type': 'get_movie_list',
            'session': user_info.get('cookies'),
            'movie_type': 'all'
        }

        # 发送获取电影请求
        back_dic = common.send_msg_back_dic(send_dic, client)
        if back_dic.get('flag'):
            back_movie_list = back_dic.get('back_movie_list')
            # 打印选择的电影
            for index, movie_list in enumerate(back_movie_list):
                print(index, movie_list)

            # 选择要删除的电影
            choice = input('请输入要删除的电影编号: ').strip()

            if choice == 'q':
                break

            if not choice.isdigit():
                continue

            choice = int(choice)

            if choice not in range(len(back_dic)):
                continue

            # back_movie_list[choice] => [movie_obj.name, '免费' if movie_obj.is_free else "收费", movie_obj.id]
            movie_id = back_movie_list[choice][2]

            send_dic = {
                'type': 'delete_movie', 'movie_id': movie_id, 'session': user_info.get('cookies')
            }

            # 发送删除电影的请求
            back_dic = common.send_msg_back_dic(send_dic, client)
            if back_dic.get('flag'):
                print(back_dic.get('msg'))
                break
        else:
            print(back_dic.get('msg'))
            break

def put_notice(client):
    title = input("请输入公告标题: ").strip()
    content = input('请输入公告内容: ').strip()

    send_dic = {
        'type': 'put_notice',
        'session': user_info.get('cookies'),
        'title': title,
        'content': content
    }

    back_dic = common.send_msg_back_dic(send_dic, client)
    print(back_dic.get('msg'))

func_dic = {
    '1': register,
    '2': login,
    '3': upload_movie,
    '4': delete_move,
    '5': put_notice
}

# 展示用户的功能菜单
def admin_view():
    sk_client = socket_client.SocketClient()
    client = sk_client.get_client()
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
        func_dic.get(choice)(client)