import asyncio
from anthropic import AnthropicBedrock
from mcp_client import MCPClient
from utils import setup_logger, cprint

logger = setup_logger(__name__, level="INFO")


class ChatBot:
    """
    A chatbot for interacting with MCP servers and processing queries using the
    Anthropic API and Amazon Bedrock.
    """

    def __init__(self, mcp_client: MCPClient):
        self.anthropic = AnthropicBedrock()
        self.mcp_client = mcp_client
        self.conversation_history = []
        self.system_message = None

    def reset_conversation(self):
        """Reset the conversation history."""
        self.conversation_history = []
        self.system_message = None

    def print_history(self):
        print("Conversation History:")
        for message in self.conversation_history:
            role = message["role"]
            content = message["content"]
            if role == "user":
                cprint(f"{role.capitalize()}:", "cyan", bold=True)
            else:
                cprint(f"{role.capitalize()}:", "magenta", bold=True)

            print(f"{content}\n")

    def _print_common_commands(self):
        """Print common commands available in all modes."""
        print("Use /reset to clear conversation history")
        print("Use /history to see conversation history")

    def _handle_common_commands(self, command):
        """Handle common commands. Raise error if unknown command."""

        if command == "/reset":
            self.reset_conversation()
            print("Conversation history cleared.")
        elif command == "/history":
            self.print_history()
        else:
            raise ValueError(f"Unknown command: {command}")

    def _parse_command_args(self, command_parts):
        """Parse command arguments from the command parts."""
        if len(command_parts) < 2:
            print("Usage: /option <name> <arg1=value1> <arg2=value2>")
            return None, None

        command_name = command_parts[1]
        args = {}

        # Parse key=value arguments
        for arg in command_parts[2:]:
            if "=" in arg:
                key, value = arg.split("=", 1)
                # Handle quoted values
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                args[key.strip()] = value.strip()
            else:
                # Handle boolean flags or positional args
                args[arg] = True

        return command_name, args

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

    async def get_prompt(self, command_parts):
        """Print a prompt with the given command parts."""
        try:
            prompt_name, args = self._parse_command_args(command_parts)
            if not prompt_name:
                return

            print(f"\nExecuting prompt '{prompt_name}'...")
            prompt_text = await self.mcp_client.get_prompt(prompt_name, args)
            print(prompt_text)
        except Exception as err:
            logger.error("Error executing prompt '%s': %s", prompt_name, err)

    async def execute_tool(self, command_parts):
        """Execute a tool with the given command parts."""
        try:
            tool_name, args = self._parse_command_args(command_parts)
            if not tool_name:
                logger.error("Invalid tool command syntax.")
                return

            print(f"\nExecuting tool '{tool_name}'...")
            result = await self.mcp_client.execute_tool(tool_name, args)
            cprint(f"Tool result: {result.content}", color="blue")

        except Exception as err:
            logger.error("Error executing tool '%s': %s", tool_name, err)

    async def get_resource(self, resource_uri):
        """Fetch and display a resource by its URI."""
        try:
            resource = await self.mcp_client.get_resource(resource_uri)
            if resource:
                print(f"\nResource '{resource_uri}':")
                print(resource)
            else:
                print(f"Resource '{resource_uri}' not found.")
        except Exception as err:
            logger.error("Error fetching resource '%s': %s", resource_uri, err)

    async def process_query(self, query):
        messages = []

        # Add conversation history
        messages.extend(self.conversation_history)

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
        return messages

    async def admin_bot(self):
        self._print_common_commands()
        print("Use /servers to list connected servers")
        print("Use /resources to list available resources")
        print("Use /tools to list available tools")
        print("Use /tool <name> <arg1=value1> to execute a tool")
        print("Use /prompts to list available prompts")
        print("Use /prompt <name> <arg1=value1> to print a prompt")
        print("Use @protocol://resource to see resource content")
        print("Type your queries or '/exit' to exit.")

        while True:
            try:
                query = input("\nAdmin: ").strip()
                if not query:
                    continue

                # Check for /command syntax
                if query.startswith("/"):
                    parts = query.split()
                    command = parts[0].lower()

                    # Handle exit command
                    if command == "/exit":
                        print("Exiting chat...")
                        break

                    # Handle admin-specific commands
                    if command == "/servers":
                        self.list_servers()
                    elif command == "/resources":
                        self.list_resources()
                    elif command == "/tools":
                        self.list_tools()
                    elif command == "/prompts":
                        self.list_prompts()
                    elif command == "/prompt":
                        await self.get_prompt(parts)
                    elif command == "/tool":
                        await self.execute_tool(parts)
                    else:
                        self._handle_common_commands(command)
                    continue

                # Check for @resource syntax first
                if query.startswith("@"):
                    # Remove @ sign and send to get_resource
                    await self.get_resource(query[1:])
                    continue

                self.conversation_history = await self.process_query(query)

            except Exception as err:
                logger.error("Error processing query: %s", err)

    async def shopper_bot(self):
        self._print_common_commands()
        print("\nHow can I help you today?")

        categories = await self.mcp_client.get_resource("catalog://categories")
        shipping_info = await self.mcp_client.get_resource("info://shipping")

        additional_context = f"""
CONVERSATION STYLE:
- Be friendly and conversational
- Ask follow-up questions to better understand needs
- Present information clearly
- Help guide customers to the right choice
- Always verify inventory before making final recommendations

AVAILABLE CATEGORIES:
{categories}

SHIPPING INFORMATION:
{shipping_info}
"""
        # Define the brand name
        brand_name = "AnyFootwear Co."

        domain_instructions = ""

        # Get product-specific instructions from MCP server
        product_instructions = await self.mcp_client.get_prompt(
            "product_instructions",
            {"brand": brand_name},
        )

        # Get order-specific instructions from MCP server
        order_instructions = await self.mcp_client.get_prompt(
            "order_instructions", {}
        )

        domain_instructions += f"\n\n{product_instructions}"
        domain_instructions += f"\n\n{order_instructions}"
        domain_instructions += f"\n\n{additional_context}"
        self.system_message = domain_instructions

        while True:
            try:
                query = input("\nQuery: ").strip()
                if not query:
                    continue

                if query.startswith("/"):
                    command = query.lower()
                    # Handle exit command
                    if command == "/exit":
                        print("Thank you for visiting! Have a great day!")
                        break
                    else:
                        self._handle_common_commands(command)
                        continue

                self.conversation_history = await self.process_query(query)

            except Exception as err:
                logger.error("Error processing query: %s", err)
                continue


async def main():
    mcp_client = MCPClient()
    chatbot = ChatBot(mcp_client)
    try:
        await mcp_client.connect_to_servers("server_config.json")
        mode = input("Enter chat mode (admin/shopper): ").strip().lower()
        if mode == "admin":
            await chatbot.admin_bot()
        elif mode == "shopper":
            await chatbot.shopper_bot()
        else:
            print("Invalid mode. Please enter 'admin' or 'shopper'.")
    finally:
        await mcp_client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
