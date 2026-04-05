from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from datetime import datetime

db = SQLAlchemy()

# USER (PADRE)
class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    contrasena: Mapped[str] = mapped_column(nullable=False)
    fecha_registro: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow)

    # RELACIONES
    planetas_favoritos = relationship("PlanetaFavorito", back_populates="usuario")
    personajes_favoritos = relationship("PersonajesFavoritos", back_populates="usuario")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "fecha_registro": self.fecha_registro
        }


# PLANETAS (PADRE)
class Planetas(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(nullable=False)
    clima: Mapped[str] = mapped_column(String(120), nullable=False)
    poblacion: Mapped[int] = mapped_column(nullable=False)

    # RELACIONES
    personajes = relationship("Personajes", back_populates="planeta")
    favoritos = relationship("PlanetaFavorito", back_populates="planeta")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "clima": self.clima,
            "poblacion": self.poblacion
        }


# PERSONAJES (HIJO de planeta)
class Personajes(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(nullable=False)
    genero: Mapped[str] = mapped_column(String(120), nullable=False)

    id_planeta: Mapped[int] = mapped_column(ForeignKey("planetas.id"), nullable=False)

    # RELACIONES
    planeta = relationship("Planetas", back_populates="personajes")
    favoritos = relationship("PersonajesFavoritos", back_populates="personaje")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "genero": self.genero,
            "id_planeta": self.id_planeta
        }


# PLANETA FAVORITO (tabla intermedia)
class PlanetaFavorito(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    id_planeta: Mapped[int] = mapped_column(ForeignKey("planetas.id"), nullable=False)

    # RELACIONES
    usuario = relationship("User", back_populates="planetas_favoritos")
    planeta = relationship("Planetas", back_populates="favoritos")

    def serialize(self):
        return {
            "id": self.id,
            "id_usuario": self.id_usuario,
            "id_planeta": self.id_planeta,
        }


# PERSONAJES FAVORITOS (tabla intermedia)
class PersonajesFavoritos(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    id_personaje: Mapped[int] = mapped_column(ForeignKey("personajes.id"), nullable=False)

    # RELACIONES
    usuario = relationship("User", back_populates="personajes_favoritos")
    personaje = relationship("Personajes", back_populates="favoritos")

    def serialize(self):
        return {
            "id": self.id,
            "id_usuario": self.id_usuario,
            "id_personaje": self.id_personaje,
        }
