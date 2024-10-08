from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow.fields import Nested
from src.schemas.actors import ActorSchema
from src.database.models import Stuntman


class StuntmanSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Stuntman
        load_instance = True  # Загрузка объекта при десериализации
        include_fk = True  # Если нужно включить связи с другими моделями

    actor = Nested(ActorSchema, only=["name"])