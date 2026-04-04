from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    contrasena: Mapped[str] = mapped_column(nullable=False)
    fecha_registro: Mapped[datetime] = mapped_column(
        DateTime(), default=datetime.utcnow)

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "fecha_registro": self.fecha_registro
        }


class Planetas(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(nullable=False)
    clima: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    poblacion: Mapped[int] = mapped_column(nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "clima": self.clima,
            "poblacion": self.poblacion
        }


class Personajes(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(nullable=False)
    genero: Mapped[str] = mapped_column(String(120), nullable=False)
    id_planeta: Mapped[int] = mapped_column(ForeignKey("planetas.id"), nullable=False
                                            )

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "genero": self.genero,
            "id_planeta": self.id_planeta
        }


class PlanetaFavorito(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    id_usuario: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False)
    id_planeta: Mapped[int] = mapped_column(
        ForeignKey("planetas.id"), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "id_usuario": self.id_usuario,
            "id_planeta": self.id_planeta,
        }


class PersonajesFavoritos(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    id_usuario: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False)
    id_personajes: Mapped[int] = mapped_column(
        ForeignKey("personajes.id"), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "id_usuario": self.id_usuario,
            "id_personajes": self.id_personajes,
        }
