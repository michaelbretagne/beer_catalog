from sqlalchemy import Table, Column, ForeignKey, Integer, String
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
    image = Column(String(80), default="static/img/uploaded_images/not_available.jpg")
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
    image = Column(String(80), default="static/img/uploaded_images/not_available.jpg")
    name = Column(String(80), nullable=False)
    style = Column(String(80)) # eg. IPA, PALE ALE...
    abv = Column(Integer) # Alcohol By Volume
    ibu = Column(Integer) # International Bitterness Units
    description = Column(String(700)) # Description of the beer
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
            'style': self.style,
            'abv': self.abv,
            'ibu': self.ibu,
            'description': self.description,
        }

class Rating(Base):
    __tablename__ = 'rating'

    id = Column(Integer, primary_key=True)
    num_of_stars = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey('user.id'))
    beer_id = Column(Integer, ForeignKey('beer.id'))
    beer = relationship(Beer)
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'num_of_stars': self.num_of_stars,
            'id': self.id,
        }


engine = create_engine('sqlite:///beercatalog.db')


Base.metadata.create_all(engine)