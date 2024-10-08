from datetime import date

from src import db, app
from src.database.models import Actor


def populate_actors():
    daniel_radcliffe = Actor(
        name=' Daniel Radcliffe',
        birthday=date(1989, 7, 23),
        is_active=True,
    )
    rupert_grint = Actor(
        name='Rupert Grint',
        birthday=date(1988, 8, 24),
        is_active=False,
    )
    emma_watson = Actor(
        name='Emma Watson',
        birthday=date(1990, 4, 15),
        is_active=True
    )
    alan_rickman = Actor(
        name='Alan Rickman',
        birthday=date(1946, 2, 21),
        is_active=False
    )
    jason_isaacs = Actor(
        name='Jason Isaacs',
        birthday=date(1963, 6, 6),
        is_active=True
    )
    gary_oldman = Actor(
        name='Gary Oldman',
        birthday=date(1958, 3, 21),
        is_active=True
    )
    robert_pattinson = Actor(
        name='Robert Pattinson',
        birthday=date(1986, 5, 13),
        is_active=True,
    )
    evanna_lynch = Actor(
        name='Evanna Lynch',
        birthday=date(1991, 8, 16),
        is_active=True,
    )

    db.session.add(daniel_radcliffe)
    db.session.add(rupert_grint)
    db.session.add(alan_rickman)
    db.session.add(emma_watson)
    db.session.add(jason_isaacs)
    db.session.add(gary_oldman)
    db.session.add(robert_pattinson)
    db.session.add(evanna_lynch)

    db.session.commit()
    db.session.close()


if __name__ == '__main__':
    print('Populating db...')
    with app.app_context():
        db.create_all()

        populate_actors()
        print('Successfully populated!')