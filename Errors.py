class BaseError(Exception):
    '''Base class error for init error Classes'''
    def __init__(self, error):
        self.error = error
        super().__init__(self.error)


class ForbiddenError(BaseError):
    '''Raises when browser attract 403 error'''

    def __init__(self, error):
        super().__init__(error)

    def __str__(self):
        return f'Упс, возникла проблема с полуением данных :(\nОшибка: {self.error}'


class LostTaskError(BaseError):
    '''Raises when search_tasks function can't get result'''

    def __init__(self, error):
        super().__init__(error)

    def __str__(self):
        return f'Упс, не удалось найти задачу :(\nОшибка: {self.error}'
