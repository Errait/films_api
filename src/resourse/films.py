from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.orm import joinedload, selectinload

from src import db

from src.database.models import Film
from src.resourse.auth import token_required
from src.schemas.films import FilmSchema
from src.services.film_service import FilmService

# def get_all_films():
#     return [
#         {
#             'id': '1',
#             'title': 'Harry Potter and the Philosopher\'s Stone',
#             'release_data': 'November 4, 2001',
#         },
#         {
#             'id': '2',
#             'title': 'Harry Potter and Chamber of Secrets',
#             'release_data': 'November 3, 2002',
#         },
#         {
#             'id': '3',
#             'title': 'Harry Potter and Prizoner of Azkaban',
#             'release_data': 'June 4, 2004',
#         },
#         {
#             'id': '4',
#             'title': 'Harry Potter and the Goblet of Fire',
#             'release_data': 'November 6, 2005',
#         },
#         {
#             'id': '5',
#             'title': 'Harry Potter and The Order of the Phoenix',
#             'release_data': 'July 19, 2007',
#         },
#         {
#             'id': '6',
#             'title': 'Harry Potter and the Half_Blood Prince',
#             'release_data': 'July 16, 2009',
#         },
#         {
#             'id': '7',
#             'title': 'Harry Potter and the Deathly Hallows part 1',
#             'release_data': 'November 18, 2010',
#         },
#         {
#             'id': '8',
#             'title': 'Harry Potter and the Deathly Hallows part 2',
#             'release_data': 'July 13, 2011',
#         },
#     ]

# def get_film_by_uuid(uuid: str) -> dict:
#     films = get_all_films()
#     film = list(filter(lambda f: f['id'] == uuid, films))
#     return film[0] if film else {}

# def create_films(film_json:dict) -> List[dict]:
#     films = get_all_films()
#     films.append(film_json)
#     return films

# film = db.session.query(Film).filter_by(uuid=uuid).first()
# if not film:
#     return '', 400
# film_json = request.json
# title = film_json.get('title')
# release_date = datetime.datetime.strptime(
#     film_json.get('release_date').date(),'%B %d, %Y') \
#     if film_json.get('release_date') else None
# distributed_by = film_json.get('distributed_by')
# description = film_json.get('description')
# length = film_json.get('length')
# rating = film_json.get('rating')
# if title:
#     film.title = title
# elif release_date:
#     film.release_date = release_date
# elif distributed_by:
#     film.distributed_by = distributed_by
# elif description:
#     film.description = description
# elif length:
#     film.length = length
# elif rating:
#     film.rating = rating
# film_json = request.json
# if not film_json:
#     return {'message': 'Wrong data'}, 400
# try:
#     release_date = datetime.datetime.strptime(
#         film_json['release_date'],'%Y-%m-%d').date()
#
#     film = Film(
#         title=film_json['title'],
#         release_date=release_date,
#         # release_date=film_json['release_date'],
#         distributed_by=film_json['distributed_by'],
#         description=film_json.get('description'),
#         length=film_json.get('length'),
#         rating=film_json.get('rating')
#     )
#     db.session.add(film)
#     db.session.commit()
# except ValueError:
#     return {'message': 'Invalid date format.'}, 400
# except KeyError as e:
#     return {'message': f'Missing key: {str(e)}'}, 400
# return {'message': 'Created successfully'}, 201

# def put(self, uuid):
#     film_json = request.json
#     if not film_json:
#         return {'message': 'Wrong data'}, 400
#     try:
#         db.session.query(Film).filter_by(uuid=uuid).upgrade(
#             dict(
#                 title=film_json['title'],
#                 release_date=datetime.datetime.strptime(
#                     film_json['release_date'], '%B %d, %Y').date(),
#                 distributed_by=film_json['distributed_by'],
#                 description=film_json.get('description'),
#                 length=film_json.get('length'),
#                 rating=film_json.get('rating')
#             )
#         )
#         db.session.commit()
#     except ValueError:
#         return {'message': 'Invalid date format.'}, 400
#     except KeyError as e:
#         return {'message': f'Missing key: {str(e)}'}, 400
#     return {'message': 'Upgrade successfully'}, 200


class FilmListApi(Resource):
    film_schema = FilmSchema()
    film_schema_partial = FilmSchema(partial=True)

    # @token_required
    def get(self, uuid=None):
        if not uuid:
            films = FilmService.fetch_all_films(db.session).options(
                selectinload(Film.cast)
            ).all()
            return self.film_schema.dump(films, many=True), 200

        film = FilmService.fetch_film_by_uuid(db.session, uuid)

        if not film:
            return '', 404
        return self.film_schema.dump(film), 200

    def post(self):
        try:
            film = self.film_schema.load(request.json, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400

        db.session.add(film)
        db.session.commit()
        return self.film_schema.dump(film), 201

    def patch(self, uuid):
        film = FilmService.fetch_film_by_uuid(db.session, uuid)

        if not film:
            return {'message': 'Film not found'}, 404
        try:
            film = self.film_schema_partial.load(request.json, instance=film, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400

        db.session.commit()
        return self.film_schema.dump(film), 200

    def delete(self, uuid):
        film = FilmService.fetch_film_by_uuid(db.session, uuid)

        if not film:
            return '', 400

        db.session.delete(film)
        db.session.commit()
        return '', 204

    def put(self, uuid):
        film = FilmService.fetch_film_by_uuid(db.session, uuid)

        if not film:
            return {'message': 'Film not found'}, 400

        actor_json = request.json.get('actors')

        if not actor_json or not isinstance(actor_json, list):
            return {'message': 'Invalid actors data'}, 400

        actors_to_add = []

        for actor_uuid in actor_json:
            actor = db.session.query(Film).filter_by(uuid=actor_uuid).first()
            if not actor:
                return {'message': f'Actor with UUID {actor_uuid} not found'}, 404
            if actor not in film.cast:
                actors_to_add.append(actor.name)
            else:
                return {'message': f'Actor "{actor.name}" already in film\'s cast'}, 400

        film.cast.extend(actors_to_add)
        db.session.add(film)
        db.session.commit()
        return {'message': 'Upgrade successfully'}, 200

    def putt(self, uuid):
        film = FilmService.fetch_film_by_uuid(db.session, uuid)

        if not film:
            return '', 404
        try:
            film = self.film_schema.load(request.json, instance=film, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400

        db.session.add(film)
        db.session.commit()
        return self.film_schema.dump(film), 200
