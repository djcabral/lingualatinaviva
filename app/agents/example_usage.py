"""
Example usage of LatinLingua agents
"""
import asyncio
from app.agents.factory import create_agent


async def main():
    # Create an agent
    agent = create_agent("latinlingua_ai")
    
    # Get agent capabilities
    capabilities = await agent.get_capabilities()
    print("Agent Capabilities:")
    print(capabilities)
    
    # Process a sample request
    request = {
        "type": "translation_exercise",
        "text": "Lorem ipsum dolor sit amet"
    }
    
    response = await agent.process_request(request)
    print("\nSample Response:")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())