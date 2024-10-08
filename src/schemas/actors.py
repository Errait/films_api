from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow.fields import Nested, List, String

from src.schemas.contacts import ContactSchema
from src.database.models import Actor, Film, Contacts


class ActorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Actor
        load_instance = True  # Загрузка объекта при десериализации
        include_fk = True  # Если нужно включить связи с другими моделями

    filmography = List(String(attribute="title"))
    contacts = List(Nested(ContactSchema, only=["social_media", "publicist_agent_info"]))
