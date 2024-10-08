"""
SELECT QUERIES
"""
from sqlalchemy import and_

from src import db, app
from src.database import models

with app.app_context():
    films = db.session.query(models.Film).order_by(models.Film.rating.desc()).all()
    # print(*[i for i in films], sep='\n')

    harry_potter_and_cha_s = db.session.query(models.Film).filter(
        models.Film.title == 'Harry Potter and Chamber of Secrets'
    ).first()

    harry_potter_and_priz_az = db.session.query(models.Film).filter_by(
        title='Harry Potter and the Prizoner of Azkaban'
    ).first()

    and_statement_harry_potter = db.session.query(models.Film).filter(
        models.Film.title != 'Harry Potter and Chamber of Secrets',
        models.Film.rating >= 7.8
    ).all()

    # and_statement_harry_potter = db.session.query(models.Film).filter(
    #     models.Film.title != 'Harry Potter and Chamber of Secrets'
    # ).filter(
    #     models.Film.rating >= 7.8).all()

    # and_statement_harry_potter = db.session.query(models.Film).filter(
    #     and_(
    #         models.Film.title != 'Harry Potter and Chamber of Secrets',
    #         models.Film.rating >= 7.8
    #     )
    # ).all()

    # print(*[i for i in and_statement_harry_potter], sep='\n')

    # deathly_hallows = db.session.query(models.Film).filter(
    #     models.Film.title.like('%Deathly Hallows%')
    # ).all()
    # print(*[i for i in deathly_hallows], sep='\n')

    deathly_hallows = db.session.query(models.Film).filter(
        models.Film.title.ilike('%Deathly Hallows%')
    ).all()
    # print(*[i for i in deathly_hallows], sep='\n')

    harry_potter_sorted_by_length = db.session.query(models.Film).filter(
        models.Film.length.in_([146, 161])).all()
    # print(*[i for i in harry_potter_sorted_by_length], sep='\n')

    # ~ == in not
    harry_potter_sorted_by_length_2 = db.session.query(models.Film).filter(
        ~models.Film.length.in_([146, 161]))[:2]  # срезы
    # print(*[i for i in harry_potter_sorted_by_length_2], sep='\n')

    '''
    QUERYING WITH JOINS
    '''
    films_with_actors = db.session.query(models.Film).join(models.Film.cast).all()
    print(*[i for i in films_with_actors], sep='\n')