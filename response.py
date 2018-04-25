#Python 3.6

import sys, os

# class ServerException(Exception):
#     pass

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
        # path = request.resolve_path()[0]
        # return route_dict.get(path, error_handle)(request)
        try:
            #获取文件路径
            full_path = os.getcwd() + self.path
            print(full_path)
            # 如果路径不存在
            if not os.path.exists(full_path):
                # raise ServerException("'{0}' not found".format(self.path))
                self.handle_error("'{0}' not found".format(self.path))
            #如果该路径是一个文件
            elif os.path.isfile(full_path):
                self.handle_file(full_path)
            #如果该路径不是一个文件
            else:
                # raise ServerException("Unknown object '{0}'".format(self.path))
                self.handle_error("Unknown object '{0}'".format(self.path))
        except Exception as msg:
            self.handle_error(msg)

    def handle_file(self, full_path):
        #处理 html 文件
        if self.file_type == 'html':
            self.response = """HTTP/1.1 200 OK
            Content-Type: text/html

            """
            try:  
                with open(full_path, 'r', encoding='UTF-8') as file:
                    self.response += file.read()
                self.response = self.response.encode(encoding='utf-8')
            except IOError as msg:
                msg = "'{0}' cannot be read: {1}".format(self.path, msg)
                self.handle_error(msg)
        #
        else:
            self.response = """HTTP/1.1 200 OK
            Content-Type: image/jpg
            
            """
            try:  
                with open(full_path, 'rb') as file:
                    self.response = bytes(self.response, 'utf-8')
                    self.response += file.read()
                    # self.response = bytes(self.response, 'utf-8') + file.read()
                    # self.response += str(file.read(), encoding = 'utf-8')
                # self.response = self.response.encode()
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

    # def route_index(request):
    #     print('Request: ', request.content)
    #     # response = """HTTP/1.1 200 OK
    #     # Content-Type: text/html

    #     #     """
    #     response = request.response
    #     print('Response: ', response)
    #     return response.encode(encoding='utf-8')

# def error_handle(mes):
#     print('404 Not fund \n %s' % mes)

# route_dict = {
#     '/': route_index,
# }

        # <!DOCTYPE html>
        # <html lang="en">
        # <head>
        #     <meta charset="UTF-8">
        #     <title>INDEX
        #     中文</title>
        # </head>
        # <body background="/dif1.jpg">
        # <h1>Index Page
        # 中文</h1>
        # <img src="dif1.jpg" />
        # </body>
        # </html>
