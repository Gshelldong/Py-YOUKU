import os.path

from lib import common
from db import models
from conf import settings


@common.login_auth
def upload_movie_interface(client_back_dic, conn):
    print('有用户在上传电影...')

    # 确保电影的名称是唯一的 随机字符加电影名称
    movie_name = common.get_random_code() + client_back_dic.get('movie_name')
    movie_size = client_back_dic.get('file_size')
    movie_path = os.path.join(
        settings.DOWNLOAD_PATH, movie_name
    )

    # 接收上传的文件
    data_recv = 0
    with open(movie_path, mode='wb') as f:
        while data_recv < movie_size:
            data = conn.recv(1024)
            f.write(data)
            data_recv += len(data)

    # 把电影数据保存到mysql中
    move_obj = models.Movie(
        name=movie_name,
        file_md5=client_back_dic.get('file_md5'),
        is_free=client_back_dic.get('is_free'),
        is_delete=0,
        path=movie_path,
        user_id=client_back_dic.get('user_id'),
        upload_time=common.get_time()
    )

    move_obj.save()

    send_dic = {
        'flag': True, 'msg': f'{client_back_dic.get("movie_name")} 上传成功!'
    }
    print('电影上传完了.......')
    common.send_data(send_dic, conn)


@common.login_auth
def check_movie_interface(client_back_dic, conn):
    file_md5 = client_back_dic.get('file_md5')
    movie_list = models.Movie.select(file_md5=file_md5)
    if movie_list:
        print('电影已经存在!')
        send_dic = {
            'flag': False, 'msg': '电影已经存在了!'
        }
    else:
        print('服务端没有此记录,可以上传!')
        send_dic = {
            'flag': True, 'msg': '电影可以上传!'
        }
    common.send_data(send_dic, conn)


def delete_movie_interface(client_back_dic, conn):
    movie_id = client_back_dic.get('movie_id')
    movie_obj_select = models.Movie.select(id=movie_id)
    print('movie_obj_select - ', movie_obj_select)
    movie_obj = movie_obj_select[0]
    movie_obj.is_delete = 1
    movie_obj.sql_update()

    send_dic = {
        'flag': True, 'msg': '电影删除成功!'
    }
    common.send_data(send_dic, conn)

@common.login_auth
def put_notice_interface(client_back_dic, conn):
    title = client_back_dic.get('title')
    content = client_back_dic.get('content')
    user_id = client_back_dic.get('user_id')

    notice_obj = models.Notice(title = title, content = content, user_id = user_id, create_time = common.get_time())

    notice_obj.save()

    send_dic = {
        'msg': '公告发布成功!'
    }

    common.send_data(send_dic, conn)
