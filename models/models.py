from typing import Optional
from sqlalchemy import DateTime, Enum
import enum
import datetime

from sqlalchemy import (
    CheckConstraint,
    Column,
    Computed,
    Date,
    ForeignKeyConstraint,
    Index,
    Integer,
    String,
    Table,
    text,
    Boolean,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Player(Base):
    __tablename__ = "player"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    username: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    last_opened: Mapped[Optional[datetime.date]] = mapped_column(Date)

    profile_picture: Mapped[str] = mapped_column(
        String(255), nullable=False, default="default.png"
    )

    pokeball_history: Mapped[list["PokeballHistory"]] = relationship(
        "PokeballHistory", back_populates="user"
    )
    pokemon_owned: Mapped[list["PokemonOwned"]] = relationship(
        "PokemonOwned", back_populates="player"
    )


class PokemonStat(Base):
    __tablename__ = "pokemon_stat"

    pokedex_number: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    type1: Mapped[str] = mapped_column(String(20), nullable=False)
    classification: Mapped[Optional[str]] = mapped_column(String(50))
    base_total: Mapped[Optional[int]] = mapped_column(Integer)
    type2: Mapped[Optional[str]] = mapped_column(String(20))
    generation: Mapped[Optional[int]] = mapped_column(Integer)
    capture_rate: Mapped[Optional[int]] = mapped_column(Integer)
    is_legendary: Mapped[Optional[bool]] = mapped_column(Boolean)

    pokeball_history: Mapped[list["PokeballHistory"]] = relationship(
        "PokeballHistory", back_populates="pokemon_stat"
    )
    pokemon_owned: Mapped[list["PokemonOwned"]] = relationship(
        "PokemonOwned", back_populates="pokemon_stat"
    )


t_friend = Table(
    "friend",
    Base.metadata,
    Column("id1", String(32), nullable=False),
    Column("id2", String(32), nullable=False),
    Column(
        "id_min",
        String(100),
        Computed(func.least(text("id1"), text("id2")), persisted=True),
    ),
    Column(
        "id_max",
        String(100),
        Computed(func.greatest(text("id1"), text("id2")), persisted=True),
    ),
    Column("approved", Boolean, nullable=False, server_default=text("false")),
    Column("petitioner", String(100), nullable=False),
    CheckConstraint("petitioner IN (id1, id2)", name="friend_chk_1"),
    ForeignKeyConstraint(["id1"], ["player.id"], name="friend_ibfk_1"),
    ForeignKeyConstraint(["id2"], ["player.id"], name="friend_ibfk_2"),
    ForeignKeyConstraint(["petitioner"], ["player.id"], name="friend_ibfk_3"),
    Index("id1", "id1"),
    Index("id2", "id2"),
    Index("id_min", "id_min", "id_max", unique=True),
    Index("petitioner", "petitioner"),
)


class PokeballHistory(Base):
    __tablename__ = "pokeball_history"
    __table_args__ = (
        ForeignKeyConstraint(
            ["awarded_pokemon_number"],
            ["pokemon_stat.pokedex_number"],
            name="fk_pokeball_pokemon",
        ),
        ForeignKeyConstraint(["user_id"], ["player.id"], name="fk_pokeball_user"),
        Index("fk_pokeball_pokemon", "awarded_pokemon_number"),
        Index("fk_pokeball_user", "user_id"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(32), nullable=False)
    awarded_pokemon_number: Mapped[int] = mapped_column(Integer, nullable=False)
    opened_at: Mapped[Optional[datetime.date]] = mapped_column(Date)

    pokemon_stat: Mapped["PokemonStat"] = relationship(
        "PokemonStat", back_populates="pokeball_history"
    )
    user: Mapped["Player"] = relationship("Player", back_populates="pokeball_history")


class PokemonOwned(Base):
    __tablename__ = "pokemon_owned"
    __table_args__ = (
        ForeignKeyConstraint(
            ["player_id"],
            ["player.id"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="fk_player",
        ),
        ForeignKeyConstraint(
            ["pokedex_number"],
            ["pokemon_stat.pokedex_number"],
            ondelete="RESTRICT",
            onupdate="CASCADE",
            name="fk_pokemon",
        ),
        Index("fk_player", "player_id"),
        Index("fk_pokemon", "pokedex_number"),
    )

    id: Mapped[str] = mapped_column(String(24), primary_key=True)
    player_id: Mapped[str] = mapped_column(String(32), nullable=False)
    pokedex_number: Mapped[int] = mapped_column(Integer, nullable=False)
    in_team: Mapped[bool] = mapped_column(Boolean, nullable=False)
    obtained_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    mote: Mapped[Optional[str]] = mapped_column(String(20))

    player: Mapped["Player"] = relationship("Player", back_populates="pokemon_owned")
    pokemon_stat: Mapped["PokemonStat"] = relationship(
        "PokemonStat", back_populates="pokemon_owned"
    )


class TradeStatus(enum.Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"


class Trade(Base):
    __tablename__ = "trade"
    __table_args__ = (
        ForeignKeyConstraint(
            ["requester_id"], ["player.id"], name="fk_trade_requester"
        ),
        ForeignKeyConstraint(["receiver_id"], ["player.id"], name="fk_trade_receiver"),
        ForeignKeyConstraint(
            ["requester_pokemon_id"],
            ["pokemon_owned.id"],
            name="fk_trade_requester_pokemon",
        ),
        ForeignKeyConstraint(
            ["receiver_pokemon_id"],
            ["pokemon_owned.id"],
            name="fk_trade_receiver_pokemon",
        ),
        Index("fk_trade_requester", "requester_id"),
        Index("fk_trade_receiver", "receiver_id"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    requester_id: Mapped[str] = mapped_column(String(32), nullable=False)
    receiver_id: Mapped[str] = mapped_column(String(32), nullable=False)
    requester_pokemon_id: Mapped[str] = mapped_column(String(24), nullable=False)
    receiver_pokemon_id: Mapped[str] = mapped_column(String(24), nullable=False)
    status: Mapped[TradeStatus] = mapped_column(
        Enum(TradeStatus), default=TradeStatus.pending, nullable=False
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )
    decided_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, nullable=True
    )
    requester: Mapped["Player"] = relationship("Player", foreign_keys=[requester_id])
    receiver: Mapped["Player"] = relationship("Player", foreign_keys=[receiver_id])
    requester_pokemon: Mapped["PokemonOwned"] = relationship(
        "PokemonOwned", foreign_keys=[requester_pokemon_id]
    )
    receiver_pokemon: Mapped["PokemonOwned"] = relationship(
        "PokemonOwned", foreign_keys=[receiver_pokemon_id]
    )
