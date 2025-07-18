import json
import argparse
import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCard

from agent_executor import SimpleAgentExecutor
from fx_agent import FxAgent
from utils import setup_logger

logger = setup_logger(__name__, level="INFO")


def get_agent(agent_card: AgentCard):
    try:
        if agent_card.name == "FxAgent":
            return FxAgent()

        raise ValueError("Unsupported agent in agent card.")
    except Exception as err:
        logger.error("Error getting agent: %s", err)
        raise


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="A2A Agent Server")
    parser.add_argument(
        "--agent-card",
        type=str,
        default=".well-known/agent.json",
        help="Path to agent card JSON file (default: .well-known/agent.json)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=9999,
        help="Port to run the server on (default: 9999)",
    )
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host to bind the server to (default: 0.0.0.0)",
    )
    return parser.parse_args()


def main():
    args = parse_arguments()

    try:
        with open(args.agent_card, encoding="utf-8") as file:
            data = json.load(file)
        agent_card = AgentCard(**data)

        request_handler = DefaultRequestHandler(
            agent_executor=SimpleAgentExecutor(agent=get_agent(agent_card)),
            task_store=InMemoryTaskStore(),
        )

        server = A2AStarletteApplication(
            agent_card=agent_card, http_handler=request_handler
        )

        uvicorn.run(server.build(), host=args.host, port=args.port)

    except Exception as err:
        logger.error("An error occurred during server startup: %s", err)
        raise


if __name__ == "__main__":
    main()
