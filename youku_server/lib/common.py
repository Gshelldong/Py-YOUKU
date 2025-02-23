import hashlib
import time
import json
import struct

def get_md5_pwd(password: str):
    md = hashlib.md5()
    md.update(password.encode('utf-8'))
    md.update('solt-123456'.encode('utf-8'))
    return md.hexdigest()

def get_time():
    now_time = time.strftime('%Y-%m-%d %X')
    return now_time

def send_data(send_dic, conn):
    data_bytes = json.dumps(send_dic).encode('utf-8')
    headers = struct.pack('i', len(data_bytes))
    conn.send(headers)
    conn.send(data_bytes)