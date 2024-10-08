from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow.fields import Nested, List, String
from src.database.models import Film


class FilmSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Film
        exclude = ['id']    # какие поля мы хотим игнорировать
        load_instance = True
        include_fk = True  # Если нужно включить связи с другими моделями

    cast = List(String(attribute="name"))
    # filmography = Nested('ActorSchema', many=True, exclude=('filmography',))

