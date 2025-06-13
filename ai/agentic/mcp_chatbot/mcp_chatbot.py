import asyncio
from anthropic import AnthropicBedrock
from mcp_client import MCPClient


class ChatBot:
    """
    A chatbot for interacting with MCP servers and processing queries using the
    Anthropic API.
    """

    def __init__(self, mcp_client: MCPClient):
        self.anthropic = AnthropicBedrock()
        self.mcp_client = mcp_client

    def list_prompts(self):
        """List all available prompts."""

        if not self.mcp_client.available_prompts:
            print("No prompts available.")
            return

        print("\nAvailable prompts:")
        for server in set(
            p["server_name"] for p in self.mcp_client.available_prompts
        ):
            print(f"\nServer '{server}':")
            print("Prompts:")
            for prompt in self.mcp_client.available_prompts:
                if prompt["server_name"] == server:
                    print(f"- {prompt['name']}: {prompt['description']}")
                    if prompt["arguments"]:
                        print("  Arguments:")
                        for arg in prompt["arguments"]:
                            arg_name = (
                                arg.name
                                if hasattr(arg, "name")
                                else arg.get("name", "")
                            )
                            print(f"    - {arg_name}")

    def list_resources(self):
        """List all available resources."""

        if not self.mcp_client.available_resources:
            print("No resources available.")
            return

        print("\nAvailable Resources:")
        for server in set(
            r["server_name"] for r in self.mcp_client.available_resources
        ):
            print(f"\nServer '{server}':")
            for resource in self.mcp_client.available_resources:
                if resource["server_name"] == server:
                    print(f"- {resource['uri']} - {resource['name']}")

    def list_tools(self):
        """List all available tools."""
        if not self.mcp_client.available_tools:
            print("No tools available.")
            return

        print("\nAvailable Tools:")
        for server in set(
            t["server_name"] for t in self.mcp_client.available_tools
        ):
            print(f"\nServer '{server}':")
            for tool in self.mcp_client.available_tools:
                if tool["server_name"] == server:
                    print(f"- {tool['name']} - {tool['description']}\n\n")

    def list_servers(self):
        """List all connected MCP servers."""
        if not self.mcp_client.server_sessions:
            print("No servers connected.")
            return

        print("\nConnected MCP Servers:")
        for server_name in self.mcp_client.server_sessions.keys():

            # Count tools, prompts, and resources for this server
            tool_count = len(
                [
                    t
                    for t in self.mcp_client.available_tools
                    if t["server_name"] == server_name
                ]
            )
            prompt_count = len(
                [
                    p
                    for p in self.mcp_client.available_prompts
                    if p["server_name"] == server_name
                ]
            )
            resource_count = len(
                [
                    r
                    for r in self.mcp_client.available_resources
                    if r["server_name"] == server_name
                ]
            )
            print(
                f"- {server_name} (Tools: {tool_count},"
                f" Prompts: {prompt_count}, Resources: {resource_count})"
            )

    async def execute_prompt(self, command_parts):
        """Execute a prompt with the given command parts."""
        try:
            if len(command_parts) < 2:
                print("Usage: /prompt <name> <arg1=value1> <arg2=value2>")
                return

            prompt_name = command_parts[1]
            args = {}

            # Parse arguments
            for arg in command_parts[2:]:
                if "=" in arg:
                    key, value = arg.split("=", 1)
                    args[key] = value

            print(f"\nExecuting prompt '{prompt_name}'...")
            prompt_text = await self.mcp_client.get_prompt(prompt_name, args)
            await self.process_query(prompt_text)
        except Exception as err:
            print(f"Error: {err}")

    async def process_query(self, query):
        messages = [{"role": "user", "content": query}]

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

        while True:
            model = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
            max_tokens = 2048
            response = self.anthropic.messages.create(
                model=model,
                max_tokens=max_tokens,
                tools=tools_for_anthropic,
                messages=messages,
            )

            assistant_content = []
            has_tool_use = False

            for content in response.content:
                if content.type == "text":
                    print(content.text)
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
                        print(f"Error: {err}")
                        break

            # Exit loop if no tool was used
            if not has_tool_use:
                break

    async def chat_loop(self):
        print("Type your queries or '/exit' to exit.")
        print("Use /servers to list connected servers")
        print("Use /resources to list available resources")
        print("Use /tools to list available tools")
        print("Use /prompts to list available prompts")
        print("Use /prompt <name> <arg1=value1> to execute a prompt")
        print("Use @protocol://resource to see resource content")

        while True:
            try:
                query = input("\nQuery: ").strip()
                if not query:
                    continue

                # Check for /command syntax
                if query.startswith("/"):
                    parts = query.split()
                    command = parts[0].lower()

                    if command == "/exit":
                        print("Exiting chat...")
                        break
                    elif command == "/servers":
                        self.list_servers()
                    elif command == "/resources":
                        self.list_resources()
                    elif command == "/tools":
                        self.list_tools()
                    elif command == "/prompts":
                        self.list_prompts()
                    elif command == "/prompt":
                        await self.execute_prompt(parts)
                    else:
                        print(f"Unknown command: {command}")
                    continue

                # Check for @resource syntax first
                if query.startswith("@"):
                    # Remove @ sign and send to get_resource
                    await self.mcp_client.get_resource(query[1:])
                    continue

                await self.process_query(query)

            except Exception as err:
                print(f"\nError: {str(err)}")


async def main():
    mcp_client = MCPClient()
    chatbot = ChatBot(mcp_client)
    try:
        await mcp_client.connect_to_servers("server_config.json")
        await chatbot.chat_loop()
    finally:
        await mcp_client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
