from src.database.models import Stuntman


class StuntmanService:
    @staticmethod
    def fetch_all_stuntmen(session):
        return session.query(Stuntman)

    @classmethod
    def fetch_stuntman_by_uuid(cls, session, uuid):
        print(f"Fetching stuntman with UUID: {uuid}")
        return cls.fetch_all_stuntmen(session).filter_by(
            uuid=uuid
        ).first()