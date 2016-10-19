from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Country(Base):
    __tablename__ = 'country'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    # user_id = Column(Integer, ForeignKey('user.id'))
    # user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }

class Region(Base):
    __tablename__ = 'region'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    country_id = Column(Integer, ForeignKey('country.id'))
    country = relationship(Country)
    # user_id = Column(Integer, ForeignKey('user.id'))
    # user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }

class Brewery(Base):
    __tablename__ = 'brewery'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    country_id = Column(Integer, ForeignKey('country.id'))
    region_id = Column(Integer, ForeignKey('region.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    country = relationship(Country)
    region = relationship(Region)
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }

class Beer(Base):
    __tablename__ = 'beer'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    style = Column(String(80)) # eg. IPA, PALE ALE...
    abv = Column(Integer) # Alcohol By Volume
    ibu = Column(Integer) # International Bitterness Units
    country_id = Column(Integer, ForeignKey('country.id'))
    region_id = Column(Integer, ForeignKey('region.id'))
    brewery_id = Column(Integer, ForeignKey('brewery.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    country = relationship(Country)
    region = relationship(Region)
    brewery = relationship(Brewery)
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }


engine = create_engine('sqlite:///beercatalog.db')


Base.metadata.create_all(engine)