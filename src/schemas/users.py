from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow.fields import Nested, List, String
from src.database.models import User


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ('id', 'is_admin')
        load_instance = True
        load_only = ('password',)