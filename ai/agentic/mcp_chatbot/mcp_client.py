import json
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPClient:
    """
    This class manages connections to MCP servers (via separate sessions), and
    provides methods for accessing their tools, prompts, and resources.
    """

    def __init__(self):
        self.exit_stack = AsyncExitStack()
        self.server_sessions = {}
        self.available_tools = []
        self.available_prompts = []
        self.available_resources = []

    async def connect_to_servers(self, config_file):
        try:
            with open(config_file, "r", encoding="utf-8") as file:
                data = json.load(file)
            servers = data.get("mcpServers", {})
            for server_name, server_config in servers.items():
                print(f"Connecting to server: {server_name}")
                await self.connect_to_server(server_name, server_config)
        except Exception as err:
            print(f"Error loading server config: {err}")
            raise

    async def connect_to_server(self, server_name, server_config):
        # Check for duplicate server names
        if server_name in self.server_sessions:
            raise ValueError(
                f"Duplicate server name '{server_name}' found."
                " Each server must have a unique name."
            )

        server_params = StdioServerParameters(**server_config)
        try:
            stdio_transport = await self.exit_stack.enter_async_context(
                stdio_client(server_params)
            )
            read, write = stdio_transport
            session = await self.exit_stack.enter_async_context(
                ClientSession(read, write)
            )
            await session.initialize()

            # Store session in the dictionary
            self.server_sessions[server_name] = session

            # Read available tools
            response = await session.list_tools()
            for tool in response.tools:
                self.available_tools.append(
                    {
                        "name": tool.name,
                        "description": tool.description,
                        "input_schema": tool.inputSchema,
                        "server_name": server_name,
                    }
                )

            # Read available prompts
            prompts_response = await session.list_prompts()
            if prompts_response and prompts_response.prompts:
                for prompt in prompts_response.prompts:
                    self.available_prompts.append(
                        {
                            "name": prompt.name,
                            "description": prompt.description,
                            "arguments": prompt.arguments,
                            "server_name": server_name,
                        }
                    )
            # Read available resources
            resources_response = await session.list_resources()
            if resources_response and resources_response.resources:
                for resource in resources_response.resources:
                    self.available_resources.append(
                        {
                            "name": resource.name,
                            "uri": str(resource.uri),
                            "description": resource.description,
                            "protocol": str(resource.uri).split(
                                "://", maxsplit=1
                            )[0]
                            + "://",
                            "server_name": server_name,
                        }
                    )

        except Exception as err:
            print(f"Error connecting to {server_name}: {err}")
            raise

    def _get_session(self, server_name):
        """Get session for a server with error handling."""
        session = self.server_sessions.get(server_name)
        if not session:
            raise ValueError(f"Session for server '{server_name}' not found.")
        return session

    async def execute_tool(self, tool_name, arguments):
        """Execute a tool call and return the result."""
        tool_info = next(
            (t for t in self.available_tools if t["name"] == tool_name),
            None,
        )
        if not tool_info:
            raise ValueError(f"Tool '{tool_name}' not found.")

        session = self._get_session(tool_info["server_name"])
        return await session.call_tool(tool_name, arguments=arguments)

    async def get_resource(self, resource_uri):
        """Read a resource and display its content."""
        try:
            if "://" not in resource_uri:
                raise ValueError(f"Invalid resource URI: {resource_uri}")

            protocol = resource_uri.split("://")[0] + "://"
            resource_info = next(
                (
                    r
                    for r in self.available_resources
                    if r["protocol"] == protocol
                ),
                None,
            )
            if not resource_info:
                raise ValueError(f"Protocol '{protocol}' not found.")

            session = self._get_session(resource_info["server_name"])
            result = await session.read_resource(uri=resource_uri)

            if result and result.contents:
                print(f"\nResource: {resource_uri}")
                print("Content:")
                print(result.contents[0].text)
            else:
                print("No content available.")
        except Exception as err:
            print(f"Error: {err}")

    async def get_prompt(self, prompt_name, args):
        """Get a prompt with the given arguments and return its content."""
        prompt_info = next(
            (p for p in self.available_prompts if p["name"] == prompt_name),
            None,
        )
        if not prompt_info:
            print(f"Prompt '{prompt_name}' not found.")
            return

        try:
            session = self._get_session(prompt_info["server_name"])
            result = await session.get_prompt(prompt_name, arguments=args)

            if not result or not result.messages:
                raise ValueError(
                    f"No content returned for prompt '{prompt_name}'."
                )

            prompt_content = result.messages[0].content

            # Extract text from content and handle different formats
            if isinstance(prompt_content, str):
                text = prompt_content
            elif hasattr(prompt_content, "text"):
                text = prompt_content.text
            else:
                # Handle list of content items
                text = " ".join(
                    item.text if hasattr(item, "text") else str(item)
                    for item in prompt_content
                )
            return text
        except Exception as err:
            print(f"Error: {err}")

    async def cleanup(self):
        await self.exit_stack.aclose()
