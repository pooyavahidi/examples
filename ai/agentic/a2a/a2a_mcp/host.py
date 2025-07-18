import logging
import asyncio
from typing import Any
from uuid import uuid4
import httpx
from a2a.client import A2ACardResolver, A2AClient
from a2a.types import AgentCard, MessageSendParams, SendMessageRequest
from utils import setup_logger

logger = setup_logger(__name__, level="INFO")

PUBLIC_AGENT_CARD_PATH = "/.well-known/agent.json"
BASE_URL = "http://localhost:9999"


async def main() -> None:
    # Increase the default timeout for HTTP requests as the agent may take
    # longer to respond, especially when communicating with LLMs
    timeout_config = httpx.Timeout(connect=10, read=120, write=20, pool=10)

    async with httpx.AsyncClient(timeout=timeout_config) as httpx_client:
        # Initialize A2ACardResolver
        resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url=BASE_URL,
        )

        # Fetch Public Agent Card and Initialize Client
        final_agent_card_to_use: AgentCard | None = None

        try:
            logger.info(
                "Attempting to fetch public agent card from: %s%s",
                BASE_URL,
                PUBLIC_AGENT_CARD_PATH,
            )

            # Fetches from default public path
            final_agent_card_to_use = await resolver.get_agent_card()
            logger.info("Successfully fetched public agent card.")

        except Exception as err:
            logger.error(
                "Error fetching public agent card. %s", err, exc_info=True
            )
            raise

        # Create A2AClient and payload message to be sent to the agent card
        client = A2AClient(
            httpx_client=httpx_client, agent_card=final_agent_card_to_use
        )
        logger.info("A2AClient initialized.")

        message_payload: dict[str, Any] = {
            "message": {
                "role": "user",
                "parts": [{"kind": "text", "text": "USD to AUD"}],
                "messageId": uuid4().hex,
            },
        }

        request = SendMessageRequest(
            id=str(uuid4()), params=MessageSendParams(**message_payload)
        )

        response = await client.send_message(request)
        print(response.model_dump(mode="json", exclude_none=True))


if __name__ == "__main__":
    asyncio.run(main())
