```text


服务端:
    1.conf: 配置文件
        - settings

    2.db: 模型表类
        - models

    3.download_files: 客户端上传的文件存放目录

    4.interface: 接口层
        - common_interface
        - admin_interface
        - user_interface

    5.lib: 公共方法
        - common

    6.orm: 操作数据库

    7.tcp_server: 套接字服务端
        - socket_server

    8.start：启动文件

项目需求
'''
管理员:
	1.注册
	2.登录
	3.上传视频
	4.删除视频
	5.发布公告

用户:
	1.注册
	2.登录
	3.充会员
	4.查看视频
	5.下载免费视频
	6.下载会员视频
	7.查看观影记录
'''

# 然后再从models着手开始。
数据库表的设计:

youku_demo

    User:
        id, name, pwd, is_vip, is_locked, user_type, register_time

    Movie:
        id, name, path, is_free, file_md5, user_id, is_delete, upload_time

    Notice:
        id, title, content, user_id, create_time

    DownloadRecord:
        id, user_id, movie_id, download_time


1、把表通过orm创建相关的表类
2、先把主要的部分监听和run写好，客户端和服务端简单的通讯
3、客户端打印功能菜单，搭建项目的主要功能函数框架
```
