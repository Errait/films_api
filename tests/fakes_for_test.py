import datetime

date = '2002-01-02'


class FakeFilm:
    title = 'Fake Film'
    distributed_by = 'Fake'
    release_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    description = 'Fake description'
    length = 101
    rating = 8.0
    cast = []


class FakeActor:
    name = 'Fake Actor'
    birthday = '2002-01-02'
    is_active = 'false'
    filmography = []


class FakeStuntman:
    name = 'Fake Stuntman',
    is_active = Trueh
    actors_id = 2
