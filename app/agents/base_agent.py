"""
LatinLingua Agent Base Class
"""
from abc import ABC, abstractmethod
from typing import Dict, Any


class LatinLinguaAgent(ABC):
    """
    Abstract base class for all LatinLingua agents.
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a request and return a response.
        
        Args:
            request: Dictionary containing request data
            
        Returns:
            Dictionary containing response data
        """
        pass

    @abstractmethod
    async def get_capabilities(self) -> Dict[str, Any]:
        """
        Return agent capabilities.
        
        Returns:
            Dictionary describing agent capabilities
        """
        pass