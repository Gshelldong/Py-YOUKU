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
    pass
    # todo 客户端下载免费电影的函数实现