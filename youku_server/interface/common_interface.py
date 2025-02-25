from db import models
from lib import common, lock_file
from db import user_data


def register_interface(client_back_dic, conn):
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


def login_interface(client_back_dic: dict, conn):
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
            print("user_online => ",user_data.user_online)

            send_dic = {'flag': True, 'msg': '登陆成功!', 'session': session}

            new_notice = get_new_notice_interface()
            if new_notice:
                send_dic['new_notice'] = new_notice
        else:
            send_dic = {'flag': False, 'msg': '用户名或密码错误!'}
    common.send_data(send_dic, conn)


# 获取电影列表接口
@common.login_auth
def get_movie_list_interface(client_back_dic, conn):
    # 获取所有电影对象
    movie_obj_list = models.Movie.select()
    back_movie_list = []
    if movie_obj_list:
        # 过滤已经删除的电影
        for movie_obj in movie_obj_list:
            if not movie_obj.is_delete:
                if client_back_dic.get('movie_type') == 'all':
                    back_movie_list.append(
                        # [电影名称、是否免费、电影ID]
                        [movie_obj.name, '免费' if movie_obj.is_free else "收费", movie_obj.id]
                    )
                elif client_back_dic.get('movie_type') == 'free':
                    # 判断哪些是免费的
                    if movie_obj.is_free:
                        back_movie_list.append(movie_obj.name, '免费', movie_obj.id)
                else:
                    if not movie_obj.is_free:
                        back_movie_list.append(
                            [movie_obj.name, '收费', movie_obj.id]
                        )
    if back_movie_list:
        send_dic = {'flag': True, 'back_movie_list': back_movie_list}
    else:
        send_dic = {'flag': False, 'msg': '没有的电影!'}
    common.send_data(send_dic, conn)

def get_new_notice_interface():
    # 获取所有的公告
    notice_obj_list = models.Notice.select()
    if not notice_obj_list:
        return False

    # 2.对发布的时间或者id进行排序，获取最新的一条公告
    notice_desc_list = sorted(
        # [notice_obj, notice_obj,notice_obj。。。]
        # 选择1：根据ID notice_obj_list, key=lambda notice_obj: notice_obj.id
        # 选择2：根据时间
        notice_obj_list, key=lambda notice_obj: notice_obj.create_time, reverse=True
    )

    new_notice = {
        'title': notice_desc_list[0].title,
        'content': notice_desc_list[0].content
    }

    return new_notice