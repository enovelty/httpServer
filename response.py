#Python 3.6

import sys, os

class Response():
    #对 HTTP 报文进行切片
    def __init__(self, m):
        self.content = m
        self.method = m.split()[0]
        self.path = m.split()[1]
        self.body = m.split('\r\n\r\n', 1)[1]
        self.response = ''
        self.file_type = self.path.split('.')[1]

    def resolve(self):
        try:
            #获取文件路径
            full_path = os.getcwd() + self.path
            print(full_path)
            # 如果路径不存在
            if not os.path.exists(full_path):
                self.handle_error("'{0}' not found".format(self.path))
            #如果该路径是一个文件
            elif os.path.isfile(full_path):
                self.handle_file(full_path)
            #如果该路径不是一个文件
            else:
                self.handle_error("Unknown object '{0}'".format(self.path))
        except Exception as msg:
            self.handle_error(msg)

    def handle_file(self, full_path):
        #处理 html 文件
        if self.file_type == 'html':
            self.response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'
            try:  
                with open(full_path, 'r', encoding='UTF-8') as file:
                    self.response += file.read()
                self.response = self.response.encode(encoding='utf-8')
            except IOError as msg:
                msg = "'{0}' cannot be read: {1}".format(self.path, msg)
                self.handle_error(msg)
        #处理其他文件
        else:
            self.response = 'HTTP/1.1 200 OK\r\nContent-Type: image/jpg\r\n\r\n'
            try:  
                with open(full_path, 'rb') as file:
                    self.response = bytes(self.response, 'utf-8') + file.read()
            except IOError as msg:
                msg = "'{0}' cannot be read: {1}".format(self.path, msg)
                self.handle_error(msg)

    Error_Page = """HTTP/1.1 404 Not Found
    Content-Type: text/html

    <html>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <body>
    <h1>服务器无法解析： {path}</h1>
    <p>{msg}</p>
    </body>
    </html>
    """

    def handle_error(self, msg):
        self.response = self.Error_Page.format(path= self.path,msg= msg)
        self.response = self.response.encode(encoding='utf-8')