from core import admin,user

"""
用户:
	1.注册
	2.登录
	3.充会员
	4.查看视频
	5.下载免费视频
	6.下载会员视频
	7.查看观影记录

细分：
  管理员功能
  用户功能
  退出
"""

func_dic = {
    '1': admin.admin_view,
    '2': user.user_view
}

def run():
    while True:
        print(
            """
              1. 管理员
              2. 用户
              3. q退出
            """
        )
        choice = input("请选择功能: ").strip()
        if choice == 'q':
            break
        if choice not in func_dic:
            continue

        # 直接运行函数中的内容
        func_dic.get(choice)()
