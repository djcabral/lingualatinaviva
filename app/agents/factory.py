"""
Agent Factory for creating LatinLingua agents
"""
from app.agents.latinlingua_ai import LatinLinguaAI
from typing import Union


def create_agent(agent_type: str) -> Union[LatinLinguaAI]:
    """
    Factory function to create agents based on type.
    
    Args:
        agent_type: Type of agent to create
        
    Returns:
        Instance of the requested agent
    """
    if agent_type == "latinlingua_ai":
        return LatinLinguaAI()
    else:
        raise ValueError(f"Unknown agent type: {agent_type}")


async def get_available_agents():
    """
    Get list of available agents.
    
    Returns:
        List of available agent types
    """
    return ["latinlingua_ai"]