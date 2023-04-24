# coding: utf-8

class Response(dict):

    def __init__(self, code=0, message="ok", data=None):
        super(Response, self).__init__(code=code, message=message, data=data)

    @property
    def code(self):
        return self["code"]

    @code.setter
    def code(self, value):
        """
        code:
            - 0: ok
            - 99999: common error
        :param value:
        :return:
        """
        self["code"] = value

    @property
    def message(self):
        return self["message"]

    @message.setter
    def message(self, value):
        self["message"] = value

    @property
    def data(self):
        return self["data"]

    @data.setter
    def data(self, value):
        self["data"] = value


ParamsErrResponse = Response(99999, "请求参数异常")
UnknownErrResponse = Response(99999, "服务发生未知异常")
