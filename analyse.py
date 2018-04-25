# Python 3.6

from urllib.parse import unquote, quote

class Analyse:
    #对 HTTP 报文进行切片
    def __init__(self, m):
        self.content = m
        self.method = m.split()[0]
        self.path = m.split()[1]
        self.body = m.split('\r\n\r\n', 1)[1]
        self.response = ''

    @property
    def headers(self):
        #获取首部行的 list
        header_content = self.content.split('\r\n\r\n', 1)[0].split('\r\n')[1:]
        #quote 对 url 中的特殊字符进行编码
        result = {}
        for line in header_content:
            k, v = line.split(': ')
            result[quote(k)] = quote(v)
        return result

    @staticmethod
    def resolve_parameter(parameters):
        args = parameters.split('&')
        query = {}
        for arg in args:
            k, v = arg.split('=')
            query[k] = unquote(v)
        return query

    def form_body(self):
        return self.resolve_parameter(self.body)

    def do_GET(self):
    #这里要处理两个异常，一个是读入路径时可能出现的异常，一个是读入路径后若不是文件，要作为异常处理
        try:
            #获取文件路径
            full_path = os.getcwd() + self.path
            # 如果路径不存在
            if not os.path.exists(full_path):
                raise ServerException("'{0}' not found".format(self.path))
            #如果该路径是一个文件
            elif os.path.isfile(full_path):
                self.handle_file(full_path)
            #如果该路径不是一个文件
            else:
                raise ServerException("Unknown object '{0}'".format(self.path))
        except Exception as msg:
            self.handle_error(msg)

    #解析使用 GET 方法的表单
    def resolve_path(self):
        index = self.path.find('?')
        if index == -1:
            return self.path, {}
        else:
            path, query_string = self.path.split('?', 1)
            query = self.resolve_parameter(query_string)
            return path, query

