#Python 3.6

import socket
from datetime import datetime

def run_server(host='', port=2222):
    # 建立一个socket.socket()类s
    with socket.socket() as s:
        # 设置s在服务端关闭后马上释放端口，避免Address already in use错误
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 绑定host和port
        s.bind((host, port))
        while 1:
            # 开始监听传入连接，可以挂起的最大连接数为5
            s.listen(5)
            # 接受连接，根据buffer_size不断读取内容
            connection, address = s.accept()
            r = ''
            buffer_size = 1024
            while 1:
                data = connection.recv(1024).decode('utf-8')
                r += data
                if len(data) < buffer_size:
                    break
                # 防止浏览器传空请求过来
                if len(r.split()) < 2:
                    continue
            # 最后取得的r是一个http请求头字符串，对其解析，然后使用sendall返回相应的内容  
            request = request_resolve(r)
            # 每次请求时打印时间，请求的方法和路径
            print(str(datetime.now())[:19], request.method, request.path)
            res = response(request)
            connection.sendall(res)
            connection.close()

def request_resolve(request):
    pass

if __name__ == '__main__':
    run_server()
