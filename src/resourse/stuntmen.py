from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from src import db
from src.schemas.stuntmen import StuntmanSchema
from src.database.models import Stuntman


class StuntmenApi(Resource):
    stuntman_schema = StuntmanSchema()
    stuntman_schema_partial = StuntmanSchema(partial=True)

    def get(self, uuid=None):
        if not uuid:
            stuntmen = db.session.query(Stuntman).all()
            return self.stuntman_schema.dump(stuntmen, many=True), 200
        stuntman = db.session.query(Stuntman).filter_by(uuid=uuid).first()
        if not stuntman:
            return '', 404
        return self.stuntman_schema.dump(stuntman), 200

    def post(self):
        try:
            stuntman = self.stuntman_schema.load(request.json, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400
        db.session.add(stuntman)
        db.session.commit()
        return self.stuntman_schema.dump(stuntman), 201

    def patch(self, uuid):
        stuntman = db.session.query(Stuntman).filter_by(uuid=uuid).first()
        if not stuntman:
            return {'message': 'Film not found'}, 404
        try:
            stuntman = self.stuntman_schema_partial.load(request.json,
                                                         instance=stuntman,
                                                         session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400

        db.session.commit()
        return {'message': 'Upgrade successfully'}, 200

    def delete(self, uuid):
        stuntman = db.session.query(Stuntman).filter_by(uuid=uuid).first()
        if not stuntman:
            return '', 400
        db.session.delete(stuntman)
        db.session.commit()
        return '', 204

    def put(self, uuid):
        stuntman = db.session.query(Stuntman).filter_by(uuid=uuid).first()
        if not stuntman:
            return '', 404
        try:
            stuntman = self.stuntman_schema.load(request.json, instance=stuntman, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400
        db.session.add(stuntman)
        db.session.commit()
        return self.stuntman_schema.dump(stuntman), 200