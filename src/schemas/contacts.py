from marshmallow.fields import Nested
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from src.database.models import Contacts


class ContactSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Contacts
        load_instance = True
        include_fk = True

    actor = Nested("ActorSchema", attribute="name")