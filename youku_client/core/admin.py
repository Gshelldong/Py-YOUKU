import socket
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

def login():
    pass

def upload_movie():
    pass

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