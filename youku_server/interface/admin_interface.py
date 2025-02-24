from lib import common

send_dic = {
    'type': 'login',
    'username': 'gong',
    'password': '123',
    'user_type': 'admin',
    'addr': '127.0.0.1'
}

@common.login_auth
def upload_movie_interface(client_back_dic):
    print('上传电影功能')

def check_movie_interface():
    pass

def delete_movie_interface():
    pass

def put_notice_interface():
    pass

if __name__ == '__main__':
    upload_movie_interface(send_dic)

