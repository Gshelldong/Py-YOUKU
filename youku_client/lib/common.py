import json
import struct

def send_msg_back_dic(send_dict, client):
    data_bytes = json.dumps(send_dict).encode('utf-8')
    headers = struct.pack('i', len(data_bytes))
    client.send(headers)
    client.send(data_bytes)

    # 接收服务端数据的过程
    headers = client.recv(4)
    data_len = struct.unpack('i', headers)[0]
    print('data_len: ',data_len)
    data_bytes = client.recv(data_len)
    back_dic = json.loads(data_bytes.decode('utf-8'))
    return  back_dic