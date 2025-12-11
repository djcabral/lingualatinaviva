"""
Model Mapper - Centralizado
Convierte modelos de BD a modelos de dominio de forma consistente.

Esto elimina la duplicación de código en servicios y previene inconsistencias
en el mapeo de atributos.
"""

from typing import List, Optional

from app.models.core import User, Word
from database import UserProfile
from database import Word as DBWord


class ModelMapper:
    """Mapeador centralizado de modelos de BD a dominio"""

    @staticmethod
    def db_word_to_domain(db_word: DBWord) -> Word:
        """
        Convierte un modelo Word de BD a modelo de dominio.

        Args:
            db_word: Modelo Word de la BD

        Returns:
            Modelo Word de dominio
        """
        if not db_word:
            return None

        return Word(
            id=db_word.id,
            latin=db_word.latin,
            translation=db_word.translation,
            part_of_speech=db_word.part_of_speech,
            level=db_word.level,
            genitive=db_word.genitive,
            gender=db_word.gender,
            declension=db_word.declension,
            principal_parts=db_word.principal_parts,
            conjugation=db_word.conjugation,
            is_plural_only=db_word.is_plurale_tantum,
            is_singular_only=db_word.is_singulare_tantum,
            is_invariable=db_word.is_invariable,
            is_fundamental=db_word.is_fundamental,
            status=db_word.status,
        )

    @staticmethod
    def db_words_to_domain(db_words: List[DBWord]) -> List[Word]:
        """
        Convierte lista de modelos Word de BD a modelos de dominio.

        Args:
            db_words: Lista de modelos Word de BD

        Returns:
            Lista de modelos Word de dominio
        """
        return [ModelMapper.db_word_to_domain(word) for word in db_words]

    @staticmethod
    def db_user_to_domain(db_user: UserProfile) -> User:
        """
        Convierte un modelo UserProfile de BD a modelo User de dominio.

        Args:
            db_user: Modelo UserProfile de la BD

        Returns:
            Modelo User de dominio
        """
        if not db_user:
            return None

        return User(
            id=db_user.id,
            username=db_user.username,
            level=db_user.level,
            xp=db_user.xp,
            streak=db_user.streak,
            total_stars=db_user.total_stars,
            challenges_completed=db_user.challenges_completed,
            perfect_challenges=db_user.perfect_challenges,
            last_login=db_user.last_login,
        )

    @staticmethod
    def db_users_to_domain(db_users: List[UserProfile]) -> List[User]:
        """
        Convierte lista de modelos UserProfile a modelos User de dominio.

        Args:
            db_users: Lista de modelos UserProfile de BD

        Returns:
            Lista de modelos User de dominio
        """
        return [ModelMapper.db_user_to_domain(user) for user in db_users]
