"""
Optimized Vocabulary Service
Handles vocabulary operations with caching, pagination, and validation.
"""

import logging
from datetime import datetime, timedelta
from functools import lru_cache
from typing import List, Optional, Tuple

from pydantic import BaseModel, Field, validator
from sqlalchemy import and_, func, select
from sqlalchemy.orm import Session

from app.models.core import DifficultyLevel, Word
from app.utils.model_mapper import ModelMapper
from database import Word as DBWord

logger = logging.getLogger(__name__)


class SearchQuery(BaseModel):
    """Validated search query"""

    query: str = Field(..., min_length=1, max_length=100)
    limit: int = Field(default=50, le=500, ge=1)
    offset: int = Field(default=0, ge=0)

    @validator("query")
    def query_must_be_clean(cls, v):
        """Sanitize query string"""
        return v.strip().lower()


class PaginatedResult(BaseModel):
    """Paginated response wrapper"""

    items: List[Word]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool


class CacheEntry:
    """Simple cache entry with TTL"""

    def __init__(self, value, ttl_seconds: int = 300):
        self.value = value
        self.created_at = datetime.utcnow()
        self.ttl_seconds = ttl_seconds

    def is_expired(self) -> bool:
        """Check if cache entry has expired"""
        return datetime.utcnow() - self.created_at > timedelta(seconds=self.ttl_seconds)


class VocabularyCache:
    """Simple in-memory cache for vocabulary data"""

    def __init__(self, ttl_seconds: int = 300):
        self.ttl_seconds = ttl_seconds
        self.cache = {}

    def get(self, key: str) -> Optional[object]:
        """Get from cache if not expired"""
        if key not in self.cache:
            return None

        entry = self.cache[key]
        if entry.is_expired():
            del self.cache[key]
            return None

        logger.debug(f"Cache hit for key: {key}")
        return entry.value

    def set(self, key: str, value: object) -> None:
        """Store in cache with TTL"""
        self.cache[key] = CacheEntry(value, self.ttl_seconds)
        logger.debug(f"Cache set for key: {key}")

    def clear(self) -> None:
        """Clear all cache"""
        self.cache.clear()
        logger.debug("Cache cleared")

    def cleanup_expired(self) -> int:
        """Remove expired entries, return count"""
        expired = [k for k, v in self.cache.items() if v.is_expired()]
        for k in expired:
            del self.cache[k]
        if expired:
            logger.debug(f"Cleaned up {len(expired)} expired cache entries")
        return len(expired)


