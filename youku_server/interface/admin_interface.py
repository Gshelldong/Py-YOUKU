from lib import common
from db import models


@common.login_auth
def upload_movie_interface(client_back_dic, conn):
    print('上传电影功能')

@common.login_auth
def check_movie_interface(client_back_dic, conn):
    file_md5 = client_back_dic.get('file_md5')
    movie_list = models.Movie.select(file_md5 = file_md5)
    if movie_list:
        print('11111有电影存在')
        send_dic = {
            'flag': False, 'msg': '电影已经存在了!'
        }
    else:
        print('222222')
        send_dic = {
            'flag': True, 'msg': '电影可以上传!'
        }
    common.send_data(send_dic, conn)

def delete_movie_interface():
    pass

def put_notice_interface():
    pass


