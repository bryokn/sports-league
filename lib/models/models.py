import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = sqlalchemy.orm.declarative_base()
class Team(Base):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    coach_id = Column(Integer, ForeignKey('coaches.id'))
    coach = relationship("Coach", back_populates="teams")
    players = relationship("Player", back_populates="team")
    home_matches = relationship('Match', foreign_keys='Match.home_team_id', back_populates='home_team')
    away_matches = relationship('Match', foreign_keys='Match.away_team_id', back_populates='away_team')

class Coach(Base):
    __tablename__ = 'coaches'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    contact_info = Column(String)
    teams = relationship("Team", back_populates="coach")

class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    position = Column(String)
    contact_info = Column(String)
    team_id = Column(Integer, ForeignKey('teams.id'))
    team = relationship("Team", back_populates="players")

class TeamCaptain(Base):
    __tablename__ = 'team_captains'
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    player = relationship("Player")
    team_id = Column(Integer, ForeignKey('teams.id'))

class Match(Base):
    __tablename__ = 'matches'
    id = Column(Integer, primary_key=True)
    date_time = Column(DateTime)
    venue_id = Column(Integer, ForeignKey('venues.id'))
    venue = relationship("Venue")
    home_team_id = Column(Integer, ForeignKey('teams.id'))
    home_team = relationship("Team", foreign_keys=[home_team_id], back_populates='home_matches')
    away_team_id = Column(Integer, ForeignKey('teams.id'))
    away_team = relationship("Team", foreign_keys=[away_team_id], back_populates='away_matches')
    home_team_score = Column(Integer)
    away_team_score = Column(Integer)

class Venue(Base):
    __tablename__ = 'venues'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)
    availability_schedule = Column(String)

engine = create_engine('sqlite:///hockey.db')
Base.metadata.create_all(engine)
