import os.path

from conf import settings
from lib import common
from db import models

@common.login_auth
def by_vip_interface(client_back_dic, conn):
    user_id = client_back_dic.get('user_id')
    user_obj = models.User.select(id = user_id)[0]
    user_obj.is_vip = 1
    user_obj.sql_update()

    send_dic = {'flag': True,'msg': '会员充值成功!'}
    common.send_data(send_dic, conn)


def download_movie_interface(client_back_dic, conn):
    movie_id = client_back_dic.get('movie_id')
    movie_name = client_back_dic.get('movie_name')
    movie_type = client_back_dic.get('movie_type')
    user_id = client_back_dic.get('user_id')
    movie_path = os.path.join(settings.DOWNLOAD_PATH,movie_name)
    movie_size = os.path.getsize(movie_path)

    send_dic = {
        'flag':True,
        'msg': '准备下载',
        'movie_size': movie_size
    }

    user_obj = models.User.select(id=user_id)[0]
    # todo 这里可能报错

    if movie_type == '免费':
        wait_time = 0

        if not user_obj.is_vip:
            wait_time = 20
        send_dic['wait_time'] = wait_time
    print(send_dic)

    common.send_data(send_dic, conn, movie_path)

    obj = models.DownloadRecord(user_id=user_id, movie_id= movie_id, download_time=common.get_time())
    obj.save()