
class Res(object):
    success = True
    code = 2000
    message = ''
    data = {}

    def serialize(self):
        return {
            'success': self.success,
            'code': self.code,
            'message': self.message,
            'data': self.data
        }


    """ 正确 """
    @staticmethod
    def ok(code, message, data):
        res = Res()
        res.code = code
        res.message = message
        res.data = data
        return res.serialize()

    """ 错误 """
    @staticmethod
    def error(code, message, data):
        res = Res()
        res.success = False
        res.code = code
        res.message = message
        res.data = data
        return res.serialize()

