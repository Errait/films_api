import uuid
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from src import db

cast_in_films = db.Table(
    'cast_in_films',
    db.Model.metadata,
    db.Column('film_id', db.Integer(), db.ForeignKey('films.id'), primary_key=True),
    db.Column('actor_id', db.Integer(), db.ForeignKey('actors.id'), primary_key=True)
)


class Film(db.Model):
    __tablename__ = 'films'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    release_date = db.Column(db.Date, index=True, nullable=False)
    uuid = db.Column(db.String(36), unique=True)
    description = db.Column(db.Text)
    distributed_by = db.Column(db.String(128), nullable=False)
    length = db.Column(db.Float)
    rating = db.Column(db.Float)
    is_released = db.Column(db.Boolean)

    # cast = relationship('Actor',
    #                     secondary='cast_in_films',
    #                     back_populates='filmography',)

    cast = relationship('Actor',
                        secondary=cast_in_films,
                        lazy=True,
                        backref=db.backref('filmography',
                                           lazy=True))

    def __init__(self, title, release_date, description, distributed_by, length, rating, cast=None):
        self.title = title
        self.release_date = release_date
        self.description = description
        self.distributed_by = distributed_by
        self.length = length
        self.rating = rating
        self.uuid = str(uuid.uuid4())
        if not cast:
            self.cast = []
        else:
            self.cast = cast

    def __repr__(self):
        return f'{self.title}'


class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    uuid = db.Column(db.String(36), unique=True)
    birthday = db.Column(db.Date, index=True, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)

    contacts = relationship("Contacts", back_populates='actor', lazy='dynamic')

    def __init__(self, name, birthday, is_active, filmography=None):
        self.name = name
        self.birthday = birthday
        self.is_active = is_active
        self.uuid = str(uuid.uuid4())
        if not filmography:
            self.filmography = []
        else:
            self.filmography = filmography

    def __repr__(self):
        return f'{self.name}'


class Stuntman(db.Model):
    __tablename__ = 'stuntmen'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    uuid = db.Column(db.String(36), unique=True)
    is_active = db.Column(db.Boolean, nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey('actors.id'), nullable=False)

    actor = relationship('Actor',
                         backref=db.backref('stuntman', uselist=False)
                         )

    def __init__(self, name, is_active, actor_id):
        self.name = name
        self.is_active = is_active
        self.actor_id = actor_id
        self.uuid = str(uuid.uuid4())

    def __repr__(self):
        return f'{self.name}'


class Contacts(db.Model):
    __tablename__ = 'Contacts'

    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('actors.id'), nullable=False)
    publicist_agent_info = db.Column(db.String(128))
    social_media = db.Column(db.String(128))

    actor = relationship('Actor', back_populates='contacts')

    def __init__(self, actor_id, social_media=None, publicist_agent_info=None):
        self.actor_id = actor_id
        self.social_media = social_media if social_media else 'unknown'
        self.publicist_agent_info = publicist_agent_info if publicist_agent_info else 'unknown'

    def __repr__(self):
        return f'{self.actor.name} - {self.social_media}, {self.publicist_agent_info}'


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    uuid = db.Column(db.String(36), unique=True)

    def __init__(self, username, email, password, is_admin=False):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.is_admin = is_admin
        self.uuid = str(uuid.uuid4())

    def __repr__(self):
        return f'User({self.username}, {self.email}, {self.uuid}'

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def find_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_user_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid).first()
