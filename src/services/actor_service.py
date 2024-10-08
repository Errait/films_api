from src.database.models import Actor


class ActorService:
    @staticmethod
    def fetch_all_actors(session):
        return session.query(Actor)

    @classmethod
    def fetch_actor_by_uuid(cls, session, uuid):
        return cls.fetch_all_actors(session).filter_by(
            uuid=uuid
        ).first()