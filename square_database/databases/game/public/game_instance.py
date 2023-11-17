from sqlalchemy import Column, Integer, Sequence, DateTime, func, ForeignKey
from sqlalchemy.orm import declarative_base

from square_database.databases.game.public.game import Game

Base = declarative_base()


class GameInstance(Base):
    __tablename__ = 'game_instance'

    game_instance_id = Column(Integer, Sequence('game_instance_seq'), primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey(Game.game_id, ondelete="RESTRICT", onupdate="RESTRICT"), index=True,
                     nullable=False)
    game_instance_date_created = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    game_instance_last_modified = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(),
                                         nullable=False)
