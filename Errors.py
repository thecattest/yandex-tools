class ForbiddenError(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return f'Упс, возникла проблема с полуением данных :(\nОшибка: {self.error}'
