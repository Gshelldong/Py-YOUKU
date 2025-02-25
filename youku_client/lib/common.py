import hashlib
import json
import os.path
import struct
from conf import settings

def send_msg_back_dic(send_dict, client, file=None):
    data_bytes = json.dumps(send_dict).encode('utf-8')
    headers = struct.pack('i', len(data_bytes))
    client.send(headers)
    client.send(data_bytes)

    # 上传电影
    if file:
        with open(file, 'rb') as f:
            for line in f:
                client.send(line)

    # 接收服务端数据的过程
    headers = client.recv(4)
    print('headers', headers)
    data_len = struct.unpack('i', headers)[0]
    print('data_len: ',data_len)
    data_bytes = client.recv(data_len)
    back_dic = json.loads(data_bytes.decode('utf-8'))
    return  back_dic

def get_movie_list():
    if os.path.exists(settings.UPLOAD_FILES):
        movie_list = os.listdir(settings.UPLOAD_FILES)
        if movie_list:
            return movie_list

# 获取电影的MD5
def get_movie_md5(movie_path):
    md5 = hashlib.md5()

    movie_size = os.path.getsize(movie_path)
    # 截取电影4个位置截取10个bytes的数据
    current_index = [
        0, movie_size // 3, (movie_size //3 ) * 2, movie_size - 10
    ]

    with open(movie_path, 'rb') as f:
        for index in current_index:
            f.seek((index))
            data = f.read(10)
            md5.update(data)
    return md5.hexdigest()