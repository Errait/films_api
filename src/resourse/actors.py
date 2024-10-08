from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.orm import selectinload

from src import db
from src.schemas.actors import ActorSchema
from src.database.models import Actor, Film


class ActorListApi(Resource):
    actor_schema = ActorSchema()
    actor_schema_partial = ActorSchema(partial=True)

    def get(self, uuid=None):
        if not uuid:
            actors = db.session.query(Actor).options(
                selectinload(Actor.filmography)
            ).all()
            return self.actor_schema.dump(actors, many=True), 200
        actor = db.session.query(Actor).filter_by(uuid=uuid).first()
        if not actor:
            return '', 404
        return self.actor_schema.dump(actor), 200

    def post(self):
        try:
            actor = self.actor_schema.load(request.json, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400
        db.session.add(actor)
        db.session.commit()
        return self.actor_schema.dump(actor), 201

    # def put(self, uuid):
    #     actor_json = request.json
    #     if not actor_json:
    #         return {'message': 'Wrong data'}, 404
    #     try:
    #         db.session.query(Actor).filter_by(uuid=uuid).update(
    #             dict(
    #                 name=actor_json['name'],
    #                 birthday=datetime.strptime(
    #                     actor_json['birthday'], '%B %d, %Y').date(),
    #                 is_active=actor_json['is_active']
    #             )
    #         )
    #         db.session.commit()
    #     except ValueError:
    #         return {'message': 'Invalid date format.'}, 400
    #     except KeyError as e:
    #         return {'message': f'Missing key: {str(e)}'}, 400
    #     return {'message': 'Upgrade successfully'}, 200

    def patch(self, uuid):
        actor = db.session.query(Actor).filter_by(uuid=uuid).first()
        if not actor:
            return {'message': 'Actor not found'}, 404
        try:
            actor = self.actor_schema_partial.load(request.json, instance=actor, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400

        db.session.commit()
        return {'message': 'Upgrade successfully'}, 200

    def delete(self, uuid):
        actor = db.session.query(Actor).filter_by(uuid=uuid).first()
        if not actor:
            return '', 400
        db.session.delete(actor)
        db.session.commit()
        return '', 204

    def put(self, uuid):
        actor = Actor.query.filter_by(uuid=uuid).first()
        if not actor:
            return {'message': 'Actor not found'}, 400

        try:
            data = self.actor_schema_partial.load(request.json, instance=actor, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400

        film_json = request.json.get('films')
        if film_json and isinstance(film_json, list):
            films_to_add = []
            for film_uuid in film_json:
                film = Film.query.filter_by(uuid=film_uuid).first()
                if not film:
                    return {'message': f'Film with UUID {film_uuid} not found'}, 404
                if film not in actor.filmography:
                    films_to_add.append(film)
                else:
                    return {'message': f'Film "{film.title}" already in actor\'s filmography'}, 400
            actor.filmography.extend(films_to_add)

        db.session.commit()
        return {'message': 'Upgrade successfully'}, 200