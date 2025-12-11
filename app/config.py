"""
Application Configuration

Centralized configuration management.
"""

import os
from typing import Optional
from dataclasses import dataclass

@dataclass
class DatabaseConfig:
    """Database configuration settings"""
    url: str
    echo: bool = False
    pool_pre_ping: bool = True
    pool_recycle: int = 3600

@dataclass
class AppConfig:
    """Main application configuration"""
    debug: bool = False
    log_level: str = "INFO"
    data_dir: str = "."
    
    @property
    def database(self) -> DatabaseConfig:
        """Get database configuration"""
        db_url = os.getenv("DATABASE_URL", f"sqlite:///{self.data_dir}/lingua_latina.db")
        return DatabaseConfig(
            url=db_url,
            echo=self.debug
        )

# Global configuration instance
config = AppConfig(
    debug=os.getenv("DEBUG", "False").lower() == "true",
    log_level=os.getenv("LOG_LEVEL", "INFO"),
    data_dir=os.getenv("DATA_DIR", ".")
)