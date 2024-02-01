class Vacancy:

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.salary = kwargs['salary']
        self.experience = kwargs['experience']
        self.employer = kwargs['employer']
        self.url_vacancy = kwargs['url_vacancy']
        self.platform = kwargs['platform']