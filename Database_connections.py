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

sleep_audio_engine = create_engine(
    'sqlite:///E:\\programming\\python\\Spotify_data_extraction\\sleep_audio_features.db', echo=False)
workout_audio_engine = create_engine(
    'sqlite:///E:\\programming\\python\\Spotify_data_extraction\\workout_audio_features.db', echo=False)
party_audio_engine = create_engine(
    'sqlite:///E:\\programming\\python\\Spotify_data_extraction\\party_audio_features.db', echo=False)
dinner_audio_engine = create_engine(
    'sqlite:///E:\\programming\\python\\Spotify_data_extraction\\dinner_audio_features.db', echo=False)

Base = declarative_base()

engine = None

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


class AudioFeatures(Base):
    __tablename__ = 'audio features'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)  # name of the song
    mfcc = Column(REAL)  # mean of mfcc mean
    scem = Column(REAL)  # spectral centroid mean
    scom = Column(REAL)  # Spectral Contrast mean
    srom = Column(REAL)  # Spectral roll off mean
    sbwm = Column(REAL)  # Spectral bandwidth mean
    tempo = Column(REAL)  # tempo
    rmse = Column(REAL)  # Root Mean Square Energy


Session = sessionmaker(bind=engine)
session = Session()


def Create_table(database):
    engine = None
    if database == "sleep":
        engine = sleep_audio_engine
    elif database == "dinner":
        engine = dinner_audio_engine
    elif database == "party":
        engine = party_audio_engine
    elif database == "workout":
        engine = workout_audio_engine
    Base.metadata.create_all(engine)


def addAudioFeatures(name, mfcc, scem, scom, srom, sbwm, tempo, database, rmse):
    engine = None
    if database == "sleep":
        engine = sleep_audio_engine
    elif database == "dinner":
        engine = dinner_audio_engine
    elif database == "party":
        engine = party_audio_engine
    elif database == "workout":
        engine = workout_audio_engine
    Session = sessionmaker(bind=engine)
    session = Session()
    audio_features = AudioFeatures(name=name, mfcc=mfcc, scem=scem, scom=scom, srom=srom, sbwm=sbwm, tempo=tempo,
                                   rmse=rmse)
    session.add(audio_features)
    session.commit()


def addTrack(id, name, uri, artist, acousticness, danceability, duration_ms, energy, instrumentalness, key, liveness,
             mode, speechiness, tempo, time_signature, valence, loudness):
    track = Tracks(id=id, uri=uri, name=name, artist=artist, acousticness=acousticness, danceability=danceability,
                   duration_ms=duration_ms, energy=energy, instrumentalness=instrumentalness, key=key,
                   liveness=liveness, mode=mode, speechiness=speechiness, tempo=tempo, time_signature=time_signature,
                   valence=valence, loudness=loudness)
    session.add(track)
    session.commit()


def getTracksById(numberOfTracks, database, start=0):
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
    for row in session.query(Tracks)[start:numberOfTracks]:
        temp = row.id;
        data.append(temp)
    return data


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


def getAudioData(database,training=True):
    engine = None
    if database == "sleep":
        engine = sleep_audio_engine
    elif database == "dinner":
        engine = dinner_audio_engine
    elif database == "party":
        engine = party_audio_engine
    elif database == "workout":
        engine = workout_audio_engine
    Session = sessionmaker(bind=engine)
    session = Session()
    data =[]
    if training:
        for row in session.query(AudioFeatures)[:21]:
            temp = [row.mfcc, row.scem, row.scom, row.srom, row.sbwm, row.tempo, row.rmse]
            data.append(temp)
        return data
    else:
        for row in session.query(AudioFeatures)[21:]:
            temp = [row.mfcc, row.scem, row.scom, row.srom, row.sbwm, row.tempo, row.rmse]
            data.append(temp)
        return data
