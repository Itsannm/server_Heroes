from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

# Create a SQLAlchemy instance with custom metadata
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)

# Define the Hero model
class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'
    serialize_rules = ('-powers.hero',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    super_name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    powers = db.relationship('HeroPower', back_populates='hero')

    def __repr__(self):
        return f'<Hero {self.name} aka {self.super_name}>'

# Define the Power model
class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'
    serialize_rules = ('-heroes.power',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    heroes = db.relationship('HeroPower', back_populates='power')

    def __repr__(self):
        return f'<Power {self.name} aka {self.description}>'

# Define the HeroPower model
class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'heropowers'
    serialize_rules = ('-hero.powers', '-power.heroes')

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(10))

    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    hero = db.relationship('Hero', back_populates='powers')
    power = db.relationship('Power', back_populates='heroes')

    @validates('strength')
    def validate_strength(self, key, strength):
        valid_strengths = ['Strong', 'Weak', 'Average']
        if strength not in valid_strengths:
            raise AssertionError("invalid strength value")
        return strength
