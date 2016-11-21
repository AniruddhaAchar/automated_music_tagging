from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, REAL
from sqlalchemy.orm import sessionmaker

sleep_engine = create_engine('sqlite:///E:\\programming\\python\\Spotify_data_extraction\\sleep_tracks.db', echo=False)
workout_engine = create_engine('sqlite:///E:\\programming\\python\\Spotify_data_extraction\\workout_tracks.db',
                               echo=False)
dinner_engine = create_engine('sqlite:///E:\\programming\\python\\Spotify_data_extraction\\dinner_tracks.db',
                              echo=False)
party_engine = create_engine('sqlite:///E:\\programming\\python\\Spotify_data_extraction\\party_tracks.db', echo=False)
engine = None
Base = declarative_base()


class Tracks(Base):
    __tablename__ = 'tracks'
    id = Column(String, primary_key=True)
    name = Column(String)
    uri = Column(String)
    artist = Column(String)
    acousticness = Column(REAL)
    danceability = Column(REAL)
    duration_ms = Column(Integer)
    energy = Column(REAL)
    instrumentalness = Column(REAL)
    key = Column(Integer)
    liveness = Column(REAL)
    loudness = Column(REAL)
    mode = Column(Integer)
    speechiness = Column(REAL)
    tempo = Column(REAL)
    time_signature = Column(Integer)
    valence = Column(REAL)


Session = sessionmaker(bind=engine)
session = Session()


def Create_table():
    Base.metadata.create_all(engine)


def addTrack(id, name, uri, artist, acousticness, danceability, duration_ms, energy, instrumentalness, key, liveness,
             mode, speechiness, tempo, time_signature, valence, loudness):
    print("Here is a track")

    track = Tracks(id=id, uri=uri, name=name, artist=artist, acousticness=acousticness, danceability=danceability,
                   duration_ms=duration_ms, energy=energy, instrumentalness=instrumentalness, key=key,
                   liveness=liveness, mode=mode, speechiness=speechiness, tempo=tempo, time_signature=time_signature,
                   valence=valence, loudness=loudness)
    session.add(track)
    session.commit()


def getData(database):
    engine = None
    if database == "sleep":
        engine = sleep_engine
    elif database == "dinner":
        engine = dinner_engine
    elif database == "party":
        engine = party_engine
    elif database == "workout":
        engine = workout_engine
    Session.configure(bind=engine)
    session = Session()
    data = []
    for row in session.query(Tracks)[:150]:
        duration = float(row.duration_ms) / 10000
        temp = [row.acousticness, row.danceability, row.energy, row.instrumentalness,
                row.speechiness, row.tempo, row.valence, row.loudness]
        data.append(temp)
    return data


def getTestData(database):
    engine = None
    if database == "sleep":
        engine = sleep_engine
    elif database == "dinner":
        engine = dinner_engine
    elif database == "party":
        engine = party_engine
    elif database == "workout":
        engine = workout_engine
    Session.configure(bind=engine)
    session = Session()
    data = []
    for row in session.query(Tracks)[151:230]:
        duration = float(row.duration_ms) / 10000
        temp = [row.acousticness, row.danceability, row.energy, row.instrumentalness,
                row.speechiness, row.tempo, row.valence, row.loudness]
        data.append(temp)
    return data