class VocabularyService:
    """Service for handling vocabulary-related operations with optimizations"""

    def __init__(self, session: Session, cache_ttl: int = 300):
        """
        Initialize vocabulary service

        Args:
            session: Database session
            cache_ttl: Cache time-to-live in seconds
        """
        self.session = session
        self.cache = VocabularyCache(ttl_seconds=cache_ttl)
        logger.info("VocabularyService initialized")

    def get_words_by_level(
        self, level: int, page: int = 1, page_size: int = 50
    ) -> PaginatedResult:
        """
        Get words filtered by difficulty level with pagination.

        Args:
            level: Difficulty level (1-4)
            page: Page number (1-indexed)
            page_size: Results per page (max 500)

        Returns:
            PaginatedResult with words and metadata

        Raises:
            ValueError: If parameters invalid
        """
        if level < 1 or level > 4:
            raise ValueError(f"Level must be 1-4, got {level}")

        if page < 1:
            raise ValueError(f"Page must be >= 1, got {page}")

        page_size = min(page_size, 500)  # Cap at 500

        # Try cache
        cache_key = f"words_level_{level}_page_{page}_size_{page_size}"
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        try:
            # Count total
            total = (
                self.session.exec(
                    select(func.count(DBWord.id)).where(DBWord.level == level)
                ).first()
                or 0
            )

            # Calculate pagination
            offset = (page - 1) * page_size
            total_pages = (total + page_size - 1) // page_size

            # Get page of results
            db_words = self.session.exec(
                select(DBWord)
                .where(DBWord.level == level)
                .order_by(DBWord.latin)
                .offset(offset)
                .limit(page_size)
            ).all()

            words = ModelMapper.db_words_to_domain(db_words)

            result = PaginatedResult(
                items=words,
                total=total,
                page=page,
                page_size=page_size,
                total_pages=total_pages,
                has_next=page < total_pages,
                has_previous=page > 1,
            )

            # Cache result
            self.cache.set(cache_key, result)

            logger.info(f"Retrieved {len(words)} words for level {level}")
            return result

        except Exception as e:
            logger.error(f"Error fetching words by level: {e}", exc_info=True)
            raise

    def search_words(self, search: SearchQuery) -> List[Word]:
        """
        Search words by Latin term or translation.
        Optimized with startswith for better index usage.

        Args:
            search: Validated SearchQuery

        Returns:
            List of matching words (up to limit)
        """
        # Try cache
        cache_key = f"search_{search.query}_{search.limit}_{search.offset}"
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        try:
            query = search.query

            # Use startswith for better index performance
            # Fall back to contains for mid-word matches
            db_words = self.session.exec(
                select(DBWord)
                .where(
                    (func.lower(DBWord.latin).startswith(query))
                    | (func.lower(DBWord.translation).startswith(query))
                    | (func.lower(DBWord.latin).contains(query))
                    | (func.lower(DBWord.translation).contains(query))
                )
                .order_by(DBWord.latin)
                .offset(search.offset)
                .limit(search.limit)
            ).all()

            words = ModelMapper.db_words_to_domain(db_words)

            # Cache results
            self.cache.set(cache_key, words)

            logger.info(f"Search for '{query}' returned {len(words)} results")
            return words

        except Exception as e:
            logger.error(f"Error searching words: {e}", exc_info=True)
            raise

    def get_word_of_the_day(self, user_level: int) -> Optional[Word]:
        """
        Get a random word appropriate for user's level.

        Args:
            user_level: User's current level (1-4)

        Returns:
            Random Word or None if no words available
        """
        cache_key = f"wotd_level_{user_level}_{datetime.utcnow().date()}"
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        try:
            import random

            # Count words at or below level
            count = (
                self.session.exec(
                    select(func.count(DBWord.id)).where(DBWord.level <= user_level)
                ).first()
                or 0
            )

            if count == 0:
                logger.warning(f"No words found for level {user_level}")
                return None

            # Random offset
            offset = random.randint(0, max(0, count - 1))

            db_word = self.session.exec(
                select(DBWord)
                .where(DBWord.level <= user_level)
                .order_by(DBWord.id)
                .offset(offset)
                .limit(1)
            ).first()

            if not db_word:
                return None

            word = ModelMapper.db_word_to_domain(db_word)

            # Cache for the day
            self.cache.set(cache_key, word)

            logger.debug(f"Word of the day: {word.latin}")
            return word

        except Exception as e:
            logger.error(f"Error getting word of the day: {e}", exc_info=True)
            return None

    def get_fundamental_words(self, limit: int = 100) -> List[Word]:
        """
        Get fundamental vocabulary (most important words).

        Args:
            limit: Maximum words to return

        Returns:
            List of fundamental words
        """
        cache_key = f"fundamental_words_{limit}"
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        try:
            db_words = self.session.exec(
                select(DBWord)
                .where(
                    (DBWord.is_fundamental == True)
                    | (DBWord.frequency_rank_global.isnot(None))
                )
                .order_by(DBWord.frequency_rank_global.nullslast(), DBWord.latin)
                .limit(limit)
            ).all()

            words = ModelMapper.db_words_to_domain(db_words)
            self.cache.set(cache_key, words)

            logger.info(f"Retrieved {len(words)} fundamental words")
            return words

        except Exception as e:
            logger.error(f"Error getting fundamental words: {e}", exc_info=True)
            return []

    def get_words_by_part_of_speech(
        self, part_of_speech: str, page: int = 1, page_size: int = 50
    ) -> PaginatedResult:
        """
        Get words filtered by part of speech with pagination.

        Args:
            part_of_speech: Word category (noun, verb, adjective, etc.)
            page: Page number
            page_size: Results per page

        Returns:
            PaginatedResult with words
        """
        cache_key = f"pos_{part_of_speech}_page_{page}_size_{page_size}"
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        try:
            part_of_speech = part_of_speech.lower().strip()

            # Count
            total = (
                self.session.exec(
                    select(func.count(DBWord.id)).where(
                        func.lower(DBWord.part_of_speech) == part_of_speech
                    )
                ).first()
                or 0
            )

            # Paginate
            offset = (page - 1) * page_size
            page_size = min(page_size, 500)

            db_words = self.session.exec(
                select(DBWord)
                .where(func.lower(DBWord.part_of_speech) == part_of_speech)
                .order_by(DBWord.latin)
                .offset(offset)
                .limit(page_size)
            ).all()

            words = ModelMapper.db_words_to_domain(db_words)
            total_pages = (total + page_size - 1) // page_size

            result = PaginatedResult(
                items=words,
                total=total,
                page=page,
                page_size=page_size,
                total_pages=total_pages,
                has_next=page < total_pages,
                has_previous=page > 1,
            )

            self.cache.set(cache_key, result)
            logger.info(f"Retrieved {len(words)} {part_of_speech}s")
            return result

        except Exception as e:
            logger.error(f"Error getting words by POS: {e}", exc_info=True)
            raise

    def clear_cache(self) -> None:
        """Clear all cached data"""
        self.cache.clear()
        logger.info("Vocabulary cache cleared")

    def get_cache_stats(self) -> dict:
        """Get cache statistics"""
        self.cache.cleanup_expired()
        return {
            "cache_size": len(self.cache.cache),
            "ttl_seconds": self.cache.ttl_seconds,
        }
