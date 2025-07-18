from anthropic import AnthropicBedrock
from mcp_client import MCPClient
from utils import setup_logger, cprint

logger = setup_logger(__name__, level="INFO")


class FxAgent:
    """A simple agent that finds the Foreign Exchange (FX) rate for a given
    currency pair. This agent is a MCP host that uses mcp servers (i.e. fxrate)
    to process requests, orchestrate, and return the final response.
    """

    def __init__(self):
        self.anthropic = AnthropicBedrock()
        self.mcp_client = MCPClient()
        self.mcp_server_config = "mcp_server_config.json"
        self.system_message = """You are a helpful assistant that provides foreign exchange rates.

Follow these guidelines:
- Use available tools to fetch the latest exchange rates for currency pairs.
- Provide result in the format:
`<base_currency> to <quote_currency> exchange rate: <rate>`
"""

    async def invoke(self, request: str) -> str:
        """Process a request using the AI agent with tool capabilities."""
        logger.info("Request: %s", request)

        try:
            await self.mcp_client.connect_to_servers(self.mcp_server_config)
            response = await self.process_query(request)
            return response

        except Exception as err:
            logger.error("Error: %s", err, exc_info=True)
            return f"Error: {str(err)}"

        finally:
            await self.mcp_client.cleanup()

    async def process_query(self, query: str) -> str:
        """Process a query using the AI agent and return the final response."""
        messages = []

        # Add current query
        messages.append({"role": "user", "content": query})

        # Create clean tools list for Anthropic API (without any additional or
        # non-serializable data)
        tools_for_anthropic = []
        for tool in self.mcp_client.available_tools:
            tools_for_anthropic.append(
                {
                    "name": tool["name"],
                    "description": tool["description"],
                    "input_schema": tool["input_schema"],
                }
            )

        final_response = ""

        while True:
            model = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
            max_tokens = 2048
            response = self.anthropic.messages.create(
                model=model,
                max_tokens=max_tokens,
                tools=tools_for_anthropic,
                system=self.system_message,
                messages=messages,
            )

            assistant_content = []
            has_tool_use = False

            for content in response.content:
                if content.type == "text":
                    final_response = content.text
                    assistant_content.append(content)
                elif content.type == "tool_use":
                    has_tool_use = True
                    assistant_content.append(content)
                    messages.append(
                        {"role": "assistant", "content": assistant_content}
                    )
                    try:
                        result = await self.mcp_client.execute_tool(
                            content.name, content.input
                        )
                        cprint(f"Tool result: {result}", color="blue")
                        messages.append(
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "tool_result",
                                        "tool_use_id": content.id,
                                        "content": result.content,
                                    }
                                ],
                            }
                        )
                    except ValueError as err:
                        logger.error("Error: %s", err)
                        break

            # If assistant response exists, add that to the messages
            if not has_tool_use and assistant_content:
                messages.append(
                    {"role": "assistant", "content": assistant_content}
                )

            # Exit loop if no tool was used
            if not has_tool_use:
                break

        return final_response or "No response generated"
