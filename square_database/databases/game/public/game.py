from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Game(Base):
    __tablename__ = 'game'

    game_id = Column(Integer, Sequence('game_id_seq'), primary_key=True, index=True)
    game_name = Column(String, nullable=False, unique=True)
    __default_data__ = [
        {"game_name": "truecolor"}
    ]
