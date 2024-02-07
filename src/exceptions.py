class ResponseError(Exception):
    def __init__(self, *args):
        self.message = args[0] if args else 'Ошибка запроса'

    def __str__(self):
        return self.message